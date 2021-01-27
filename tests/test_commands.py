# stdlib
import inspect
from textwrap import dedent
from typing import Tuple

# 3rd party
import click
import pytest
from coincidence import not_windows
from pytest_regressions.file_regression import FileRegressionFixture

# this package
import consolekit.commands
from consolekit import CONTEXT_SETTINGS, click_command, click_group
from consolekit.options import colour_option
from consolekit.terminal_colours import ColourTrilean
from consolekit.testing import CliRunner


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
	@click_command(cls=consolekit.commands.MarkdownHelpCommand, no_args_is_help=True)
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


def test_raw_help_command(
		file_regression: FileRegressionFixture,
		cli_runner: CliRunner,
		):

	@click_command(cls=consolekit.commands.RawHelpCommand)
	def demo():
		"""
		This is the summary line.

		This **program** does *the* ``following``:

		* This
		* That
		* ~~The other~~ (deprecated)
		"""

	result = cli_runner.invoke(demo, args=["--help"])
	result.check_stdout(file_regression, extension=".md")

	assert demo.callback.__doc__ is not None
	expected = inspect.cleandoc(demo.callback.__doc__)
	assert dedent('\n'.join(result.stdout.splitlines()[2:-3])) == expected


def test_raw_help_group(
		file_regression: FileRegressionFixture,
		cli_runner: CliRunner,
		):

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

	result = cli_runner.invoke(demo, args=["--help"])
	result.check_stdout(file_regression, extension="_group.md")

	result = cli_runner.invoke(foo, args=["--help"])
	result.check_stdout(file_regression, extension="_command.md")


@not_windows("Windows support for bold and italics is non-existent.")
def test_markdown_help_command(
		file_regression: FileRegressionFixture,
		force_not_pycharm,
		markdown_demo_command,
		cli_runner: CliRunner,
		):
	result = cli_runner.invoke(markdown_demo_command, args=["--help"], color=True)
	result.check_stdout(file_regression)


@not_windows("Windows support for bold and italics is non-existent.")
def test_markdown_help_group(
		file_regression: FileRegressionFixture,
		force_not_pycharm,
		markdown_demo_group,
		cli_runner: CliRunner,
		):

	demo_group, demo_command = markdown_demo_group

	result = cli_runner.invoke(demo_group, args=["--help"], color=True)
	result.check_stdout(file_regression, extension="_group.md")

	result = cli_runner.invoke(demo_command, args=["--help"], color=True)
	result.check_stdout(file_regression, extension="_command.md")


@not_windows("Windows support for bold and italics is non-existent.")
def test_markdown_help_command_ordered_list(
		file_regression: FileRegressionFixture,
		force_not_pycharm,
		cli_runner: CliRunner,
		):

	@click_command(cls=consolekit.commands.MarkdownHelpCommand)
	def demo():
		"""
		This is the summary line.

		This **program** does *the* ``following``:

		1. This
		2. That
		3. ~~The other~~ (deprecated)
		"""

	result = cli_runner.invoke(demo, args=["--help"], color=True)
	result.check_stdout(file_regression)


@not_windows("Windows support for bold and italics is non-existent.")
def test_markdown_help_command_pycharm(
		file_regression: FileRegressionFixture,
		monkeypatch,
		markdown_demo_command,
		cli_runner: CliRunner,
		):
	monkeypatch.setattr(consolekit.utils, "_pycharm_hosted", lambda: True)
	monkeypatch.setattr(consolekit.utils, "_pycharm_terminal", lambda: False)

	result = cli_runner.invoke(markdown_demo_command, args=["--help"], color=True)
	result.check_stdout(file_regression, extension=".md")


def test_private_helpers(monkeypatch):
	monkeypatch.setenv("PYCHARM_HOSTED", '1')

	assert consolekit.utils._pycharm_hosted()
	assert not consolekit.utils._pycharm_terminal()


def test_markdown_help_command_no_colour(
		file_regression: FileRegressionFixture,
		force_not_pycharm,
		markdown_demo_command_numbered,
		cli_runner: CliRunner,
		):
	result = cli_runner.invoke(markdown_demo_command_numbered, args=["--help", "--no-colour"], color=True)
	result.check_stdout(file_regression)


def test_markdown_help_no_args_is_help(
		file_regression: FileRegressionFixture,
		force_not_pycharm,
		markdown_demo_command_numbered,
		cli_runner: CliRunner,
		):
	result = cli_runner.invoke(markdown_demo_command_numbered)
	result.check_stdout(file_regression)
	assert result.exit_code == 0


def test_suggestion_group(
		file_regression: FileRegressionFixture,
		cli_runner: CliRunner,
		):

	@click_group(
			cls=consolekit.commands.SuggestionGroup,
			context_settings={**CONTEXT_SETTINGS, "token_normalize_func": lambda x: x.lower()}
			)
	def demo():
		"""
		A program.
		"""

	@demo.command()
	def search():
		"""
		Conduct a search.
		"""

	result = cli_runner.invoke(demo, args=["searh"])
	result.check_stdout(file_regression, extension="_success.md")
	assert result.exit_code == 2

	result = cli_runner.invoke(demo, args=["list"])
	result.check_stdout(file_regression, extension="_failure.md")
	assert result.exit_code == 2

	result = cli_runner.invoke(demo, args=["SEARCH"])
	assert not result.stdout.rstrip()
	assert result.exit_code == 0
