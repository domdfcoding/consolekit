# From https://github.com/tartley/colorama
# Copyright Jonathan Hartley 2013
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holders, nor those of its contributors
#   may be used to endorse or promote products derived from this software without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# stdlib
import sys

# 3rd party
import pytest

# this package
from consolekit.terminal_colours import Back, Colour, Fore, Style

stdout_orig = sys.stdout
stderr_orig = sys.stderr

colorama = pytest.importorskip("colorama")
AnsiToWin32 = colorama.ansitowin32.AnsiToWin32


def setup_module() -> None:
	# sanity check: stdout should be a file or StringIO object.
	# It will only be AnsiToWin32 if init() has previously wrapped it
	assert not isinstance(sys.stdout, AnsiToWin32)
	assert not isinstance(sys.stderr, AnsiToWin32)


def teardown_module() -> None:
	sys.stdout = stdout_orig
	sys.stderr = stderr_orig


@pytest.mark.parametrize(
		"obj, expects",
		[
				(Fore.BLACK, "\u001b[30m"),
				(Fore.RED, "\u001b[31m"),
				(Fore.GREEN, "\u001b[32m"),
				(Fore.YELLOW, "\u001b[33m"),
				(Fore.BLUE, "\u001b[34m"),
				(Fore.MAGENTA, "\u001b[35m"),
				(Fore.CYAN, "\u001b[36m"),
				(Fore.WHITE, "\u001b[37m"),
				(Fore.RESET, "\u001b[39m"),

				# Check the light, extended versions.
				(Fore.LIGHTBLACK_EX, "\u001b[90m"),
				(Fore.LIGHTRED_EX, "\u001b[91m"),
				(Fore.LIGHTGREEN_EX, "\u001b[92m"),
				(Fore.LIGHTYELLOW_EX, "\u001b[93m"),
				(Fore.LIGHTBLUE_EX, "\u001b[94m"),
				(Fore.LIGHTMAGENTA_EX, "\u001b[95m"),
				(Fore.LIGHTCYAN_EX, "\u001b[96m"),
				(Fore.LIGHTWHITE_EX, "\u001b[97m"),
				],
		)
def test_fore_attributes(obj: Colour, expects: str, capsys):
	assert obj == expects
	assert obj("Hello World") == f"{obj}Hello World\033[39m"

	with obj:
		print("Hello World!")
		with Fore.RESET:
			print("Reset!")
		print("Coloured Again!")
	print("Reset Again!")

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout[0] == f"{obj}Hello World!"
	assert stdout[1] == "\u001b[39mReset!"
	assert stdout[2] == f"{obj}Coloured Again!"
	assert stdout[3] == "\u001b[39mReset Again!"
	assert stdout[4] == ''


@pytest.mark.parametrize(
		"obj, expects",
		[
				(Back.BLACK, "\u001b[40m"),
				(Back.RED, "\u001b[41m"),
				(Back.GREEN, "\u001b[42m"),
				(Back.YELLOW, "\u001b[43m"),
				(Back.BLUE, "\u001b[44m"),
				(Back.MAGENTA, "\u001b[45m"),
				(Back.CYAN, "\u001b[46m"),
				(Back.WHITE, "\u001b[47m"),
				(Back.RESET, "\u001b[49m"),

				# Check the light, extended versions.
				(Back.LIGHTBLACK_EX, "\u001b[100m"),
				(Back.LIGHTRED_EX, "\u001b[101m"),
				(Back.LIGHTGREEN_EX, "\u001b[102m"),
				(Back.LIGHTYELLOW_EX, "\u001b[103m"),
				(Back.LIGHTBLUE_EX, "\u001b[104m"),
				(Back.LIGHTMAGENTA_EX, "\u001b[105m"),
				(Back.LIGHTCYAN_EX, "\u001b[106m"),
				(Back.LIGHTWHITE_EX, "\u001b[107m"),
				],
		)
def test_back_attributes(obj: Colour, expects: str, capsys):
	assert obj == expects
	assert obj("Hello World") == f"{obj}Hello World\033[49m"

	with obj:
		print("Hello World!")
		with Back.RESET:
			print("Reset!")
		print("Coloured Again!")
	print("Reset Again!")

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout[0] == f"{obj}Hello World!"
	assert stdout[1] == "\u001b[49mReset!"
	assert stdout[2] == f"{obj}Coloured Again!"
	assert stdout[3] == "\u001b[49mReset Again!"
	assert stdout[4] == ''


@pytest.mark.parametrize(
		"obj, expects",
		[
				(Style.DIM, "\u001b[2m"),
				(Style.NORMAL, "\u001b[22m"),
				(Style.BRIGHT, "\u001b[1m"),
				],
		)
def test_style_attributes(obj: Colour, expects: str, capsys):
	assert obj == expects
	assert obj("Hello World") == f"{obj}Hello World\033[22m"

	with obj:
		print("Hello World!")
		with Style.NORMAL:
			print("Reset!")
		print("Coloured Again!")
	print("Reset Again!")

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout[0] == f"{obj}Hello World!"
	assert stdout[1] == "\u001b[22mReset!"
	assert stdout[2] == f"{obj}Coloured Again!"
	assert stdout[3] == "\u001b[22mReset Again!"
	assert stdout[4] == ''
