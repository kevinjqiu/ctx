import click
import functools

from ctx import exception, version, config, database, document_manager


def inject_document_manager(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        database.init()
        doc_mgr = document_manager.DocumentManager(database.db)
        return fn(doc_mgr, *args, **kwargs)
    return wrapper


@click.group()
def main():
    pass


@click.command(name='version')
def cmd_version():
    click.echo('version: {}'.format(version.__version__))
    click.echo('db_url: {}'.format(config.DB_URL))


@click.command(name='info')
@click.option('-f', '--format-str', default=None, help=('Format the output.\n'
                                                        '{id} - the id of the task\n'
                                                        '{description} - description of the task\n'
                                                        '{duration} - the duration of the task\n'
                                                        '{status} - the status of the task\n'))
@inject_document_manager
def cmd_info(doc_mgr, format_str):
    current_task = doc_mgr.get_active_task()
    if not current_task:
        click.echo('No active tasks')
        return

    if not format_str:
        format_str = 'task: {id} {description}\ntotal time: {duration}\nstatus: {status}'

    click.echo(format_str.format(id=current_task.id,
                                 description=current_task.description,
                                 duration=current_task.total_time,
                                 status=current_task.status.name))


@click.command(name='switch')
@click.argument('id')
@inject_document_manager
def cmd_switch(doc_mgr, id):
    task = doc_mgr.get_task_by_id(id)
    current_task = doc_mgr.get_active_task()
    if current_task:
        current_task.set_active(False)
        doc_mgr.update_task(current_task)

    task.set_active(True)
    doc_mgr.update_task(task)

    click.echo('Switched to task {!r}'.format(id))


@click.command(name='new')
@click.option('-d', '--description', default='', help='summary of the task')
@click.option('-s', '--switch', default=False, is_flag=True, help='create a new task and switch to it')
@click.argument('id')
@click.pass_context
@inject_document_manager
def cmd_new(doc_mgr, cli_context, id, description, switch):
    try:
        task = doc_mgr.create_task(_id=id)
        if description:
            task.description = description
        doc_mgr.update_task(task)
        click.echo('Created task {!r}'.format(id))
    except exception.DuplicateTaskID:
        click.echo('Cannot create task {!r}: Duplicate task ID'.format(id))
    else:
        if switch:
            cli_context.invoke(cmd_switch, id=id)


@click.command(name='list')
@inject_document_manager
def cmd_list(doc_mgr):
    tasks = doc_mgr.get_tasks()
    for task in tasks.rows:
        click.echo('{is_active} {task_id} {description} {total_time}'.format(
            is_active='*' if task.is_active else ' ',
            task_id=task.id,
            description=task.get('description'),
            total_time=task.total_time))


@click.command(name='stop')
@inject_document_manager
def cmd_stop(doc_mgr):
    task = doc_mgr.get_active_task()
    if not task:
        click.echo('No active tasks')
        return

    try:
        task.stop()
    except exception.TaskNotRunning:
        click.echo('Current task is not running')
        return

    doc_mgr.update_task(task)


@click.command(name='start')
@inject_document_manager
def cmd_start(doc_mgr):
    task = doc_mgr.get_active_task()
    if not task:
        click.echo('No active tasks')
        return

    try:
        task.start()
    except exception.TaskNotRunning:
        click.echo('Current task is already running')
        return

    doc_mgr.update_task(task)


main.add_command(cmd_info)
main.add_command(cmd_new)
main.add_command(cmd_list)
main.add_command(cmd_version)
main.add_command(cmd_switch)
main.add_command(cmd_stop)
main.add_command(cmd_start)
