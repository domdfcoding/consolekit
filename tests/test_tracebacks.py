# stdlib
import math
import re
import sys
from typing import Callable, ContextManager

# 3rd party
import click
import pytest
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from consolekit import click_command
from consolekit.testing import CliRunner, Result, _click_major
from consolekit.tracebacks import TracebackHandler, handle_tracebacks, traceback_handler, traceback_option

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
				pytest.param(TracebackHandler(), id="TracebackHandler"),
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
def test_handle_tracebacks_ignored_exceptions_click(
		exception,
		contextmanager: Callable[..., ContextManager],
		cli_runner: CliRunner,
		):

	@click.command()
	def demo():

		with contextmanager():
			raise exception

	result: Result = cli_runner.invoke(demo, catch_exceptions=False)

	assert result.stdout.strip() == "Aborted!"
	assert result.exit_code == 1


@pytest.mark.parametrize("exception", [EOFError, KeyboardInterrupt, click.Abort, SystemExit])
@contextmanagers
def test_handle_tracebacks_ignored_exceptions(
		exception,
		contextmanager: Callable[..., ContextManager],
		):

	with pytest.raises(exception):  # noqa: PT012
		with contextmanager():
			raise exception


@pytest.mark.parametrize(
		"exception, code",
		[
				pytest.param(click.UsageError("Message"), 2, id="click.UsageError"),
				pytest.param(click.BadParameter("Message"), 2, id="click.BadParameter"),
				pytest.param(
						click.FileError("Message"),
						1,
						id="click.FileError",
						marks=pytest.mark.skipif(_click_major == 8, reason="Output differs on Click 8")
						),
				pytest.param(
						click.FileError("Message"),
						1,
						id="click.FileError_8",
						marks=pytest.mark.skipif(_click_major != 8, reason="Output differs on Click 8")
						),
				pytest.param(click.ClickException("Message"), 1, id="click.ClickException"),
				]
		)
@contextmanagers
@pytest.mark.parametrize(
		"click_version",
		[
				pytest.param(
						'7',
						marks=pytest.mark.skipif(_click_major == 8, reason="Output differs on click 8"),
						),
				pytest.param(
						'8',
						marks=pytest.mark.skipif(_click_major != 8, reason="Output differs on click 8"),
						),
				]
		)
def test_handle_tracebacks_ignored_click(
		exception,
		contextmanager: Callable[..., ContextManager],
		file_regression,
		code: int,
		cli_runner: CliRunner,
		click_version: str
		):

	@click.command()
	def demo():

		with contextmanager():
			raise exception

	result = cli_runner.invoke(demo, catch_exceptions=False)
	result.check_stdout(file_regression)
	assert result.exit_code == code


def test_traceback_option(file_regression: FileRegressionFixture, cli_runner: CliRunner):

	@traceback_option()
	@click_command()
	def main(show_traceback: bool):
		print(show_traceback)

	result = cli_runner.invoke(main, catch_exceptions=False)
	assert result.stdout.rstrip() == "False"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args="--traceback")
	assert result.stdout.rstrip() == "True"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args="-T")
	assert result.stdout.rstrip() == "True"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args="-h")
	result.check_stdout(file_regression)
	assert result.exit_code == 0
