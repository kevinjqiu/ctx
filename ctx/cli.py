import click
from ctx import version, config


@click.group()
def main():
    pass


@click.command()
def info():
    click.echo('version: {}'.format(version.__version__))
    click.echo('db_url: {}'.format(config.DB_URL))


main.add_command(info)
