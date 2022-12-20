# stdlib
import sys
from typing import Iterable

# 3rd party
import click

# this package
from consolekit import click_command
from consolekit.options import DescribedArgument
from consolekit.testing import CliRunner


def test_result(cli_runner: CliRunner):

	@click.argument(
			"dest",
			cls=DescribedArgument,
			type=click.STRING,
			description="The destination directory.",
			)
	@click_command()
	def main(dest: str) -> None:
		print(dest)

	result = cli_runner.invoke(main, catch_exceptions=False, args="./staging")
	assert result.stdout.rstrip() == "./staging"
	assert result.output.rstrip() == "./staging"
	assert result.exit_code == 0


def test_result_no_mix_stderr():

	cli_runner = CliRunner(mix_stderr=False)

	@click.argument(
			"dest",
			cls=DescribedArgument,
			type=click.STRING,
			description="The destination directory.",
			)
	@click_command()
	def main(dest: str) -> None:
		print(dest)

	result = cli_runner.invoke(main, catch_exceptions=False, args="./staging")
	assert result.stdout.rstrip() == "./staging"
	assert result.stderr == ''
	assert result.output.rstrip() == "./staging"
	assert result.exit_code == 0
