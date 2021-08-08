#!/usr/bin/env python3
#
#  utils.py
"""
Utility functions.

.. versionchanged:: 1.0.0

	:func:`~.tracebacks.traceback_handler` and :func:`~.tracebacks.handle_tracebacks`
	moved to :mod:`consolekit.tracebacks`.
	They will still be importable from here until v2.0.0

.. automodulesumm:: consolekit.utils
.. latex:clearpage::
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

# stdlib
import contextlib
import difflib
import os
import shutil
import sys
from functools import lru_cache
from itertools import cycle
from types import ModuleType
from typing import IO, Iterable, Iterator, List, Optional, Sequence, Union

# 3rd party
import click
import deprecation_alias
from domdf_python_tools.import_tools import discover, discover_entry_points
from domdf_python_tools.stringlist import StringList
from domdf_python_tools.words import SANS_SERIF_ITALIC_LETTERS
from mistletoe import block_token, span_token  # type: ignore
from mistletoe.base_renderer import BaseRenderer  # type: ignore

# this package
from consolekit import terminal_colours, tracebacks
from consolekit.terminal_colours import ColourTrilean, resolve_color_default

__all__ = [
		"get_env_vars",
		"is_command",
		"import_commands",
		"abort",
		"overtype",
		"coloured_diff",
		"solidus_spinner",
		"braille_spinner",
		"snake_spinner",
		"hide_cursor",
		"show_cursor",
		"TerminalRenderer",
		"hidden_cursor",
		"long_echo",
		]

_deprecator = deprecation_alias.deprecated(
		deprecated_in="1.0.0",
		removed_in="2.0.0",
		current_version="1.3.0",
		details="Import from consolekit.tracebacks instead."
		)

handle_tracebacks = _deprecator(tracebacks.handle_tracebacks)
traceback_handler = _deprecator(tracebacks.traceback_handler)


def get_env_vars(ctx, args, incomplete):  # noqa: D103
	return [k for k in os.environ.keys() if incomplete in k]


def is_command(obj) -> bool:
	"""
	Return whether ``obj`` is a click command.

	:param obj:
	"""

	return isinstance(obj, click.Command)


def import_commands(source: Optional[ModuleType] = None, entry_point: Optional[str] = None) -> List[click.Command]:
	"""
	Returns a list of all commands.

	Commands can be defined locally in the module given in ``source``,
	or by third party extensions who define an entry point in the following format:

	::

		<name (can be anything)> = <module name>:<command>

	:param source:
	:param entry_point:
	"""

	all_commands = []

	if source is not None:
		all_commands.extend(discover(source, is_command, exclude_side_effects=False))
	if entry_point is not None:
		all_commands.extend(discover_entry_points(entry_point, is_command))

	return all_commands


# TODO: Turn this into a class so the message is only printed when raised.
def abort(message: str, colour: ColourTrilean = None) -> Exception:
	"""
	Aborts the program execution.

	:param message:
	:param colour: Whether to use coloured output. Default auto-detect.
	:no-default colour:

	.. versionchanged:: 1.0.1  Added the ``colour`` option.
	"""

	click.echo(terminal_colours.Fore.RED(message), err=True, color=resolve_color_default(colour))
	return click.Abort()


def overtype(
		*objects,
		sep: str = ' ',
		end: str = '',
		file: Optional[IO] = None,
		flush: bool = False,
		) -> None:
	r"""
	Print ``objects`` to the text stream ``file``, starting with ``"\r"``, separated by ``sep``
	and followed by ``end``.

	``sep``, ``end``, ``file`` and ``flush``, if present, must be given as keyword arguments

	All non-keyword arguments are converted to strings like :class:`str` does and written to the stream,
	separated by `sep` and followed by `end`.
	If no such arguments are given, :func:`~consolekit.utils.overtype` will just write ``"\r"``.

	.. TODO:: This does not currently work in the PyCharm console, at least on Windows

	:param objects: A list of strings or string-like objects to write to the terminal.
	:param sep: String to separate the objects with.
	:param end: String to end with.
	:param file: An object with a ``write(string)`` method.
	:default file: ``sys.stdout``
	:param flush: If :py:obj:`True`, the stream is forcibly flushed.
	"""  # noqa: D400

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
		removed_colour: terminal_colours.Colour = terminal_colours.Fore.RED,
		added_colour: terminal_colours.Colour = terminal_colours.Fore.GREEN,
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

	.. versionadded:: 0.3.0
	.. latex:clearpage::

	**Example:**

	>>> for line in coloured_diff(
	...     'one two three four'.split(),
	...     'zero one tree four'.split(), 'Original', 'Current',
	...     '2005-01-26 23:30:50', '2010-04-02 10:20:52',
	...     lineterm='',
	...     ):
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
:func:`itertools.cycle` of characters to use as a loading spinner.

.. versionadded:: 0.7.0
"""

braille_spinner = cycle(['⢿', '⣻', '⣽', '⣾', '⣷', '⣯', '⣟', '⡿'])
"""
:func:`itertools.cycle` of braille characters to use as a loading spinner.

.. versionadded:: 0.7.0
"""

snake_spinner = cycle(['⠋', '⠙', '⠸', '⠴', '⠦', '⠇'])
"""
:func:`itertools.cycle` of braille characters to use as a loading spinner which looks like a snake.

.. versionadded:: 1.1.0
"""


def hide_cursor() -> None:
	"""
	Hide the cursor.

	To show it again use :func:`~.show_cursor`,
	or use the :func:`~.hidden_cursor` context manager.

	.. versionadded:: 0.7.0
	"""

	click.echo(
			terminal_colours.Cursor.HIDE(),
			nl=False,
			color=terminal_colours.resolve_color_default(),
			)


def show_cursor() -> None:
	"""
	Show the cursor.

	.. seealso:: The  :func:`~.hidden_cursor` context manager.

	.. versionadded:: 0.7.0
	"""

	click.echo(
			terminal_colours.Cursor.SHOW(),
			nl=False,
			color=terminal_colours.resolve_color_default(),
			)


@contextlib.contextmanager
def hidden_cursor() -> Iterator:
	"""
	Context manager to hide the cursor for the scope of the ``with`` block.

	.. versionadded:: 0.7.0

	.. versionchanged:: 0.9.0  Moved to :mod:`consolekit.utils`.
	"""

	try:
		hide_cursor()
		yield
	finally:
		show_cursor()


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

	except Exception:  # pragma: no cover
		return False


class TerminalRenderer(BaseRenderer):
	"""
	Mistletoe markdown renderer for terminals.

	Tested in Gnome Terminal and Terminator (both libVTE-based), and PyCharm.
	libVTE has the best support.
	PyCharm's support for italics and strikethrough is poor.
	Support on Windows is, as expected, poor.

	Not tested on other terminals, but contributions are welcome to improve support.

	.. versionadded:: 0.8.0
	"""

	def render_strong(self, token: span_token.Strong) -> str:
		"""
		Render strong (``**strong**``).

		:param token: The token to render.
		"""

		return terminal_colours.Style.BRIGHT(self.render_inner(token))

	def render_emphasis(self, token: span_token.Emphasis) -> str:
		"""
		Render emphasis (``*emphasis*``).

		:param token: The token to render.
		"""

		if int(os.environ.get("PYCHARM_HOSTED", 0)):
			# Pycharm terminal doesn't support italic escape
			return SANS_SERIF_ITALIC_LETTERS(self.render_inner(token))

		return ''.join([
				terminal_colours.code_to_chars(3),
				self.render_inner(token),
				terminal_colours.code_to_chars(23),
				])

	def render_inline_code(self, token: span_token.InlineCode) -> str:
		r"""
		Render inline code (:inline-code:`code`).

		:param token: The token to render.
		"""

		# TODO: A better implementation
		return f"{self.render_inner(token)!r}"

	def render_strikethrough(self, token: span_token.Strikethrough) -> str:
		"""
		Render strikethrough (``~~strikethrough~~``).

		:param token: The token to render.
		"""

		if int(os.environ.get("PYCHARM_HOSTED", 0)) or _pycharm_terminal():
			# Pycharm terminal doesn't support strikethrough
			return self.render_inner(token)

		return ''.join([f'{char}\u0336' for char in self.render_inner(token)])

	def render_paragraph(self, token: block_token.Paragraph) -> str:
		"""
		Render a paragraph.

		:param token: The token to render.
		"""

		return f'\n{self.render_inner(token)}\n'

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

	@staticmethod
	def render_line_break(token):
		"""
		Render a line break in a multiline paragraph.

		:param token:
		"""

		return ' '

	def render(self, token) -> str:
		"""
		Render the given token for display in a terminal.

		:param token:
		"""

		return super().render(token).replace("\n\n\n", "\n\n")


def long_echo(
		text: Union[str, StringList, Iterable[str]],
		use_pager: Optional[bool] = None,
		colour: ColourTrilean = None
		) -> None:
	"""
	Echo ``text`` to the terminal, optionally via a pager.

	.. versionadded:: 1.2.0

	:param text:
	:param use_pager: If :py:obj:`True`, forces the use of the pager. If :py:obj:`False` the pager is never used.
		If :py:obj:`None` the pager is used if `sys.stdout`` is a TTY and the number of lines is
		less than the terminal height.
	:param colour:  Whether to use coloured output. Default auto-detect.
	:no-default colour:

	.. tip:: Allow the user to control the value of ``use_pager`` with the :func:`no_pager_option` decorator.
	"""

	if isinstance(text, str):
		text = StringList(text.split('\n'))
	elif not isinstance(text, StringList):
		text = StringList(text)

	if use_pager is None:
		use_pager = True

		if shutil.get_terminal_size().lines >= len(text):
			# Don't use pager if fewer lines than terminal height
			use_pager = False

		if not sys.stdout.isatty():
			use_pager = False

	if use_pager:
		return click.echo_via_pager(str(text), color=colour)
	else:
		return click.echo(str(text), color=colour)
