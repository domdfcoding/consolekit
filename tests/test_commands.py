# stdlib
import inspect
from textwrap import dedent
from typing import Tuple

# 3rd party
import click
import pytest
from coincidence.regressions import AdvancedFileRegressionFixture
from coincidence.selectors import not_windows

# this package
import consolekit.commands
from consolekit import CONTEXT_SETTINGS, click_command, click_group
from consolekit.options import colour_option
from consolekit.terminal_colours import ColourTrilean
from consolekit.testing import CliRunner


@pytest.fixture()
def force_not_pycharm(monkeypatch) -> None:
	# Pretend we aren't running in PyCharm, even if we are.
	monkeypatch.setenv("PYCHARM_HOSTED", '0')
	monkeypatch.setattr(consolekit.utils, "_pycharm_terminal", lambda: False)


@pytest.fixture()
def markdown_demo_command() -> click.Command:

	@click_command(cls=consolekit.commands.MarkdownHelpCommand)
	def demo() -> None:
		"""
		This is the summary line.

		This **program** does *the* ``following``:

		* This
		* That
		* ~~The other~~ (deprecated)

		A
		multiline
		paragraph
		"""

	return demo


@pytest.fixture()
def markdown_demo_command_numbered() -> click.Command:

	@colour_option()
	@click_command(cls=consolekit.commands.MarkdownHelpCommand, no_args_is_help=True)
	def demo(colour: ColourTrilean = None) -> None:
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
	def demo() -> None:
		"""
		This is the summary line.

		This **program** does *the* ``following``:

		* This
		* That
		* ~~The other~~ (deprecated)
		"""

	@demo.command(cls=consolekit.commands.MarkdownHelpCommand)
	def foo() -> None:
		"""
		This is the summary line.

		This **program** does *the* ``following``:

		* This
		* That
		* ~~The other~~ (deprecated)
		"""

	return demo, foo


def test_raw_help_command(
		advanced_file_regression: AdvancedFileRegressionFixture,
		cli_runner: CliRunner,
		):

	@click_command(cls=consolekit.commands.RawHelpCommand)
	def demo() -> None:
		"""
		This is the summary line.

		This **program** does *the* ``following``:

		* This
		* That
		* ~~The other~~ (deprecated)
		"""

	result = cli_runner.invoke(demo, args=["--help"])
	result.check_stdout(advanced_file_regression, extension=".md")

	assert demo.callback.__doc__ is not None
	expected = inspect.cleandoc(demo.callback.__doc__)
	assert dedent('\n'.join(result.stdout.splitlines()[2:-3])) == expected


def test_raw_help_group(
		advanced_file_regression: AdvancedFileRegressionFixture,
		cli_runner: CliRunner,
		):

	@click_group(cls=consolekit.commands.RawHelpGroup)
	def demo() -> None:
		"""
		This is the summary line.

		This **program** does *the* ``following``:

		* This
		* That
		* ~~The other~~ (deprecated)
		"""

	@demo.command(cls=consolekit.commands.RawHelpCommand)
	def foo() -> None:
		"""
		This is the summary line.

		This **program** does *the* ``following``:

		* This
		* That
		* ~~The other~~ (deprecated)
		"""

	result = cli_runner.invoke(demo, args=["--help"])
	result.check_stdout(advanced_file_regression, extension="_group.md")

	result = cli_runner.invoke(foo, args=["--help"])
	result.check_stdout(advanced_file_regression, extension="_command.md")


@pytest.mark.usefixtures("force_not_pycharm")
@not_windows("Windows support for bold and italics is non-existent.")
def test_markdown_help_command(
		advanced_file_regression: AdvancedFileRegressionFixture,
		markdown_demo_command: click.Command,
		cli_runner: CliRunner,
		):
	result = cli_runner.invoke(markdown_demo_command, args=["--help"], color=True)
	result.check_stdout(advanced_file_regression, extension=".md")


@pytest.mark.usefixtures("force_not_pycharm")
@not_windows("Windows support for bold and italics is non-existent.")
def test_markdown_help_group(
		advanced_file_regression: AdvancedFileRegressionFixture,
		markdown_demo_group: Tuple[click.Command, click.Command],
		cli_runner: CliRunner,
		):

	demo_group, demo_command = markdown_demo_group

	result = cli_runner.invoke(demo_group, args=["--help"], color=True)
	result.check_stdout(advanced_file_regression, extension="_group.md")

	result = cli_runner.invoke(demo_command, args=["--help"], color=True)
	result.check_stdout(advanced_file_regression, extension="_command.md")


@pytest.mark.usefixtures("force_not_pycharm")
@not_windows("Windows support for bold and italics is non-existent.")
def test_markdown_help_command_ordered_list(
		advanced_file_regression: AdvancedFileRegressionFixture,
		cli_runner: CliRunner,
		):

	@click_command(cls=consolekit.commands.MarkdownHelpCommand)
	def demo() -> None:
		"""
		This is the summary line.

		This **program** does *the* ``following``:

		1. This
		2. That
		3. ~~The other~~ (deprecated)
		"""

	result = cli_runner.invoke(demo, args=["--help"], color=True)
	result.check_stdout(advanced_file_regression, extension=".md")


@not_windows("Windows support for bold and italics is non-existent.")
def test_markdown_help_command_pycharm(
		advanced_file_regression: AdvancedFileRegressionFixture,
		monkeypatch,
		markdown_demo_command: click.Command,
		cli_runner: CliRunner,
		):
	monkeypatch.setenv("PYCHARM_HOSTED", '1')
	monkeypatch.setattr(consolekit.utils, "_pycharm_terminal", lambda: False)

	result = cli_runner.invoke(markdown_demo_command, args=["--help"], color=True)
	result.check_stdout(advanced_file_regression, extension=".md")


def test_private_helper(monkeypatch):
	monkeypatch.setenv("PYCHARM_HOSTED", '1')

	assert not consolekit.utils._pycharm_terminal()


@pytest.mark.usefixtures("force_not_pycharm")
def test_markdown_help_command_no_colour(
		advanced_file_regression: AdvancedFileRegressionFixture,
		markdown_demo_command_numbered: click.Command,
		cli_runner: CliRunner,
		monkeypatch,
		):

	result = cli_runner.invoke(markdown_demo_command_numbered, args=["--help", "--no-colour"], color=True)
	result.check_stdout(advanced_file_regression, extension=".md")

	# Again with envvar
	monkeypatch.setenv("NO_COLOR", '1')
	result = cli_runner.invoke(markdown_demo_command_numbered, args=["--help"], color=True)
	result.check_stdout(advanced_file_regression, extension=".md")


@pytest.mark.usefixtures("force_not_pycharm")
def test_markdown_help_no_args_is_help(
		advanced_file_regression: AdvancedFileRegressionFixture,
		markdown_demo_command_numbered: click.Command,
		cli_runner: CliRunner,
		):
	result = cli_runner.invoke(markdown_demo_command_numbered)
	result.check_stdout(advanced_file_regression, extension=".md")
	assert result.exit_code == 0


@pytest.mark.usefixtures("force_not_pycharm")
def test_markdown_help_group_no_args_is_help(
		advanced_file_regression: AdvancedFileRegressionFixture,
		markdown_demo_group: Tuple[click.Command, click.Command],
		cli_runner: CliRunner,
		):
	result = cli_runner.invoke(markdown_demo_group[0])
	result.check_stdout(advanced_file_regression, extension=".md")
	assert result.exit_code == 0


def test_suggestion_group(
		advanced_file_regression: AdvancedFileRegressionFixture,
		cli_runner: CliRunner,
		):

	@click_group(context_settings={**CONTEXT_SETTINGS, "token_normalize_func": lambda x: x.lower()})
	def demo() -> None:
		"""
		A program.
		"""

	@demo.command()  # skipcq
	def search() -> None:
		"""
		Conduct a search.
		"""

	result = cli_runner.invoke(demo, args=["searh"])
	result.check_stdout(advanced_file_regression, extension="_success.md")
	assert result.exit_code == 2

	result = cli_runner.invoke(demo, args=["list"])
	result.check_stdout(advanced_file_regression, extension="_failure.md")
	assert result.exit_code == 2

	result = cli_runner.invoke(demo, args=["SEARCH"])
	assert not result.stdout.rstrip()
	assert result.exit_code == 0


def test_context_inheriting_group(
		advanced_file_regression: AdvancedFileRegressionFixture,
		cli_runner: CliRunner,
		):

	@click_group(cls=consolekit.commands.ContextInheritingGroup)
	def demo() -> None:
		"""
		A program.
		"""

	@demo.command()
	def search() -> None:
		"""
		Conduct a search.
		"""

	@demo.group()
	def foo() -> None:
		"""
		Does bar.
		"""

	result = cli_runner.invoke(demo, args=["--help"])
	assert result.exit_code == 0

	result = cli_runner.invoke(demo, args=["-h"])
	assert result.exit_code == 0
	result.check_stdout(advanced_file_regression, extension=".md")

	result = cli_runner.invoke(foo, args=["--help"])
	assert result.exit_code == 0

	result = cli_runner.invoke(foo, args=["-h"])
	assert result.exit_code == 0
	result.check_stdout(advanced_file_regression, extension="_foo.md")

	result = cli_runner.invoke(search, args=["--help"])
	assert result.exit_code == 0

	result = cli_runner.invoke(search, args=["-h"])
	assert result.exit_code == 0
	result.check_stdout(advanced_file_regression, extension="_search.md")
