# stdlib
import math
import re
import sys
from typing import Callable, ContextManager

# 3rd party
import click
import pytest
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.testing import check_file_regression
from pytest_regressions.data_regression import DataRegressionFixture
from pytest_regressions.file_regression import FileRegressionFixture

# this package
import consolekit
from consolekit import click_command
from consolekit.testing import CliRunner, Result
from consolekit.utils import (
		coloured_diff,
		handle_tracebacks,
		hidden_cursor,
		hide_cursor,
		is_command,
		overtype,
		show_cursor,
		solidus_spinner,
		traceback_handler
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


exceptions = pytest.mark.parametrize(
		"exception",
		[
				pytest.param(FileNotFoundError("foo.txt"), id="FileNotFoundError"),
				pytest.param(FileExistsError("foo.txt"), id="FileExistsError"),
				pytest.param(Exception("Something's awry!"), id="Exception"),
				pytest.param(ValueError("'age' must be >= 0"), id="ValueError"),
				pytest.param(TypeError("Expected type int, got type str"), id="TypeError"),
				pytest.param(NameError("name 'hello' is not defined"), id="NameError"),
				pytest.param(SyntaxError("invalid syntax"), id="SyntaxError"),
				]
		)
contextmanagers = pytest.mark.parametrize(
		"contextmanager",
		[
				pytest.param(handle_tracebacks, id="handle_tracebacks"),
				pytest.param(traceback_handler, id="traceback_handler"),
				]
		)


@exceptions
@contextmanagers
def test_handle_tracebacks(
		exception,
		contextmanager: Callable[..., ContextManager],
		file_regression,
		cli_runner: CliRunner,
		):

	@click.command()
	def demo():

		with contextmanager():
			raise exception

	result: Result = cli_runner.invoke(demo, catch_exceptions=False)
	result.check_stdout(file_regression)
	assert result.exit_code == 1


@exceptions
def test_handle_tracebacks_show_traceback(
		exception,
		file_regression,
		cli_runner: CliRunner,
		):

	@click.command()
	def demo():

		with handle_tracebacks(show_traceback=True):
			raise exception

	with pytest.raises(type(exception), match=re.escape(str(exception))):
		cli_runner.invoke(demo, catch_exceptions=False)


@pytest.mark.parametrize("exception", [EOFError(), KeyboardInterrupt(), click.Abort()])
@contextmanagers
def test_handle_tracebacks_ignored_exceptions(
		exception,
		contextmanager: Callable[..., ContextManager],
		file_regression,
		cli_runner: CliRunner,
		):

	@click.command()
	def demo():

		with contextmanager():
			raise exception

	result: Result = cli_runner.invoke(demo, catch_exceptions=False)

	assert result.stdout.strip() == "Aborted!"
	assert result.exit_code == 1


@pytest.mark.parametrize(
		"exception, code",
		[
				pytest.param(click.UsageError("Message"), 2, id="click.UsageError"),
				pytest.param(click.BadParameter("Message"), 2, id="click.BadParameter"),
				pytest.param(click.FileError("Message"), 1, id="click.FileError"),
				pytest.param(click.ClickException("Message"), 1, id="click.ClickException"),
				]
		)
@contextmanagers
def test_handle_tracebacks_ignored_click(
		exception,
		contextmanager: Callable[..., ContextManager],
		file_regression,
		code: int,
		cli_runner: CliRunner,
		):

	@click.command()
	def demo():

		with contextmanager():
			raise exception

	result = cli_runner.invoke(demo, catch_exceptions=False)
	result.check_stdout(file_regression)
	assert result.exit_code == code


def test_is_command():

	@click_command()
	def main():
		...

	assert is_command(main)
	assert not is_command(int)
	assert not is_command(lambda: True)
	assert not is_command(math.ceil)


def test_hidden_cursor(monkeypatch, capsys, data_regression: DataRegressionFixture):
	monkeypatch.setattr(consolekit.terminal_colours, "resolve_color_default", lambda *args: True)

	hide_cursor()
	show_cursor()

	with hidden_cursor():
		click.echo(f"\r{next(solidus_spinner)}", nl=False)
		click.echo(f"\r{next(solidus_spinner)}", nl=False)
		click.echo(f"\r{next(solidus_spinner)}", nl=False)

	data_regression.check(tuple(capsys.readouterr()))
