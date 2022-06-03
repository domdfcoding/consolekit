# this package
from consolekit import click_command, click_group

# this package
from . import submodule  # noqa: F401


@click_group()
def commando():
	pass


@click_command()
def command1():
	pass
