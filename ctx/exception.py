class DuplicateTaskID(Exception):
    pass


class MultipleActiveTasks(Exception):
    pass


class TaskNotFound(Exception):
    pass


class TaskNotRunning(Exception):
    pass


class TaskAlreadyRunning(Exception):
    pass
