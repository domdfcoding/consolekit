# this package
from consolekit import click_command, click_group

# this package
from . import submodule


@click_group()
def commando():
	pass


@click_command()
def command1():
	pass
