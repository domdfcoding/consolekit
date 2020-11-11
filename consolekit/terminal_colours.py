#!/usr/bin/env python
#
#  terminal_colours.py
"""
Functions for adding colours to terminal print statements.

This module generates ANSI character codes to printing colors to terminals.
See: http://en.wikipedia.org/wiki/ANSI_escape_code
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#
#  Based on colorama
#  https://github.com/tartley/colorama
#  Copyright Jonathan Hartley 2013
#  Distributed under the BSD 3-Clause license.
#  |  Redistribution and use in source and binary forms, with or without
#  |  modification, are permitted provided that the following conditions are met:
#  |
#  |  * Redistributions of source code must retain the above copyright notice, this
#  |    list of conditions and the following disclaimer.
#  |
#  |  * Redistributions in binary form must reproduce the above copyright notice,
#  |    this list of conditions and the following disclaimer in the documentation
#  |    and/or other materials provided with the distribution.
#  |
#  |  * Neither the name of the copyright holders, nor those of its contributors
#  |    may be used to endorse or promote products derived from this software without
#  |    specific prior written permission.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  |  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  |  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  |  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#  |  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  |  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  |  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  |  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  |  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  |  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  Includes modifications to colorama made by Bram Geelen in
#  https://github.com/tartley/colorama/pull/141/files
#
#  resolve_color_default, _ansi_re and strip_ansi based on
#  https://github.com/pallets/click
#  Copyright 2014 Pallets
#  Distributed under the BSD 3-Clause license.
#

# stdlib
import os
import re
from abc import ABC
from typing import List, Optional, Pattern

# 3rd party
import click
from colorama import init  # type: ignore
from typing_extensions import Final

__all__ = [
		"CSI",
		"OSC",
		"BEL",
		"resolve_color_default",
		"code_to_chars",
		"set_title",
		"clear_line",
		"Colour",
		"AnsiCodes",
		"AnsiCursor",
		"AnsiFore",
		"AnsiBack",
		"AnsiStyle",
		"Fore",
		"Back",
		"Style",
		"Cursor",
		"strip_ansi",
		]

init()

CSI: Final[str] = "\u001b["
OSC: Final[str] = "\u001b]"
BEL: Final[str] = '\x07'

fore_stack: List[str] = []
back_stack: List[str] = []
style_stack: List[str] = []


def resolve_color_default(color: Optional[bool] = None) -> Optional[bool]:
	"""
	Internal helper to get the default value of the color flag. If a
	value is passed it's returned unchanged, otherwise it's looked up from
	the current context.

	If the environment variable ``PYCHARM_HOSTED`` is 1
	(which is the case if running in PyCharm)
	the output will be coloured by default.

	:param color:
	"""  # noqa: D400

	if color is not None:
		return color

	ctx = click.get_current_context(silent=True)

	if ctx is not None:
		return ctx.color

	if os.environ.get("PYCHARM_HOSTED", 0):
		return True

	return None


def code_to_chars(code) -> str:
	return CSI + str(code) + 'm'


def set_title(title: str) -> str:
	return OSC + "2;" + title + BEL


#
# def clear_screen(mode: int = 2) -> str:
# 	return CSI + str(mode) + 'J'


def clear_line(mode: int = 2) -> str:
	return CSI + str(mode) + 'K'


_ansi_re: Pattern[str] = re.compile(r"\033\[[;?0-9]*[a-zA-Z]")


def strip_ansi(value: str) -> str:
	"""
	Strip ANSI colour codes from the given string to return a plaintext output.

	:param value:

	:rtype:

	.. versionadded:: 1.1.0
	"""

	return _ansi_re.sub('', value)


class Colour(str):
	r"""
	An ANSI escape sequence representing a colour.

	The colour can be used as a context manager, a string, or a function.

	:param style: Escape sequence representing the style.
	:type style: :class:`str`
	:param stack: The stack to place the escape sequence on.
	:type stack: :class:`~typing.List`\[:class:`str`\]
	:param reset: The escape sequence to reset the style.
	:type reset: :class:`str`
	"""

	style: str
	reset: str
	stack: List[str]

	def __new__(cls, style: str, stack: List[str], reset: str) -> "Colour":  # noqa D102
		color = super().__new__(cls, style)  # type: ignore
		color.style = style
		color.stack = stack
		color.reset = reset

		return color

	def __enter__(self) -> None:
		print(self.style, end='')
		self.stack.append(self.style)

	def __exit__(self, exc_type, exc_val, exc_tb) -> None:
		if self.style == self.stack[-1]:
			self.stack.pop()
			print(self.stack[-1], end='')

	def __call__(self, text) -> str:
		"""
		Returns the given text in this colour.
		"""

		return f"{self}{text}{self.reset}"


class AnsiCodes(ABC):
	"""
	Abstract base class for ANSI Codes.
	"""

	_stack: List[str]
	_reset: str

	def __init__(self) -> None:
		"""
		The subclasses declare class attributes which are numbers.

		Upon instantiation we define instance attributes, which are the same
		as the class attributes but wrapped with the ANSI escape sequence.
		"""

		for name in dir(self):
			if not name.startswith('_'):
				value = getattr(self, name)
				setattr(self, name, Colour(code_to_chars(value), self._stack, self._reset))


class AnsiCursor:

	def UP(self, n: int = 1) -> str:
		"""
		Move the cursor up ``n`` lines.

		:param n:
		"""

		return f"{CSI}{str(n)}A"

	def DOWN(self, n: int = 1) -> str:
		"""
		Move the cursor down ``n`` lines.

		:param n:
		"""

		return f"{CSI}{str(n)}B"

	def FORWARD(self, n: int = 1) -> str:
		"""
		Move the cursor forward ``n`` lines.

		:param n:
		"""

		return f"{CSI}{str(n)}C"

	def BACK(self, n: int = 1) -> str:
		"""
		Move the cursor backward ``n`` lines.

		:param n:
		"""

		return f"{CSI}{str(n)}D"

	def POS(self, x: int = 1, y: int = 1) -> str:
		"""
		Move the cursor to the given position.

		:param x:
		:param y:
		"""

		return f"{CSI}{str(y)};{str(x)}H"


class AnsiFore(AnsiCodes):
	"""
	ANSI Colour Codes for foreground colour.

	The colours can be used as a context manager, a string, or a function.

	Valid values are:

	* BLACK
	* RED
	* GREEN
	* YELLOW
	* BLUE
	* MAGENTA
	* CYAN
	* WHITE
	* RESET
	* LIGHTBLACK_EX
	* LIGHTRED_EX
	* LIGHTGREEN_EX
	* LIGHTYELLOW_EX
	* LIGHTBLUE_EX
	* LIGHTMAGENTA_EX
	* LIGHTCYAN_EX
	* LIGHTWHITE_EX
	"""

	_stack = fore_stack
	_reset = "\u001b[39m"

	BLACK = 30
	RED = 31
	GREEN = 32
	YELLOW = 33
	BLUE = 34
	MAGENTA = 35
	CYAN = 36
	WHITE = 37
	RESET = 39

	# These are fairly well supported, but not part of the standard.
	LIGHTBLACK_EX = 90
	LIGHTRED_EX = 91
	LIGHTGREEN_EX = 92
	LIGHTYELLOW_EX = 93
	LIGHTBLUE_EX = 94
	LIGHTMAGENTA_EX = 95
	LIGHTCYAN_EX = 96
	LIGHTWHITE_EX = 97


class AnsiBack(AnsiCodes):
	"""
	ANSI Colour Codes for background colour.

	The colours can be used as a context manager, a string, or a function.

	Valid values are:

	* BLACK
	* RED
	* GREEN
	* YELLOW
	* BLUE
	* MAGENTA
	* CYAN
	* WHITE
	* RESET
	* LIGHTBLACK_EX
	* LIGHTRED_EX
	* LIGHTGREEN_EX
	* LIGHTYELLOW_EX
	* LIGHTBLUE_EX
	* LIGHTMAGENTA_EX
	* LIGHTCYAN_EX
	* LIGHTWHITE_EX
	"""

	_stack = back_stack
	_reset = "\u001b[49m"

	BLACK = 40
	RED = 41
	GREEN = 42
	YELLOW = 43
	BLUE = 44
	MAGENTA = 45
	CYAN = 46
	WHITE = 47
	RESET = 49

	# These are fairly well supported, but not part of the standard.
	LIGHTBLACK_EX = 100
	LIGHTRED_EX = 101
	LIGHTGREEN_EX = 102
	LIGHTYELLOW_EX = 103
	LIGHTBLUE_EX = 104
	LIGHTMAGENTA_EX = 105
	LIGHTCYAN_EX = 106
	LIGHTWHITE_EX = 107


class AnsiStyle(AnsiCodes):
	"""
	ANSI Colour Codes for text style.

	Valid values are:

	* BRIGHT
	* DIM
	* NORMAL

	Additionally, ``AnsiStyle.RESET_ALL`` can be used to reset the
	foreground and background colours as well as the text style.
	"""

	_stack = style_stack
	_reset = "\u001b[22m"

	BRIGHT = 1
	DIM = 2
	NORMAL = 22
	RESET_ALL = 0


Fore = AnsiFore()
Back = AnsiBack()
Style = AnsiStyle()
Cursor = AnsiCursor()

fore_stack.append(Fore.RESET)
back_stack.append(Back.RESET)
style_stack.append(Style.NORMAL)
