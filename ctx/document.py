import datetime
import uuid

from couchdb import mapping


TimeSlice = mapping.Mapping.build(
    start_time=mapping.DateTimeField(default=datetime.datetime.utcnow()),
    end_time=mapping.DateTimeField(default=None),
    note=mapping.TextField(default=''),
)


class Task(mapping.Document):
    _id = mapping.TextField(default=uuid.uuid4().hex[:10])
    description = mapping.TextField()
    created_at = mapping.DateTimeField(default=datetime.datetime.utcnow())
    time_slices = mapping.ListField(mapping.DictField(TimeSlice))
    is_active = mapping.BooleanField(default=False)
