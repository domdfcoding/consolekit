# stdlib
import sys
from typing import Iterable

# 3rd party
import click
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from consolekit import click_command
from consolekit.options import (
		DescribedArgument,
		MultiValueOption,
		auto_default_argument,
		auto_default_option,
		colour_option,
		flag_option,
		force_option,
		no_pager_option,
		verbose_option,
		version_option
		)
from consolekit.terminal_colours import ColourTrilean
from consolekit.testing import CliRunner, Result


def test_described_argument(
		file_regression: FileRegressionFixture,
		cli_runner: CliRunner,
		):

	@click.argument(
			"dest",
			cls=DescribedArgument,
			type=click.STRING,
			description="The destination directory.",
			)
	@click_command()
	def main(dest: str):
		print(dest)

	result = cli_runner.invoke(main, args="--help")
	result.check_stdout(file_regression, extension=".md")
	assert result.exit_code == 0

	result = cli_runner.invoke(main, catch_exceptions=False, args="./staging")
	assert result.stdout.rstrip() == "./staging"
	assert result.exit_code == 0

	ctx = click.Context(main, info_name="main", parent=None)
	argument = ctx.command.params[0]
	assert isinstance(argument, DescribedArgument)
	assert argument.description == "The destination directory."


def test_auto_default_option(
		file_regression: FileRegressionFixture,
		cli_runner: CliRunner,
		):

	@auto_default_option(
			"--width",
			type=click.INT,
			help="The max width to display.",
			show_default=True,
			)
	@click_command()
	def main(width: int = 80):
		print(width)

	argument = main.params[0]
	assert argument.default == 80
	assert not argument.required
	assert argument.show_default

	result = cli_runner.invoke(main, args="--help")
	result.check_stdout(file_regression, extension=".md")
	assert result.exit_code == 0

	result = cli_runner.invoke(main, catch_exceptions=False)
	assert result.stdout.rstrip() == "80"
	assert result.exit_code == 0

	for width in [0, 8, 36, 48, 130]:

		result = cli_runner.invoke(main, args=["--width", str(width)])
		assert result.stdout.rstrip() == str(width)
		assert result.exit_code == 0


def test_flag_option(cli_runner: CliRunner):

	@flag_option("--no-colour")
	@click_command()
	def main(no_colour: bool):
		print(no_colour)

	result = cli_runner.invoke(main, catch_exceptions=False)
	assert result.stdout.rstrip() == "False"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args="--no-colour")
	assert result.stdout.rstrip() == "True"
	assert result.exit_code == 0


def test_no_pager_option(file_regression: FileRegressionFixture, cli_runner: CliRunner):

	@no_pager_option()
	@click_command()
	def main(no_pager: bool):
		print(no_pager)

	result = cli_runner.invoke(main, catch_exceptions=False)
	assert result.stdout.rstrip() == "False"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args="--no-pager")
	assert result.stdout.rstrip() == "True"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args="-h")
	result.check_stdout(file_regression)
	assert result.exit_code == 0


def test_force_option(file_regression: FileRegressionFixture, cli_runner: CliRunner):

	@force_option("Force the operation")
	@click_command()
	def main(force: bool):
		print(force)

	result = cli_runner.invoke(main, catch_exceptions=False)
	assert result.stdout.rstrip() == "False"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args="--force")
	assert result.stdout.rstrip() == "True"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args="-f")
	assert result.stdout.rstrip() == "True"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args="-h")
	result.check_stdout(file_regression)
	assert result.exit_code == 0


def test_verbose_option(file_regression: FileRegressionFixture, cli_runner: CliRunner):

	@verbose_option("Show verbose output.")
	@click_command()
	def main(verbose: int):
		print(verbose)

	result = cli_runner.invoke(main)
	assert result.stdout.rstrip() == '0'
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args="--verbose")
	assert result.stdout.rstrip() == '1'
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args="-v")
	assert result.stdout.rstrip() == '1'
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args=["--verbose", "--verbose"])
	assert result.stdout.rstrip() == '2'
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args="-vv")
	assert result.stdout.rstrip() == '2'
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args="-vvv")
	assert result.stdout.rstrip() == '3'
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args="-h")
	result.check_stdout(file_regression)
	assert result.exit_code == 0


def test_colour_option(file_regression: FileRegressionFixture, cli_runner: CliRunner):

	@colour_option()
	@click_command()
	def main(colour: ColourTrilean):
		print(colour)

	result = cli_runner.invoke(main, catch_exceptions=False)
	assert result.stdout.rstrip() == "None"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args="--no-colour")
	assert result.stdout.rstrip() == "False"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args="--colour")
	assert result.stdout.rstrip() == "True"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args="-h")
	result.check_stdout(file_regression)
	assert result.exit_code == 0


def test_version_option(file_regression: FileRegressionFixture, cli_runner: CliRunner):

	def version_callback(ctx: click.Context, param: click.Option, value: int):
		if not value or ctx.resilient_parsing:
			return

		if value > 1:
			click.echo("consolekit version 1.2.3, Python 3.8.5")
		else:
			click.echo("consolekit version 1.2.3")

		ctx.exit()

	@version_option(version_callback)
	@click_command()
	def main():
		sys.exit(1)

	result = cli_runner.invoke(main, args="--version")
	assert result.stdout.rstrip() == "consolekit version 1.2.3"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args=["--version", "--version"])
	assert result.stdout.rstrip() == "consolekit version 1.2.3, Python 3.8.5"
	assert result.exit_code == 0


def test_multi_value_option(cli_runner: CliRunner):

	@click.option(
			"--select",
			type=click.STRING,
			help="The checks to enable",
			cls=MultiValueOption,
			)
	@colour_option()
	@click_command()
	def main(select: Iterable[str], colour: bool):
		select = list(select)
		print(*select)
		print(", ".join(select))

	result: Result = cli_runner.invoke(main, catch_exceptions=False)
	assert result.stdout.rstrip() == ''
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args=["--select", "E102", "F223"])
	assert result.stdout.rstrip() == "E102 F223\nE102, F223"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args=["--select", "E102", "F223", "--colour"])
	assert result.stdout.rstrip() == "E102 F223\nE102, F223"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args=["--select", "E102"])
	assert result.stdout.rstrip() == "E102\nE102"
	assert result.exit_code == 0


def test_auto_default_argument(cli_runner: CliRunner):

	@auto_default_argument(
			"greeting",
			type=click.STRING,
			)
	@click_command()
	def main(greeting: str = "Hello"):
		print(f"{greeting} User!")

	argument = main.params[0]
	assert argument.default == "Hello"
	assert not argument.required

	result = cli_runner.invoke(main)
	assert result.stdout.rstrip() == "Hello User!"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args=["Good Morning"])
	assert result.stdout.rstrip() == "Good Morning User!"
	assert result.exit_code == 0
