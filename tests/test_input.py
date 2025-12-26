# stdlib
from typing import Type

# 3rd party
import click
import pytest
from click import echo
from coincidence.regressions import AdvancedDataRegressionFixture
from domdf_python_tools.stringlist import StringList

# this package
from consolekit.input import choice, confirm, prompt
from consolekit.testing import _click_version


def test_choice_letters(
		capsys,
		monkeypatch,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	inputs = iter(['F', 'G', 'D'])

	def fake_input(prompt: str) -> str:
		value = next(inputs)
		print(f"{prompt}{value}".rstrip())
		return value

	monkeypatch.setattr(click.termui, "visible_prompt_func", fake_input)

	echo("Configuration file '/etc/sudoers'")
	echo("==> Modified (by you or by a script) since installation.")
	echo("==> Package distributor has shipped an updated version.")
	echo("What would you like to do about it ?  Your options are:")
	options = {
			'Y': "install the package maintainer's version",
			'N': "keep your currently-installed version",
			'D': "show the differences between the versions",
			'Z': "start a shell to examine the situation",
			}
	assert choice(text="*** sudoers", options=options, default='N') == 'D'

	advanced_data_regression.check(list(StringList(capsys.readouterr().out.splitlines())))


@pytest.mark.parametrize(
		"click_version",
		[
				pytest.param(
						'7',
						marks=pytest.mark.skipif(_click_version[0] == 8, reason="Output differs on click 8"),
						),
				pytest.param(
						'8',
						marks=pytest.mark.skipif(_click_version[0] != 8, reason="Output differs on click 8"),
						),
				]
		)
def test_choice_numbers(
		capsys,
		monkeypatch,
		advanced_data_regression: AdvancedDataRegressionFixture,
		click_version: str,
		):

	inputs = iter(["20", '0', '5'])

	def fake_input(prompt: str) -> str:
		value = next(inputs)
		print(f"{prompt}{value}".rstrip())
		return value

	monkeypatch.setattr(click.termui, "visible_prompt_func", fake_input)

	echo("What is the Development Status of this project?")
	options = [
			"Planning",
			"Pre-Alpha",
			"Alpha",
			"Beta",
			"Production/Stable",
			"Mature",
			"Inactive",
			]
	assert choice(text='', options=options, start_index=1) == 4

	advanced_data_regression.check(list(StringList(capsys.readouterr().out.splitlines())))


def test_confirm(
		capsys,
		monkeypatch,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	inputs = iter(['Y', 'N', '', '', "yEs", "No", "gkjhkhjv", ''])

	def fake_input(prompt: str) -> str:
		value = next(inputs)
		print(f"{prompt}{value}".rstrip())
		return value

	monkeypatch.setattr(click.termui, "visible_prompt_func", fake_input)

	assert confirm(text="Do you wish to delete all files in '/' ?", default=False) is True
	assert confirm(text="Do you wish to delete all files in '/' ?", default=False) is False
	assert confirm(text="Do you wish to delete all files in '/' ?", default=False) is False
	assert confirm(text="Do you wish to delete all files in '/' ?", default=True) is True
	assert confirm(text="Do you wish to delete all files in '/' ?", default=False) is True
	assert confirm(text="Do you wish to delete all files in '/' ?", default=True) is False
	assert confirm(text="Do you wish to delete all files in '/' ?", default=True) is True

	advanced_data_regression.check(list(StringList(capsys.readouterr().out.splitlines())))


def test_prompt(
		capsys,
		monkeypatch,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	inputs = iter([
			'',
			'',
			'',
			'',
			"24",
			"Bond007",
			"badpassword",
			"baspassword",
			"badpassword",
			"badpassword",
			"badpassword",
			"badpassword",
			])

	def fake_input(prompt: str) -> str:
		value = next(inputs)
		print(f"{prompt}{value}".rstrip())
		return value

	monkeypatch.setattr(click.termui, "visible_prompt_func", fake_input)

	assert prompt(text="What is your age", prompt_suffix="? ", type=click.INT) == 24

	assert prompt(text="Username", type=click.STRING) == "Bond007"
	assert prompt(text="Password", type=click.STRING, confirmation_prompt=True) == "badpassword"
	assert prompt(
			text="Password",
			type=click.STRING,
			confirmation_prompt="Are you sure about that? ",
			) == "badpassword"

	advanced_data_regression.check(list(StringList(capsys.readouterr().out.splitlines())))


@pytest.mark.parametrize("exception", [KeyboardInterrupt, EOFError])
def test_prompt_abort(
		capsys,
		monkeypatch,
		advanced_data_regression: AdvancedDataRegressionFixture,
		exception: Type[Exception],
		):

	def fake_input(prompt: str) -> str:
		print(f"{prompt}", end='')
		raise exception

	monkeypatch.setattr(click.termui, "visible_prompt_func", fake_input)

	with pytest.raises(click.Abort, match="^$"):
		prompt(text="Password", type=click.STRING, confirmation_prompt=True)

	assert list(StringList(capsys.readouterr().out.splitlines())) == ["Password:"]


@pytest.mark.parametrize("exception", [KeyboardInterrupt, EOFError])
def test_confirm_abort(
		capsys,
		monkeypatch,
		advanced_data_regression: AdvancedDataRegressionFixture,
		exception: Type[Exception],
		):

	def fake_input(prompt: str) -> str:
		print(f"{prompt}", end='')
		raise exception

	monkeypatch.setattr(click.termui, "visible_prompt_func", fake_input)

	with pytest.raises(click.Abort, match="^$"):
		confirm(text="Do you wish to delete all files in '/' ?", default=False)

	expected = ["Do you wish to delete all files in '/' ? [y/N]:"]
	assert list(StringList(capsys.readouterr().out.splitlines())) == expected
