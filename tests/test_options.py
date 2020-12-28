# stdlib
from typing import Optional

# 3rd party
import click
from click.testing import CliRunner, Result
from domdf_python_tools.testing import check_file_regression
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from consolekit import click_command
from consolekit.options import (
		auto_default_option,
		colour_option,
		flag_option,
		force_option,
		no_pager_option,
		verbose_option
		)


def test_auto_default_option():

	@auto_default_option("--width", type=click.INT)
	@click_command()
	def main(width: int = 80):
		print(width)

	runner = CliRunner()

	result: Result = runner.invoke(main, catch_exceptions=False)
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
	def main(colour: Optional[bool]):
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
