# stdlib
from collections import deque

# 3rd party
from coincidence import check_file_regression
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from consolekit import terminal_colours
from consolekit.terminal_colours import Colour, print_256_colour_testpattern, strip_ansi


def test_terminal_colours_constants():
	assert terminal_colours.CSI == "\u001b["
	assert terminal_colours.OSC == "\u001b]"
	assert terminal_colours.BEL == '\x07'


def test_terminal_colours_stacks():
	assert terminal_colours.fore_stack == deque([terminal_colours.Fore.RESET])
	assert terminal_colours.back_stack == deque([terminal_colours.Back.RESET])
	assert terminal_colours.style_stack == deque([terminal_colours.Style.NORMAL])


def test_terminal_colours_functions():
	assert terminal_colours.set_title("Foo") == "\u001b]2;Foo\u0007"

	# assert terminal_colours.clear_screen() == "\033[2J"
	# assert terminal_colours.clear_screen(1) == "\033[1J"

	assert terminal_colours.clear_line() == "\u001b[2K"
	assert terminal_colours.clear_line(1) == "\u001b[1K"


def test_ansi_cursor():
	assert terminal_colours.Cursor.UP() == "\u001b[1A"
	assert terminal_colours.Cursor.UP(1) == "\u001b[1A"
	assert terminal_colours.Cursor.UP(2) == "\u001b[2A"
	assert terminal_colours.Cursor.UP(3) == "\u001b[3A"

	assert terminal_colours.Cursor.DOWN() == "\u001b[1B"
	assert terminal_colours.Cursor.DOWN(1) == "\u001b[1B"
	assert terminal_colours.Cursor.DOWN(2) == "\u001b[2B"
	assert terminal_colours.Cursor.DOWN(3) == "\u001b[3B"

	assert terminal_colours.Cursor.FORWARD() == "\u001b[1C"
	assert terminal_colours.Cursor.FORWARD(1) == "\u001b[1C"
	assert terminal_colours.Cursor.FORWARD(2) == "\u001b[2C"
	assert terminal_colours.Cursor.FORWARD(3) == "\u001b[3C"

	assert terminal_colours.Cursor.BACK() == "\u001b[1D"
	assert terminal_colours.Cursor.BACK(1) == "\u001b[1D"
	assert terminal_colours.Cursor.BACK(2) == "\u001b[2D"
	assert terminal_colours.Cursor.BACK(3) == "\u001b[3D"

	assert terminal_colours.Cursor.POS() == "\u001b[1;1H"
	assert terminal_colours.Cursor.POS(1) == "\u001b[1;1H"
	assert terminal_colours.Cursor.POS(2) == "\u001b[1;2H"
	assert terminal_colours.Cursor.POS(3) == "\u001b[1;3H"
	assert terminal_colours.Cursor.POS(y=1) == "\u001b[1;1H"
	assert terminal_colours.Cursor.POS(y=2) == "\u001b[2;1H"
	assert terminal_colours.Cursor.POS(y=3) == "\u001b[3;1H"
	assert terminal_colours.Cursor.POS(x=1) == "\u001b[1;1H"
	assert terminal_colours.Cursor.POS(x=2) == "\u001b[1;2H"
	assert terminal_colours.Cursor.POS(x=3) == "\u001b[1;3H"
	assert terminal_colours.Cursor.POS(1, 1) == "\u001b[1;1H"
	assert terminal_colours.Cursor.POS(2, 2) == "\u001b[2;2H"
	assert terminal_colours.Cursor.POS(3, 3) == "\u001b[3;3H"
	assert terminal_colours.Cursor.POS(x=2, y=3) == "\u001b[3;2H"


class TestColour:

	def test_from_code(self):
		black = Colour.from_code(30)
		assert black == "\u001b[30m"
		assert black("Hello") == "\u001b[30mHello\u001b[39m"

		black = Colour.from_code(40, background=True)
		assert black == "\u001b[40m"
		assert black("Hello") == "\u001b[40mHello\u001b[49m"

	def test_from_rgb(self):
		yellow = Colour.from_rgb(252, 186, 3)
		assert yellow == "\u001b[38;2;252;186;3m"
		assert yellow("Hello") == "\u001b[38;2;252;186;3mHello\u001b[39m"

		yellow = Colour.from_rgb(252, 186, 3, background=True)
		assert yellow == "\u001b[48;2;252;186;3m"
		assert yellow("Hello") == "\u001b[48;2;252;186;3mHello\u001b[49m"

	def test_from_hex(self):
		yellow = Colour.from_hex("#fcba03")
		assert yellow == "\u001b[38;2;252;186;3m"
		assert yellow("Hello") == "\u001b[38;2;252;186;3mHello\u001b[39m"

		yellow = Colour.from_hex("#fcba03", background=True)
		assert yellow == "\u001b[48;2;252;186;3m"
		assert yellow("Hello") == "\u001b[48;2;252;186;3mHello\u001b[49m"


def test_print_256_colour_testpattern(
		monkeypatch,
		file_regression: FileRegressionFixture,
		capsys,
		):
	monkeypatch.setattr(terminal_colours, "resolve_color_default", lambda *args: False)

	# Checks only the structure, not the colours
	print_256_colour_testpattern()

	check_file_regression(strip_ansi(capsys.readouterr().out.strip()), file_regression)
