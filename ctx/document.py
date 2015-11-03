import calendar
import enum
import logging
import time
import uuid

from couchdb import mapping
from datetime import datetime, timedelta
from time import struct_time
from ctx import exception


log = logging.getLogger(__name__)


class Duration():
    def __init__(self, timedelta_object):
        self.timedelta = timedelta_object

    def __getattr__(self, key):
        return getattr(self.timedelta, key)

    def __str__(self):
        pieces = []
        if self.timedelta.days:
            pieces.append('{}d'.format(self.timedelta.days))
        if self.timedelta.seconds:
            hours = self.timedelta.seconds // 60 // 60
            minutes = (self.timedelta.seconds - (hours * 60 * 60)) // 60
            if hours:
                pieces.append('{}h'.format(hours))
            if minutes:
                pieces.append('{}m'.format(minutes))
        if not pieces:
            return '0m'
        else:
            return ''.join(pieces)

    def __eq__(self, other):
        if isinstance(other, timedelta):
            return self.timedelta == other
        return super().__eq__(other)


class TaskStatus(enum.Enum):
    not_started = 'not started'
    running = 'running'
    stopped = 'stopped'


class UTCDateTimeField(mapping.DateTimeField):
    def _to_json(self, value):
        if isinstance(value, str):
            return value
        if isinstance(value, struct_time):
            value = datetime.utcfromtimestamp(calendar.timegm(value))
        elif not isinstance(value, datetime):
            value = datetime.combine(value, time(0))
        value = value.replace(microsecond=0)
        return value.isoformat().split('+')[0] + 'Z'


TimeSlice = mapping.Mapping.build(
    start_time=UTCDateTimeField(default=None),
    end_time=UTCDateTimeField(default=None),
    note=mapping.TextField(default=''),
)


class Task(mapping.Document):
    _id = mapping.TextField(default=uuid.uuid4().hex[:10])
    description = mapping.TextField(default='')
    created_at = UTCDateTimeField(default=None)
    time_slices = mapping.ListField(mapping.DictField(TimeSlice))
    is_active = mapping.BooleanField(default=False)

    def set_active(self, is_active):
        if self.is_active == is_active:
            return

        if is_active:
            self._handle_from_inactive_to_active()
        else:
            self._handle_from_active_to_inactive()
        self.is_active = is_active

    @property
    def total_time(self):
        if len(self.time_slices) == 0:
            return timedelta(0)

        total = timedelta(0)
        for time_slice in self.time_slices:
            end_time = datetime.utcnow()
            if time_slice.end_time:
                end_time = time_slice.end_time

            total += end_time - time_slice.start_time

        return Duration(total)

    @property
    def status(self):
        if len(self.time_slices) == 0:
            return TaskStatus.not_started

        latest_slice = self.time_slices[-1]

        if not latest_slice.end_time:
            return TaskStatus.running
        else:
            return TaskStatus.stopped

    def stop(self):
        if self.status != TaskStatus.running:
            raise exception.TaskNotRunning()

        self.time_slices[-1].end_time = datetime.utcnow()

    def _handle_from_inactive_to_active(self):
        self.time_slices.append(
            TimeSlice(start_time=datetime.utcnow()))

    def _handle_from_active_to_inactive(self):
        if len(self.time_slices) < 1:
            return
        if self.time_slices[-1].end_time is not None:
            log.warning('Integrity error: '
                        'The last time slice has a not null end_time')
            return
        self.time_slices[-1].end_time = datetime.utcnow()
