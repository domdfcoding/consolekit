# stdlib
from collections import deque

# this package
from consolekit import terminal_colours


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
