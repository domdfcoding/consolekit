#!/usr/bin/env python3
#
#  utils.py
"""
Utility functions.
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

# stdlib
import difflib
import os
from itertools import cycle
from types import ModuleType
from typing import IO, List, Sequence

# 3rd party
import click
from domdf_python_tools.import_tools import discover, discover_entry_points
from domdf_python_tools.stringlist import StringList

# this package
from consolekit.terminal_colours import Colour, Cursor, Fore

__all__ = [
		"get_env_vars",
		"is_command",
		"import_commands",
		"abort",
		"overtype",
		"coloured_diff",
		"solidus_spinner",
		"braille_spinner",
		"hide_cursor",
		"show_cursor",
		]


def get_env_vars(ctx, args, incomplete):  # noqa: D103
	return [k for k in os.environ.keys() if incomplete in k]


def is_command(obj) -> bool:
	"""
	Return whether ``obj`` is a click command.

	:param obj:
	"""

	return isinstance(obj, click.Command)


def import_commands(source: ModuleType, entry_point: str) -> List[click.Command]:
	"""
	Returns a list of all commands.

	Commands can be defined locally in the module given in ``source``,
	or by third party extensions who define an entry point in the following format:

	::

		<name (can be anything)> = <module name>:<command>

	:param source:
	:param entry_point:
	"""

	local_commands = discover(source, is_command, exclude_side_effects=False)
	third_party_commands = discover_entry_points(entry_point, is_command)
	return [*local_commands, *third_party_commands]


def abort(message: str) -> Exception:
	"""
	Aborts the program execution.

	:param message:
	"""

	click.echo(Fore.RED(message), err=True)
	return click.Abort()


def overtype(*objects, sep: str = ' ', end: str = '', file: IO = None, flush: bool = False) -> None:
	"""
	Print ``objects`` to the text stream ``file``, starting with ``"\\r"``, separated by ``sep``
	and followed by ``end``.

	``sep``, ``end``, ``file`` and ``flush``, if present, must be given as keyword arguments

	All non-keyword arguments are converted to strings like :class:`str` does and written to the stream,
	separated by `sep` and followed by `end`.

	If no objects are given, :func:`~consolekit.terminal.overtype` will just write ``"\\r"``.

	.. TODO:: This does not currently work in the PyCharm console, at least on Windows

	:param objects: A list of strings or string-like objects to write to the terminal.
	:param sep: String to separate the objects with.
	:param end: String to end with.
	:param file: An object with a ``write(string)`` method.
	:default file: ``sys.stdout``
	:param flush: If :py:obj:`True`, the stream is forcibly flushed.
	"""  # noqa D400

	object0 = f"\r{objects[0]}"
	objects = (object0, *objects[1:])
	print(*objects, sep=sep, end=end, file=file, flush=flush)


def coloured_diff(
		a: Sequence[str],
		b: Sequence[str],
		fromfile: str = '',
		tofile: str = '',
		fromfiledate: str = '',
		tofiledate: str = '',
		n: int = 3,
		lineterm: str = '\n',
		removed_colour: Colour = Fore.RED,
		added_colour: Colour = Fore.GREEN,
		) -> str:
	r"""
	Compare two sequences of lines; generate the delta as a unified diff.

	Unified diffs are a compact way of showing line changes and a few
	lines of context. The number of context lines is set by ``n`` which
	defaults to three.

	By default, the diff control lines (those with ``---``, ``+++``, or ``@@``)
	are created with a trailing newline. This is helpful so that inputs
	created from ``file.readlines()`` result in diffs that are suitable for
	``file.writelines()`` since both the inputs and outputs have trailing
	newlines.

	For inputs that do not have trailing newlines, set the lineterm
	argument to ``''`` so that the output will be uniformly newline free.

	The unidiff format normally has a header for filenames and modification
	times. Any or all of these may be specified using strings for
	``fromfile``, ``tofile``, ``fromfiledate``, and ``tofiledate``.
	The modification times are normally expressed in the ISO 8601 format.

	**Example:**

	>>> for line in coloured_diff('one two three four'.split(),
	...             'zero one tree four'.split(), 'Original', 'Current',
	...             '2005-01-26 23:30:50', '2010-04-02 10:20:52',
	...             lineterm=''):
	...     print(line)                 # doctest: +NORMALIZE_WHITESPACE
	--- Original        2005-01-26 23:30:50
	+++ Current         2010-04-02 10:20:52
	@@ -1,4 +1,4 @@
	+zero
	one
	-two
	-three
	+tree
	four

	:param a:
	:param b:
	:param fromfile:
	:param tofile:
	:param fromfiledate:
	:param tofiledate:
	:param n:
	:param lineterm:
	:param removed_colour: The :class:`~consolekit.terminal_colours.Colour` to use for lines that were removed.
	:param added_colour: The :class:`~consolekit.terminal_colours.Colour` to use for lines that were added.

	.. versionadded:: 0.3.0
	"""

	buf = StringList()
	diff = difflib.unified_diff(a, b, fromfile, tofile, fromfiledate, tofiledate, n, lineterm)

	for line in diff:
		if line.startswith('+'):
			buf.append(added_colour(line))
		elif line.startswith('-'):
			buf.append(removed_colour(line))
		else:
			buf.append(line)

	buf.blankline(ensure_single=True)

	return str(buf)


solidus_spinner = cycle("|/-\\")
"""
:class:`itertools.cycle` of characters to use as a loading spinner.

.. versionadded:: 0.7.0
"""

braille_spinner = cycle("⢿ ⣻ ⣽ ⣾ ⣷ ⣯ ⣟ ⡿ ".split(' '))
"""
:class:`itertools.cycle` of braille characters to use as a loading spinner.

.. versionadded:: 0.7.0
"""


def hide_cursor() -> None:
	"""
	Hides the cursor.

	.. versionadded:: 0.7.0
	"""

	click.echo(Cursor.HIDE)


def show_cursor() -> None:
	"""
	Shows the cursor.

	.. versionadded:: 0.7.0
	"""

	click.echo(Cursor.SHOW)


@lru_cache(1)
def _pycharm_hosted():
	return os.environ.get("PYCHARM_HOSTED", 0)


@lru_cache(1)
def _pycharm_terminal():
	try:
		# 3rd party
		import psutil  # type: ignore  # nodep

		parent_process = psutil.Process(os.getppid())
		grandparent_process = psutil.Process(parent_process.ppid())
		great_grandparent_process = psutil.Process(grandparent_process.ppid())
		great_grandparent_name = great_grandparent_process.name()

		#: TODO: pycharm on Windows and macOS
		return great_grandparent_name == "pycharm.sh"

	except Exception:
		return False


class TerminalRenderer(BaseRenderer):
	"""
	Mistletoe markdown renderer for terminals.

	Tested in Gnome Terminal and Terminator (both libVTE-based), and PyCharm.
	libVTE has the best support. PyCharm's support for italics and strikethrough is poor.

	Not tested on other terminals, but contributions are welcome to improve support.

	.. versionadded:: 0.8.0
	"""

	def render_strong(self, token: span_token.Strong) -> str:
		"""
		Render strong (``**strong**``).

		:param token: The token to render.
		"""

		return Style.BRIGHT(self.render_inner(token))

	def render_emphasis(self, token: span_token.Emphasis) -> str:
		"""
		Render emphasis (``*emphasis*``).

		:param token: The token to render.
		"""

		if _pycharm_hosted():
			# Pycharm terminal doesn't support italic escape
			return SANS_SERIF_ITALIC_LETTERS(self.render_inner(token))

		return f"{code_to_chars(3)}{self.render_inner(token)}{code_to_chars(23)}"

	def render_inline_code(self, token: span_token.InlineCode) -> str:
		r"""
		Render inline code (``\`code\```).

		:param token: The token to render.
		"""

		# TODO: A better implementation
		return f"'{self.render_inner(token)}'"

	def render_strikethrough(self, token: span_token.Strikethrough) -> str:
		"""
		Render strikethrough (``~~strikethrough~~``).

		:param token: The token to render.
		"""

		if _pycharm_hosted() or _pycharm_terminal():
			# Pycharm terminal doesn't support strikethrough
			return self.render_inner(token)

		return ''.join([f'{char}\u0336' for char in self.render_inner(token)])

	def render_paragraph(self, token: block_token.Paragraph) -> str:
		"""
		Render a paragraph.

		:param token: The token to render.
		"""

		return '\n{}\n'.format(self.render_inner(token))

	_in_ordered_list: bool = False
	_ol_number: int = 0

	def render_list(self, token: block_token.List) -> str:
		"""
		Render a markdown list.

		:param token: The token to render.
		"""

		self._in_ordered_list = token.start is not None
		if self._in_ordered_list:
			self._ol_number = 0

		return self.render_inner(token) + '\n'

	def render_list_item(self, token: block_token.ListItem) -> str:
		"""
		Render a markdown list item.

		:param token:
		"""

		if self._in_ordered_list:
			self._ol_number += 1
			return f" {self._ol_number}. {self.render_inner(token).lstrip()}"

		else:
			return f" * {self.render_inner(token).lstrip()}"

	def render(self, token) -> str:
		"""
		Render the given token for display in a terminal.

		:param token:
		"""

		return super().render(token).replace("\n\n\n", "\n\n")
