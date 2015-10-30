import copy
import arrow

from ctx import document


def convert_to_datetime(param, key):
    if key in param and param[key]:
        param[key] = arrow.get(param[key]).datetime


def create_task_from_view_result(value):
    task_params = copy.deepcopy(value['value'])
    task_params['time_slices'] = map(create_time_slice,
                                     task_params['time_slices'])
    convert_to_datetime(task_params, 'created_at')
    return document.Task(**task_params)


def create_time_slice(time_slice_dict):
    time_slice_params = copy.deepcopy(time_slice_dict)
    convert_to_datetime(time_slice_params, 'start_time')
    convert_to_datetime(time_slice_params, 'end_time')

    return document.TimeSlice(**time_slice_params)
