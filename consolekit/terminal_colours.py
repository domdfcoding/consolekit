#!/usr/bin/env python
#
#  terminal_colours.py
"""
Functions for adding ANSI character codes to terminal print statements.

.. seealso:: http://en.wikipedia.org/wiki/ANSI_escape_code
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
from collections import deque
from functools import partial
from typing import Deque, Iterable, List, Optional, Pattern, Type, TypeVar, Union

# 3rd party
import click
from typing_extensions import Final

__all__ = (
		"AnsiFore",
		"AnsiBack",
		"AnsiStyle",
		"AnsiCursor",
		"Fore",
		"Back",
		"Style",
		"Cursor",
		"AnsiCodes",
		"Colour",
		"ColourTrilean",
		"clear_line",
		"code_to_chars",
		"resolve_color_default",
		"set_title",
		"strip_ansi",
		"CSI",
		"OSC",
		"BEL",
		)

try:
	# 3rd party
	import colorama  # type: ignore[import]
	colorama.init()

except ImportError:
	pass

_C = TypeVar("_C", bound="Colour")
_AC = TypeVar("_AC", bound="AnsiCodes")

ColourTrilean = Optional[bool]
"""
Represents the :py:obj:`True`/:py:obj:`False`/:py:obj:`None` state of colour options.

.. versionadded:: 0.8.0
"""

CSI: Final[str] = "\u001b["
OSC: Final[str] = "\u001b]"
BEL: Final[str] = '\x07'

fore_stack: Deque[str] = deque()
back_stack: Deque[str] = deque()
style_stack: Deque[str] = deque()


def resolve_color_default(color: ColourTrilean = None) -> ColourTrilean:
	"""
	Helper to get the default value of the color flag.

	If a value is passed it is returned unchanged,
	otherwise it's looked up from the current context.

	If the environment variable ``PYCHARM_HOSTED`` is ``1``
	(which is the case if running in PyCharm)
	the output will be coloured by default.

	If the environment variable ``NO_COLOR`` is ``1``
	the output will not be coloured by default.
	See https://no-color.org/ for more details.
	This variable takes precedence over ``PYCHARM_HOSTED``.

	If no value is passed in, there is no context,
	and neither environment variable is set,
	:py:obj:`None` is returned.

	.. versionchanged:: 1.3.0

		* Added support for the ``NO_COLOR`` environment variable.
		* Only uses a value from the click context (:attr:`Context.color <click.Context.color>`)
		  if it is not :py:obj:`None`. Otherwise falls back to checking the environment variables.

	:param color:
	"""

	if color is not None:
		return color

	ctx = click.get_current_context(silent=True)

	if ctx is not None and ctx.color is not None:
		return ctx.color

	if int(os.environ.get("NO_COLOR", 0)):
		return False

	if int(os.environ.get("PYCHARM_HOSTED", 0)):
		return True

	return None


def code_to_chars(code: Union[str, int]) -> str:  # noqa: D103
	return CSI + str(code) + 'm'


def set_title(title: str) -> str:  # noqa: D103
	return OSC + "2;" + title + BEL


# def clear_screen(mode: int = 2) -> str:
# 	return CSI + str(mode) + 'J'


def clear_line(mode: int = 2) -> str:  # noqa: D103
	return CSI + str(mode) + 'K'


_ansi_re: Pattern[str] = re.compile(r"\033\[[;?0-9]*[a-zA-Z]")


def strip_ansi(value: str) -> str:
	"""
	Strip ANSI colour codes from the given string to return a plaintext output.

	:param value:
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

	.. autosummary-widths:: 7/16
	"""

	__slots__ = ("style", "reset", "stack")

	style: str
	reset: str
	stack: Union[Deque[str], List[str]]

	def __new__(cls, style: str, stack: Union[Deque[str], List[str]], reset: str) -> "Colour":  # noqa: D102
		self = super().__new__(cls, style)  # type: ignore[import]
		self.style = style
		self.stack = stack
		self.reset = reset

		return self

	def __enter__(self) -> None:
		print(self.style, end='')
		self.stack.append(self.style)

	def __exit__(self, exc_type, exc_val, exc_tb) -> None:
		if self.style == self.stack[-1]:
			self.stack.pop()
			print(self.stack[-1], end='')

	def __call__(self, text) -> str:  # noqa: MAN001
		"""
		Returns the given text in this colour.
		"""

		return f"{self}{text}{self.reset}"

	@classmethod
	def from_code(cls: Type[_C], code: Union[str, int], background: bool = False) -> _C:
		"""
		Returns a :class:`~.Colour` to create coloured text.

		The colour can be reset using :py:obj:`.Fore.RESET` or :py:obj:`.Back.RESET`.

		.. versionadded:: 0.9.0

		:param code: A 3- or 4- bit ANSI colour code.
		:param background: Whether to set the colour for the background.

		:rtype: :class:`~.Colour`

		.. note::

			The ``background`` option only influences the reset value and the stack used.
			It will not handle conversion of foreground codes to background codes.

		.. latex:clearpage::
		"""

		if background:
			stack = back_stack
			reset = AnsiBack._reset
		else:
			stack = fore_stack
			reset = AnsiFore._reset

		return cls(code_to_chars(code), stack=stack, reset=reset)

	@classmethod
	def from_256_code(cls: Type[_C], code: Union[str, int], background: bool = False) -> _C:
		"""
		Returns a :class:`~.Colour` to create 256-colour text.

		The colour can be reset using :py:obj:`.Fore.RESET` or :py:obj:`.Back.RESET`.

		.. versionadded:: 0.9.0
		.. note:: Not all terminals support 256-colour mode.

		:param code: A 256-colour ANSI code.
		:param background: Whether to set the colour for the background.

		:rtype: :class:`~.Colour`

		.. note::

			The ``background`` option only influences the reset value and the stack used.
			It will not handle conversion of foreground codes to background codes.
		"""

		if background:
			stack = back_stack
			reset = AnsiBack._reset
			template = CSI + "48;5;{}m"

		else:
			stack = fore_stack
			reset = AnsiFore._reset
			template = CSI + "38;5;{}m"

		return cls(template.format(code), stack=stack, reset=reset)

	@classmethod
	def from_rgb(
			cls: Type[_C],
			r: Union[str, int],
			g: Union[str, int],
			b: Union[str, int],
			background: bool = False
			) -> _C:
		"""
		Returns a :class:`~.Colour` to create 24-bit coloured text.

		The colour can be reset using :py:obj:`.Fore.RESET` or :py:obj:`.Back.RESET`.

		.. versionadded:: 0.9.0

		.. note:: Not all terminals support 24-bit colours.

		:param r:
		:param g:
		:param b:
		:param background: Whether to set the colour for the background.

		:rtype: :class:`~.Colour`

		.. note::

			The ``background`` option only influences the reset value and the stack used.
			It will not handle conversion of foreground codes to background codes.

		.. latex:clearpage::
		"""

		if background:
			template = CSI + "48;2;{r};{g};{b}m"
			stack = back_stack
			reset = AnsiBack._reset

		else:
			template = CSI + "38;2;{r};{g};{b}m"
			stack = fore_stack
			reset = AnsiFore._reset

		return cls(template.format(r=r, g=g, b=b), stack=stack, reset=reset)

	@classmethod
	def from_hex(cls: Type[_C], hex_colour: str, background: bool = False) -> _C:
		"""
		Returns a :class:`~.Colour` to create 24-bit coloured text.

		The colour can be reset using :py:obj:`.Fore.RESET` or :py:obj:`.Back.RESET`.

		.. versionadded:: 0.9.0

		.. note:: Not all terminals support 24-bit colours.

		:param hex_colour: The hex colour code.
		:param background: Whether to set the colour for the background.

		:rtype: :class:`~.Colour`

		.. note::

			The ``background`` option only influences the reset value and the stack used.
			It will not handle conversion of foreground codes to background codes.
		"""

		# From https://stackoverflow.com/q/29643352
		# https://stackoverflow.com/users/3924370/julian-white
		# CC BY-SA 3.0

		value = hex_colour.lstrip('#')
		lv = len(value)
		r, g, b = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

		return cls.from_rgb(r, g, b, background=background)


def print_256_colour_testpattern() -> None:
	"""
	Print a 256-colour test pattern to the terminal.

	.. versionadded:: 0.9.0

	.. note:: Not all terminals support 24-bit colours.
	"""

	# 3rd party
	from domdf_python_tools.iterative import chunks

	def print_heading(text: str, block_size: int = 3, n_blocks: int = 36) -> None:
		click.echo()
		click.echo(str(text).center(((block_size + 1) * n_blocks) - 1, '-'))

	def print_line(values: Iterable[int], block_size: int = 3) -> None:
		values = list(values)
		mid = len(values) // 2

		colour: Optional[bool] = resolve_color_default()
		echo = partial(click.echo, nl=False, color=colour)

		for code in values[:mid]:
			echo(Colour.from_256_code(code, background=True)(str(code).center(block_size)) + ' ')
		with Fore.BLACK:
			for code in values[mid:-1]:
				echo(Colour.from_256_code(code, background=True)(str(code).center(block_size)) + ' ')
			click.echo(
					Colour.from_256_code(values[-1], background=True)(str(values[-1]).center(block_size).rstrip()),
					color=colour
					)

	print_heading(
			"Standard Colours".center((9 * 8) - 1, '-') + ' ' + "High-Intensity Colours".center((9 * 8) - 1, '-'),
			block_size=8,
			n_blocks=16
			)

	print_line(range(16), block_size=8)

	print_heading("216 Colours")
	for row in chunks(range(16, 232), 36):  # pylint: disable=loop-invariant-statement
		print_line(row)

	print_heading("Greyscale Colours", block_size=5, n_blocks=24)
	print_line(range(232, 256), block_size=5)

	click.echo('\n')


class AnsiCodes(ABC):
	"""
	Abstract base class for ANSI Codes.
	"""

	_stack: Union[Deque[str], List[str]]
	_reset: str

	def __init_subclass__(cls, **kwargs) -> None:
		"""
		The subclasses declare class attributes which are numbers.

		Upon instantiation we define instance attributes, which are the same
		as the class attributes but wrapped with the ANSI escape sequence.
		"""

		for name in dir(cls):
			if not name.startswith('_'):
				value = getattr(cls, name)
				setattr(cls, name, Colour(code_to_chars(value), cls._stack, cls._reset))

	def __new__(cls: Type[_AC], *args, **kwargs) -> Type[_AC]:  # noqa: D102
		return cls


class AnsiCursor:
	"""
	Provides methods to control the cursor.
	"""

	def UP(self, n: int = 1) -> str:
		"""
		Moves the cursor up ``n`` lines.

		:param n:
		"""

		return f"{CSI}{str(n)}A"

	def DOWN(self, n: int = 1) -> str:
		"""
		Moves the cursor down ``n`` lines.

		:param n:
		"""

		return f"{CSI}{str(n)}B"

	def FORWARD(self, n: int = 1) -> str:
		"""
		Moves the cursor forward (right) ``n`` lines.

		:param n:
		"""

		return f"{CSI}{str(n)}C"

	def BACK(self, n: int = 1) -> str:
		"""
		Moves the cursor backward (left) ``n`` lines.

		:param n:
		"""

		return f"{CSI}{str(n)}D"

	def POS(self, x: int = 1, y: int = 1) -> str:
		"""
		Moves the cursor to the given position.

		:param x:
		:param y:
		"""

		return f"{CSI}{str(y)};{str(x)}H"

	def HIDE(self) -> str:
		"""
		Hides the cursor.

		.. versionadded:: 0.7.0
		"""

		return f"{CSI}?25l"

	def SHOW(self) -> str:
		"""
		Shows the cursor.

		.. versionadded:: 0.7.0
		"""

		return f"{CSI}?25h"


class AnsiFore(AnsiCodes):
	r"""
	ANSI Colour Codes for foreground colour.

	The colours can be used as a context manager, a string, or a function.

	Valid values are:

	.. raw:: latex

		\vspace{-5px}
		\begin{multicols}{3}

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

	.. raw:: latex

		\end{multicols}
		\vspace{-5px}

	This class is also available under the shorter alias :py:obj:`Fore`.
	"""

	_stack = fore_stack
	_reset = f"{CSI}39m"

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
	r"""
	ANSI Colour Codes for background colour.

	The colours can be used as a context manager, a string, or a function.

	Valid values are:

	.. raw:: latex

		\vspace{-5px}
		\begin{multicols}{3}

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

	.. raw:: latex

		\end{multicols}
		\vspace{-5px}

	This class is also available under the shorter alias :py:obj:`Back`.
	"""

	_stack = back_stack
	_reset = f"{CSI}49m"

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

	This class is also available under the shorter alias :py:obj:`Style`.
	"""

	_stack = style_stack
	_reset = f"{CSI}22m"

	BRIGHT = 1
	DIM = 2
	NORMAL = 22
	RESET_ALL = 0


Fore = AnsiFore
Back = AnsiBack
Style = AnsiStyle
Cursor = AnsiCursor()

fore_stack.append(Fore.RESET)
back_stack.append(Back.RESET)
style_stack.append(Style.NORMAL)

if __name__ == "__main__":
	print_256_colour_testpattern()
