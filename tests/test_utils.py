# stdlib
import math
import os
import shutil
import sys
from typing import Tuple

# 3rd party
import click
from coincidence.regressions import AdvancedDataRegressionFixture, check_file_regression
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.utils import redirect_output
from pytest_regressions.file_regression import FileRegressionFixture

# this package
import consolekit
from consolekit import click_command
from consolekit.utils import (
		coloured_diff,
		hidden_cursor,
		hide_cursor,
		import_commands,
		is_command,
		long_echo,
		overtype,
		show_cursor,
		solidus_spinner
		)


def test_overtype(capsys):
	print("Waiting...", end='')
	overtype("foo", "bar")
	sys.stdout.flush()

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout == ["Waiting...\rfoo bar"]

	print("Waiting...", end='')
	overtype("foo", "bar", sep='')
	sys.stdout.flush()

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout == ["Waiting...\rfoobar"]

	print("Waiting...", end='')
	overtype("foo", "bar", sep='-', end='\n')
	sys.stdout.flush()

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout == ["Waiting...\rfoo-bar", '']

	sys.stderr.write("Waiting...")
	overtype("foo", "bar", file=sys.stderr)
	sys.stdout.flush()

	captured = capsys.readouterr()
	stderr = captured.err.split('\n')
	assert stderr == ["Waiting...\rfoo bar"]


def test_coloured_diff(file_regression: FileRegressionFixture):
	data_dir = PathPlus(__file__).parent / "test_diff_"
	original = data_dir / "original"
	modified = data_dir / "modified"

	diff = coloured_diff(
			original.read_lines(),
			modified.read_lines(),
			fromfile="original_file.txt",
			tofile="modified_file.txt",
			fromfiledate="(original)",
			tofiledate="(modified)",
			lineterm='',
			)

	check_file_regression(diff, file_regression)


def test_is_command():

	@click_command()
	def main(): ...

	assert is_command(main)
	assert not is_command(int)
	assert not is_command(lambda: True)
	assert not is_command(math.ceil)


def test_hidden_cursor(monkeypatch, capsys, advanced_data_regression: AdvancedDataRegressionFixture):
	monkeypatch.setattr(consolekit.terminal_colours, "resolve_color_default", lambda *args: True)

	hide_cursor()
	show_cursor()

	with hidden_cursor():
		click.echo(f"\r{next(solidus_spinner)}", nl=False)
		click.echo(f"\r{next(solidus_spinner)}", nl=False)
		click.echo(f"\r{next(solidus_spinner)}", nl=False)

	advanced_data_regression.check(tuple(capsys.readouterr()))


def test_import_commands():
	# this package
	from tests import import_commands_demo

	commands = import_commands(import_commands_demo)
	assert commands == [
			import_commands_demo.command1,
			import_commands_demo.commando,
			import_commands_demo.submodule.command2,
			import_commands_demo.submodule.group2,
			]


def test_long_echo(monkeypatch):

	def get_terminal_size(fallback: Tuple[int, int] = (80, 24)):
		return os.terminal_size((80, 5))

	def echo_via_pager(text_or_generator, color=None):
		click.echo('\n'.join(f"|{line}" for line in text_or_generator.splitlines()))

	monkeypatch.setattr(shutil, "get_terminal_size", get_terminal_size)
	monkeypatch.setattr(click, "echo_via_pager", echo_via_pager)

	with redirect_output() as (stdout, stderr):
		stdout.isatty = lambda *args: True  # type: ignore
		assert stdout.isatty()
		assert sys.stdout.isatty()

		long_echo([
				"Line 1",
				"Line 2",
				"Line 3",
				"Line 4",
				"Line 5",
				"Line 6",
				])

	assert stdout.getvalue() == "|Line 1\n|Line 2\n|Line 3\n|Line 4\n|Line 5\n|Line 6\n"

	with redirect_output() as (stdout, stderr):
		stdout.isatty = lambda *args: True  # type: ignore
		assert stdout.isatty()
		assert sys.stdout.isatty()

		long_echo('\n'.join([
				"Line 1",
				"Line 2",
				"Line 3",
				"Line 4",
				"Line 5",
				]))

	assert stdout.getvalue() == "Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n"
