import click
from ctx import exception


def new_task(doc_mgr, id, description):
    try:
        task = doc_mgr.create_task(_id=id)
        # get the current active task
        # set is_active to False
        # set this task.is_active to True
        task.set_active(True)
        doc_mgr.update_task(task)
    except exception.DuplicateTaskID:
        click.echo('Cannot create task {!r}: Duplicate task ID'.format(id))
    else:
        click.echo('Created task {!r}'.format(task._id))
        return task


def show_current_task(doc_mgr):
    current_task = doc_mgr.get_current_task()
    if not current_task:
        click.echo('No active tasks')
        return
    click.echo('{}'.format(current_task.id))
