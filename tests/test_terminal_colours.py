from consolekit import terminal_colours


def test_terminal_colours_constants():
	assert terminal_colours.CSI == "\033["
	assert terminal_colours.OSC == "\033]"
	assert terminal_colours.BEL == "\a"


def test_terminal_colours_stacks():
	assert terminal_colours.fore_stack == [terminal_colours.Fore.RESET]
	assert terminal_colours.back_stack == [terminal_colours.Back.RESET]
	assert terminal_colours.style_stack == [terminal_colours.Style.NORMAL]


def test_terminal_colours_functions():
	assert terminal_colours.set_title("Foo") == "\033]2;Foo\a"

	assert terminal_colours.clear_screen() == "\033[2J"
	assert terminal_colours.clear_screen(1) == "\033[1J"

	assert terminal_colours.clear_line() == "\033[2K"
	assert terminal_colours.clear_line(1) == "\033[1K"


def test_ansi_cursor():
	assert terminal_colours.Cursor.UP() == "\033[1A"
	assert terminal_colours.Cursor.UP(1) == "\033[1A"
	assert terminal_colours.Cursor.UP(2) == "\033[2A"
	assert terminal_colours.Cursor.UP(3) == "\033[3A"

	assert terminal_colours.Cursor.DOWN() == "\033[1B"
	assert terminal_colours.Cursor.DOWN(1) == "\033[1B"
	assert terminal_colours.Cursor.DOWN(2) == "\033[2B"
	assert terminal_colours.Cursor.DOWN(3) == "\033[3B"

	assert terminal_colours.Cursor.FORWARD() == "\033[1C"
	assert terminal_colours.Cursor.FORWARD(1) == "\033[1C"
	assert terminal_colours.Cursor.FORWARD(2) == "\033[2C"
	assert terminal_colours.Cursor.FORWARD(3) == "\033[3C"

	assert terminal_colours.Cursor.BACK() == "\033[1D"
	assert terminal_colours.Cursor.BACK(1) == "\033[1D"
	assert terminal_colours.Cursor.BACK(2) == "\033[2D"
	assert terminal_colours.Cursor.BACK(3) == "\033[3D"

	assert terminal_colours.Cursor.POS() == "\033[1;1H"
	assert terminal_colours.Cursor.POS(1) == "\033[1;1H"
	assert terminal_colours.Cursor.POS(2) == "\033[1;2H"
	assert terminal_colours.Cursor.POS(3) == "\033[1;3H"
	assert terminal_colours.Cursor.POS(y=1) == "\033[1;1H"
	assert terminal_colours.Cursor.POS(y=2) == "\033[2;1H"
	assert terminal_colours.Cursor.POS(y=3) == "\033[3;1H"
	assert terminal_colours.Cursor.POS(x=1) == "\033[1;1H"
	assert terminal_colours.Cursor.POS(x=2) == "\033[1;2H"
	assert terminal_colours.Cursor.POS(x=3) == "\033[1;3H"
	assert terminal_colours.Cursor.POS(1, 1) == "\033[1;1H"
	assert terminal_colours.Cursor.POS(2, 2) == "\033[2;2H"
	assert terminal_colours.Cursor.POS(3, 3) == "\033[3;3H"
	assert terminal_colours.Cursor.POS(x=2, y=3) == "\033[3;2H"
