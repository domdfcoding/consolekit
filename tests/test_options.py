# stdlib
import sys
from typing import Iterable

# 3rd party
import click
from click.testing import CliRunner, Result
from domdf_python_tools.testing import check_file_regression
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from consolekit import click_command
from consolekit.options import (
		MultiValueOption,
		auto_default_option,
		colour_option,
		flag_option,
		force_option,
		no_pager_option,
		verbose_option,
		version_option
		)
from consolekit.terminal_colours import ColourTrilean


def test_auto_default_option(file_regression: FileRegressionFixture):

	@auto_default_option("--width", type=click.INT, help="The max width to display.", show_default=True)
	@click_command()
	def main(width: int = 80):
		print(width)

	runner = CliRunner()

	result: Result = runner.invoke(main, catch_exceptions=False, args="--help")
	check_file_regression(result.stdout.rstrip(), file_regression, extension=".md")
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False)
	assert result.stdout.rstrip() == "80"
	assert result.exit_code == 0

	for width in [0, 8, 36, 48, 130]:

		result = runner.invoke(main, catch_exceptions=False, args=["--width", str(width)])
		assert result.stdout.rstrip() == str(width)
		assert result.exit_code == 0


def test_flag_option():

	@flag_option("--no-colour")
	@click_command()
	def main(no_colour: bool):
		print(no_colour)

	runner = CliRunner()

	result: Result = runner.invoke(main, catch_exceptions=False)
	assert result.stdout.rstrip() == "False"
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args="--no-colour")
	assert result.stdout.rstrip() == "True"
	assert result.exit_code == 0


def test_no_pager_option(file_regression: FileRegressionFixture):

	@no_pager_option()
	@click_command()
	def main(no_pager: bool):
		print(no_pager)

	runner = CliRunner()

	result: Result = runner.invoke(main, catch_exceptions=False)
	assert result.stdout.rstrip() == "False"
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args="--no-pager")
	assert result.stdout.rstrip() == "True"
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args="-h")
	check_file_regression(result.stdout.rstrip(), file_regression)
	assert result.exit_code == 0


def test_force_option(file_regression: FileRegressionFixture):

	@force_option("Force the operation")
	@click_command()
	def main(force: bool):
		print(force)

	runner = CliRunner()

	result: Result = runner.invoke(main, catch_exceptions=False)
	assert result.stdout.rstrip() == "False"
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args="--force")
	assert result.stdout.rstrip() == "True"
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args="-f")
	assert result.stdout.rstrip() == "True"
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args="-h")
	check_file_regression(result.stdout.rstrip(), file_regression)
	assert result.exit_code == 0


def test_verbose_option(file_regression: FileRegressionFixture):

	@verbose_option("Force the operation")
	@click_command()
	def main(verbose: int):
		print(verbose)

	runner = CliRunner()

	result: Result = runner.invoke(main, catch_exceptions=False)
	assert result.stdout.rstrip() == '0'
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args="--verbose")
	assert result.stdout.rstrip() == '1'
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args="-v")
	assert result.stdout.rstrip() == '1'
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args=["--verbose", "--verbose"])
	assert result.stdout.rstrip() == '2'
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args="-vv")
	assert result.stdout.rstrip() == '2'
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args="-vvv")
	assert result.stdout.rstrip() == '3'
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args="-h")
	check_file_regression(result.stdout.rstrip(), file_regression)
	assert result.exit_code == 0


def test_colour_option(file_regression: FileRegressionFixture):

	@colour_option()
	@click_command()
	def main(colour: ColourTrilean):
		print(colour)

	runner = CliRunner()

	result: Result = runner.invoke(main, catch_exceptions=False)
	assert result.stdout.rstrip() == "None"
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args="--no-colour")
	assert result.stdout.rstrip() == "False"
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args="--colour")
	assert result.stdout.rstrip() == "True"
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args="-h")
	check_file_regression(result.stdout.rstrip(), file_regression)
	assert result.exit_code == 0


def test_version_option(file_regression: FileRegressionFixture):

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

	runner = CliRunner()

	result = runner.invoke(main, catch_exceptions=False, args="--version")
	assert result.stdout.rstrip() == "consolekit version 1.2.3"
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args=["--version", "--version"])
	assert result.stdout.rstrip() == "consolekit version 1.2.3, Python 3.8.5"
	assert result.exit_code == 0


def test_multi_value_option(file_regression: FileRegressionFixture):

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

	runner = CliRunner()

	result: Result = runner.invoke(main, catch_exceptions=False)
	assert result.stdout.rstrip() == ''
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args=["--select", "E102", "F223"])
	assert result.stdout.rstrip() == "E102 F223\nE102, F223"
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args=["--select", "E102", "F223", "--colour"])
	assert result.stdout.rstrip() == "E102 F223\nE102, F223"
	assert result.exit_code == 0

	result = runner.invoke(main, catch_exceptions=False, args=["--select", "E102"])
	assert result.stdout.rstrip() == "E102\nE102"
	assert result.exit_code == 0
