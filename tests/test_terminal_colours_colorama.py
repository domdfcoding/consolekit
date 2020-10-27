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
from colorama.ansitowin32 import AnsiToWin32  # type: ignore

# this package
from domdf_python_tools.terminal_colours import Back, Fore, Style

stdout_orig = sys.stdout
stderr_orig = sys.stderr


def setup_module():
	# sanity check: stdout should be a file or StringIO object.
	# It will only be AnsiToWin32 if init() has previously wrapped it
	assert not isinstance(sys.stdout, AnsiToWin32)
	assert not isinstance(sys.stderr, AnsiToWin32)


def teardown_module():
	sys.stdout = stdout_orig
	sys.stderr = stderr_orig


@pytest.mark.parametrize(
		"obj, expects",
		[
				(Fore.BLACK, "\033[30m"),
				(Fore.RED, "\033[31m"),
				(Fore.GREEN, "\033[32m"),
				(Fore.YELLOW, "\033[33m"),
				(Fore.BLUE, "\033[34m"),
				(Fore.MAGENTA, "\033[35m"),
				(Fore.CYAN, "\033[36m"),
				(Fore.WHITE, "\033[37m"),
				(Fore.RESET, "\033[39m"),

				# Check the light, extended versions.
				(Fore.LIGHTBLACK_EX, "\033[90m"),
				(Fore.LIGHTRED_EX, "\033[91m"),
				(Fore.LIGHTGREEN_EX, "\033[92m"),
				(Fore.LIGHTYELLOW_EX, "\033[93m"),
				(Fore.LIGHTBLUE_EX, "\033[94m"),
				(Fore.LIGHTMAGENTA_EX, "\033[95m"),
				(Fore.LIGHTCYAN_EX, "\033[96m"),
				(Fore.LIGHTWHITE_EX, "\033[97m"),
				],
		)
def test_fore_attributes(obj, expects, capsys):
	assert obj == expects
	assert obj("Hello World") == f"{obj}Hello World\033[39m"

	with obj:
		print("Hello World!")
		with Fore.RESET:
			print("Reset!")
		print("Coloured Again!")
	print("Reset Again!")

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout[0] == f"{obj}Hello World!"
	assert stdout[1] == f"\033[39mReset!"
	assert stdout[2] == f"{obj}Coloured Again!"
	assert stdout[3] == f"\033[39mReset Again!"
	assert stdout[4] == ''


@pytest.mark.parametrize(
		"obj, expects",
		[
				(Back.BLACK, "\033[40m"),
				(Back.RED, "\033[41m"),
				(Back.GREEN, "\033[42m"),
				(Back.YELLOW, "\033[43m"),
				(Back.BLUE, "\033[44m"),
				(Back.MAGENTA, "\033[45m"),
				(Back.CYAN, "\033[46m"),
				(Back.WHITE, "\033[47m"),
				(Back.RESET, "\033[49m"),

				# Check the light, extended versions.
				(Back.LIGHTBLACK_EX, "\033[100m"),
				(Back.LIGHTRED_EX, "\033[101m"),
				(Back.LIGHTGREEN_EX, "\033[102m"),
				(Back.LIGHTYELLOW_EX, "\033[103m"),
				(Back.LIGHTBLUE_EX, "\033[104m"),
				(Back.LIGHTMAGENTA_EX, "\033[105m"),
				(Back.LIGHTCYAN_EX, "\033[106m"),
				(Back.LIGHTWHITE_EX, "\033[107m"),
				],
		)
def test_back_attributes(obj, expects, capsys):
	assert obj == expects
	assert obj("Hello World") == f"{obj}Hello World\033[49m"

	with obj:
		print("Hello World!")
		with Back.RESET:
			print("Reset!")
		print("Coloured Again!")
	print("Reset Again!")

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout[0] == f"{obj}Hello World!"
	assert stdout[1] == f"\033[49mReset!"
	assert stdout[2] == f"{obj}Coloured Again!"
	assert stdout[3] == f"\033[49mReset Again!"
	assert stdout[4] == ''


@pytest.mark.parametrize(
		"obj, expects",
		[
				(Style.DIM, "\033[2m"),
				(Style.NORMAL, "\033[22m"),
				(Style.BRIGHT, "\033[1m"),
				],
		)
def test_style_attributes(obj, expects, capsys):
	assert obj == expects
	assert obj("Hello World") == f"{obj}Hello World\033[22m"

	with obj:
		print("Hello World!")
		with Style.NORMAL:
			print("Reset!")
		print("Coloured Again!")
	print("Reset Again!")

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout[0] == f"{obj}Hello World!"
	assert stdout[1] == f"\033[22mReset!"
	assert stdout[2] == f"{obj}Coloured Again!"
	assert stdout[3] == f"\033[22mReset Again!"
	assert stdout[4] == ''
