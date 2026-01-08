# stdlib
import sys

# this package
from consolekit import click_command
from consolekit.options import version_option
from consolekit.testing import CliRunner
from consolekit.versions import get_formatted_versions, get_version_callback, version_callback_option


def test_get_formatted_versions():
	dependencies = ["click", "deprecation-alias", "domdf-python-tools", "mistletoe", "typing-extensions"]

	sl = get_formatted_versions(dependencies)
	for line, dep in zip(sl, dependencies):
		assert line.startswith(f"{dep}:")
	assert sl[-2].startswith("Python: 3.")

	sl = get_formatted_versions(dependencies, show_platform=False)
	for line, dep in zip(sl, [*dependencies]):
		assert line.startswith(f"{dep}:")
	assert sl[-1].startswith("Python: 3.")

	sl = get_formatted_versions(dependencies, show_python=False)
	assert len(sl) == len(dependencies) + 1

	sl = get_formatted_versions(dependencies, show_python=False, show_platform=False)
	assert len(sl) == len(dependencies)

	sl = get_formatted_versions({
			"click": "pkg1",
			"deprecation-alias": "pkg2",
			"domdf-python-tools": "pkg3",
			"mistletoe": "pkg4",
			"typing-extensions": "pkg5",
			})
	for line, name in zip(sl, ["pkg1", "pkg2", "pkg3", "pkg4", "pkg5"]):
		assert line.startswith(f"{name}:")
	assert sl[-2].startswith("Python: 3.")


def test_version_callback(cli_runner: CliRunner):

	@version_option(
			get_version_callback(
					"1.2.3",
					"my-tool",
					["click", "deprecation-alias", "domdf-python-tools", "mistletoe", "typing-extensions"],
					),
			)
	@click_command()
	def main() -> None:
		sys.exit(1)

	result = cli_runner.invoke(main, args="--version")
	assert result.stdout.rstrip() == "my-tool version 1.2.3"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args=["--version", "--version"])
	assert result.stdout.startswith("my-tool version 1.2.3, Python 3.")
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args=["--version", "--version", "--version"])
	print(result.stdout)
	assert result.stdout.startswith("my-tool\n  Version: 1.2.3\n  click: ")
	assert result.exit_code == 0


def test_version_callback_option(cli_runner: CliRunner):

	@version_callback_option(
			"1.2.3",
			"my-tool",
			["click", "deprecation-alias", "domdf-python-tools", "mistletoe", "typing-extensions"],
			)
	@click_command()
	def main() -> None:
		sys.exit(1)

	result = cli_runner.invoke(main, args="--version")
	assert result.stdout.rstrip() == "my-tool version 1.2.3"
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args=["--version", "--version"])
	assert result.stdout.startswith("my-tool version 1.2.3, Python 3.")
	assert result.exit_code == 0

	result = cli_runner.invoke(main, args=["--version", "--version", "--version"])
	print(result.stdout)
	assert result.stdout.startswith("my-tool\n  Version: 1.2.3\n  click: ")
	assert result.exit_code == 0
