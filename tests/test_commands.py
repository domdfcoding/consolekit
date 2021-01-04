# stdlib
import inspect
from textwrap import dedent
from typing import Tuple

# 3rd party
import click
import pytest
from click.testing import CliRunner, Result
from domdf_python_tools.testing import check_file_regression, not_windows
from pytest_regressions.file_regression import FileRegressionFixture

# this package
import consolekit.commands
from consolekit import click_command, click_group
from consolekit.options import colour_option
from consolekit.terminal_colours import ColourTrilean


@pytest.fixture()
def force_not_pycharm(monkeypatch):
	# Pretend we aren't running in PyCharm, even if we are.
	monkeypatch.setattr(consolekit.utils, "_pycharm_hosted", lambda: False)
	monkeypatch.setattr(consolekit.utils, "_pycharm_terminal", lambda: False)


@pytest.fixture()
def markdown_demo_command() -> click.Command:

	@click_command(cls=consolekit.commands.MarkdownHelpCommand)
	def demo():
		"""
		This is the summary line.

		This **program** does *the* ``following``:

		* This
		* That
		* ~~The other~~ (deprecated)
		"""

	return demo


@pytest.fixture()
def markdown_demo_command_numbered() -> click.Command:

	@colour_option()
	@click_command(cls=consolekit.commands.MarkdownHelpCommand)
	def demo(colour: ColourTrilean = None):
		"""
		This is the summary line.

		This **program** does *the* ``following``:

		1. This
		2. That
		3. ~~The other~~ (deprecated)
		"""

	return demo


@pytest.fixture()
def markdown_demo_group() -> Tuple[click.Command, click.Command]:

	@click_group(cls=consolekit.commands.MarkdownHelpGroup)
	def demo():
		"""
		This is the summary line.

		This **program** does *the* ``following``:

		* This
		* That
		* ~~The other~~ (deprecated)
		"""

	@demo.command(cls=consolekit.commands.MarkdownHelpCommand)
	def foo():
		"""
		This is the summary line.

		This **program** does *the* ``following``:

		* This
		* That
		* ~~The other~~ (deprecated)
		"""

	return demo, foo


def test_raw_help_command(file_regression: FileRegressionFixture):

	@click_command(cls=consolekit.commands.RawHelpCommand)
	def demo():
		"""
		This is the summary line.

		This **program** does *the* ``following``:

		* This
		* That
		* ~~The other~~ (deprecated)
		"""

	runner = CliRunner()

	result: Result = runner.invoke(demo, catch_exceptions=False, args=["--help"])
	check_file_regression(result.stdout.rstrip(), file_regression, extension=".md")

	assert demo.callback.__doc__ is not None
	expected = inspect.cleandoc(demo.callback.__doc__)
	assert dedent('\n'.join(result.stdout.splitlines()[2:-3])) == expected


def test_raw_help_group(file_regression: FileRegressionFixture):

	@click_group(cls=consolekit.commands.RawHelpGroup)
	def demo():
		"""
		This is the summary line.

		This **program** does *the* ``following``:

		* This
		* That
		* ~~The other~~ (deprecated)
		"""

	@demo.command(cls=consolekit.commands.RawHelpCommand)
	def foo():
		"""
		This is the summary line.

		This **program** does *the* ``following``:

		* This
		* That
		* ~~The other~~ (deprecated)
		"""

	runner = CliRunner()

	result: Result = runner.invoke(demo, catch_exceptions=False, args=["--help"])
	check_file_regression(result.stdout.rstrip(), file_regression, extension="_group.md")

	result = runner.invoke(foo, catch_exceptions=False, args=["--help"])
	check_file_regression(result.stdout.rstrip(), file_regression, extension="_command.md")


@not_windows("Windows support for bold and italics is non-existent.")
def test_markdown_help_command(
		file_regression: FileRegressionFixture,
		force_not_pycharm,
		markdown_demo_command,
		):
	runner = CliRunner()

	result: Result = runner.invoke(markdown_demo_command, catch_exceptions=False, args=["--help"], color=True)
	check_file_regression(result.stdout.rstrip(), file_regression)


@not_windows("Windows support for bold and italics is non-existent.")
def test_markdown_help_group(
		file_regression: FileRegressionFixture,
		force_not_pycharm,
		markdown_demo_group,
		):

	runner = CliRunner()

	demo_group, demo_command = markdown_demo_group

	result: Result = runner.invoke(demo_group, catch_exceptions=False, args=["--help"], color=True)
	check_file_regression(result.stdout.rstrip(), file_regression, extension="_group.md")

	result = runner.invoke(demo_command, catch_exceptions=False, args=["--help"], color=True)
	check_file_regression(result.stdout.rstrip(), file_regression, extension="_command.md")


@not_windows("Windows support for bold and italics is non-existent.")
def test_markdown_help_command_ordered_list(file_regression: FileRegressionFixture, force_not_pycharm):

	@click_command(cls=consolekit.commands.MarkdownHelpCommand)
	def demo():
		"""
		This is the summary line.

		This **program** does *the* ``following``:

		1. This
		2. That
		3. ~~The other~~ (deprecated)
		"""

	runner = CliRunner()

	result: Result = runner.invoke(demo, catch_exceptions=False, args=["--help"], color=True)
	check_file_regression(result.stdout.rstrip(), file_regression)


@not_windows("Windows support for bold and italics is non-existent.")
def test_markdown_help_command_pycharm(
		file_regression: FileRegressionFixture,
		monkeypatch,
		markdown_demo_command,
		):
	monkeypatch.setattr(consolekit.utils, "_pycharm_hosted", lambda: True)
	monkeypatch.setattr(consolekit.utils, "_pycharm_terminal", lambda: False)

	runner = CliRunner()

	result: Result = runner.invoke(markdown_demo_command, catch_exceptions=False, args=["--help"], color=True)
	check_file_regression(result.stdout.rstrip(), file_regression)


def test_private_helpers(monkeypatch):
	monkeypatch.setenv("PYCHARM_HOSTED", '1')

	assert consolekit.utils._pycharm_hosted()
	assert not consolekit.utils._pycharm_terminal()


def test_markdown_help_command_no_colour(
		file_regression: FileRegressionFixture,
		force_not_pycharm,
		markdown_demo_command_numbered,
		):

	runner = CliRunner()

	result: Result = runner.invoke(
			markdown_demo_command_numbered, catch_exceptions=False, args=["--help", "--no-colour"], color=True
			)
	check_file_regression(result.stdout.rstrip(), file_regression)
