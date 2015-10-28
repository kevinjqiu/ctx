import datetime
import uuid

from couchdb import mapping


TimeSlice = mapping.Mapping.build(
    start_time=mapping.DateTimeField(),
    end_time=mapping.DateTimeField(),
    note=mapping.TextField(),
)


class Task(mapping.Document):
    title = mapping.TextField(default='')
    description = mapping.TextField(default='')
    created_at = mapping.DateTimeField(default=datetime.datetime.now())
    time_slices = mapping.ListField(mapping.DictField(TimeSlice))
    is_active = mapping.BooleanField(default=False)
