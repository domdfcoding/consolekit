# stdlib
import re
from typing import Callable, ContextManager, Type

# 3rd party
import click
import pytest
from coincidence.regressions import AdvancedFileRegressionFixture
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
		"contextmanager, exit_code",
		[
				pytest.param(handle_tracebacks, 1, id="handle_tracebacks"),
				pytest.param(traceback_handler, 1, id="traceback_handler"),
				pytest.param(TracebackHandler(), 1, id="TracebackHandler"),
				pytest.param(TracebackHandler(SystemExit(1)), 1, id="TracebackHandler_SystemExit"),
				pytest.param(TracebackHandler(SystemExit(2)), 2, id="TracebackHandler_SystemExit_2"),
				]
		)


@exceptions
@contextmanagers
def test_handle_tracebacks(
		exception: BaseException,
		contextmanager: Callable[..., ContextManager],
		exit_code: int,
		advanced_file_regression: AdvancedFileRegressionFixture,
		cli_runner: CliRunner,
		):

	@click.command()
	def demo() -> None:

		with contextmanager():
			raise exception

	result: Result = cli_runner.invoke(demo, catch_exceptions=False)
	result.check_stdout(advanced_file_regression)
	assert result.exit_code == exit_code


@exceptions
def test_handle_tracebacks_show_traceback(exception: Exception, cli_runner: CliRunner):

	@click.command()
	def demo() -> None:

		with handle_tracebacks(show_traceback=True):
			raise exception

	with pytest.raises(type(exception), match=re.escape(str(exception))):
		cli_runner.invoke(demo, catch_exceptions=False)


@pytest.mark.parametrize("exception", [EOFError(), KeyboardInterrupt(), click.Abort()])
@contextmanagers
def test_handle_tracebacks_ignored_exceptions_click(
		exception: Exception,
		contextmanager: Callable[..., ContextManager],
		cli_runner: CliRunner,
		exit_code: int,
		):

	@click.command()
	def demo() -> None:

		with contextmanager():
			raise exception

	result: Result = cli_runner.invoke(demo, catch_exceptions=False)

	assert result.stdout.strip() == "Aborted!"
	assert result.exit_code == 1


@pytest.mark.parametrize("exception", [EOFError, KeyboardInterrupt, click.Abort, SystemExit])
@contextmanagers
def test_handle_tracebacks_ignored_exceptions(
		exception: Type[Exception],
		contextmanager: Callable[..., ContextManager],
		exit_code: int,
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
		exception: Exception,
		contextmanager: Callable[..., ContextManager],
		advanced_file_regression: AdvancedFileRegressionFixture,
		code: int,
		cli_runner: CliRunner,
		click_version: str,
		exit_code: int,
		):

	@click.command()
	def demo() -> None:

		with contextmanager():
			raise exception

	result = cli_runner.invoke(demo, catch_exceptions=False)
	result.check_stdout(advanced_file_regression)

	# if code == 1 and exit_code == 2:
	# 	code = 2

	assert result.exit_code == code


def test_traceback_option(file_regression: FileRegressionFixture, cli_runner: CliRunner):

	@traceback_option()
	@click_command()
	def main(show_traceback: bool) -> None:
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


def test_traceback_handler_abort(capsys):

	TH = TracebackHandler(ValueError("foo"))

	with pytest.raises(ValueError, match="foo$"):
		TH.abort("Hello World")

	assert capsys.readouterr().err == "Hello World\n"

	with pytest.raises(ValueError, match="foo$"):
		TH.abort(["Hello", "Everybody"])

	assert capsys.readouterr().err == "HelloEverybody\n"
