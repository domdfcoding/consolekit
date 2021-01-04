# stdlib
import math
import re
import sys
from typing import Callable, ContextManager

# 3rd party
import click
import pytest
from click.testing import CliRunner, Result
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.testing import check_file_regression
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from consolekit import click_command
from consolekit.utils import coloured_diff, handle_tracebacks, is_command, overtype, traceback_handler


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
def test_handle_tracebacks(exception, contextmanager: Callable[..., ContextManager], file_regression):

	@click.command()
	def demo():

		with contextmanager():
			raise exception

	runner = CliRunner()

	result: Result = runner.invoke(demo, catch_exceptions=False)

	check_file_regression(result.stdout.rstrip(), file_regression)

	assert result.exit_code == 1


@exceptions
def test_handle_tracebacks_show_traceback(exception, file_regression):

	@click.command()
	def demo():

		with handle_tracebacks(show_traceback=True):
			raise exception

	runner = CliRunner()

	with pytest.raises(type(exception), match=re.escape(str(exception))):
		runner.invoke(demo, catch_exceptions=False)


@pytest.mark.parametrize("exception", [EOFError(), KeyboardInterrupt(), click.Abort()])
@contextmanagers
def test_handle_tracebacks_ignored_exceptions(
		exception, contextmanager: Callable[..., ContextManager], file_regression
		):

	@click.command()
	def demo():

		with contextmanager():
			raise exception

	runner = CliRunner()

	result: Result = runner.invoke(demo, catch_exceptions=False)

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
		):

	@click.command()
	def demo():

		with contextmanager():
			raise exception

	runner = CliRunner()

	result: Result = runner.invoke(demo, catch_exceptions=False)

	check_file_regression(result.stdout.rstrip(), file_regression)

	assert result.exit_code == code


def test_is_command():

	@click_command()
	def main():
		...

	assert is_command(main)
	assert not is_command(int)
	assert not is_command(lambda: True)
	assert not is_command(math.ceil)
