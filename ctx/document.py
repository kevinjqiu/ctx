import datetime
import logging
import uuid

from couchdb import mapping


log = logging.getLogger(__name__)


TimeSlice = mapping.Mapping.build(
    start_time=mapping.DateTimeField(default=None),
    end_time=mapping.DateTimeField(default=None),
    note=mapping.TextField(default=''),
)


class Task(mapping.Document):
    _id = mapping.TextField(default=uuid.uuid4().hex[:10])
    description = mapping.TextField()
    created_at = mapping.DateTimeField(default=None)
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
            return datetime.timedelta(0)

        total = datetime.timedelta(0)
        for time_slice in self.time_slices:
            end_time = datetime.datetime.utcnow()
            if time_slice.end_time:
                end_time = time_slice.end_time

            total += end_time - time_slice.start_time

        return total

    def _handle_from_inactive_to_active(self):
        self.time_slices.append(
            TimeSlice(start_time=datetime.datetime.utcnow()))

    def _handle_from_active_to_inactive(self):
        if len(self.time_slices) < 1:
            return
        if self.time_slices[-1].end_time is not None:
            log.warning('Integrity error: '
                        'The last time slice has a not null end_time')
            return
        self.time_slices[-1].end_time = datetime.datetime.utcnow()
