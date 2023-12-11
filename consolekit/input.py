#!/usr/bin/env python3
#
#  input.py
"""
Input functions (prompt, choice etc.).
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
#  prompt and confirm based on https://github.com/pallets/click
#  Copyright 2014 Pallets
#  |  Redistribution and use in source and binary forms, with or without modification,
#  |  are permitted provided that the following conditions are met:
#  |
#  |      * Redistributions of source code must retain the above copyright notice,
#  |        this list of conditions and the following disclaimer.
#  |      * Redistributions in binary form must reproduce the above copyright notice,
#  |        this list of conditions and the following disclaimer in the documentation
#  |        and/or other materials provided with the distribution.
#  |      * Neither the name of the copyright holder nor the names of its contributors
#  |        may be used to endorse or promote products derived from this software without
#  |        specific prior written permission.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  |  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  |  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  |  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#  |  OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  |  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  |  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  |  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  |  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  |  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  |  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  |
#
#  stderr_input based on raw_input from https://foss.heptapod.net/pypy/pypy
#  PyPy Copyright holders 2003-2020
#  MIT Licenced
#

# stdlib
import sys
from typing import IO, Any, Callable, List, Mapping, Optional, Union, overload

# 3rd party
import click
from click.termui import _build_prompt, hidden_prompt_func
from click.types import Path, convert_type

# this package
from consolekit import _readline  # noqa: F401
from consolekit._types import _ConvertibleType

__all__ = (
		"prompt",
		"confirm",
		"stderr_input",
		"choice",
		)


def prompt(  # noqa: MAN002
		text: str,
		default: Optional[str] = None,
		hide_input: bool = False,
		confirmation_prompt: Union[bool, str] = False,
		type: Optional[_ConvertibleType] = None,  # noqa: A002  # pylint: disable=redefined-builtin
		value_proc: Optional[Callable[[Optional[str]], Any]] = None,
		prompt_suffix: str = ": ",
		show_default: bool = True,
		err: bool = False,
		show_choices: bool = True,
		):
	"""
	Prompts a user for input.

	If the user aborts the input by sending an interrupt signal,
	this function will catch it and raise a :exc:`click.Abort` exception.

	:param text: The text to show for the prompt.
	:param default: The default value to use if no input happens.
		If this is not given it will prompt until it is aborted.
	:param hide_input: If :py:obj:`True` then the input value will be hidden.
	:param confirmation_prompt: Asks for confirmation for the value.
		Can be set to a string instead of :py:obj:`True` to customize the message.
	:param type: The type to check the value against.
	:param value_proc: If this parameter is provided it must be a function that
		is invoked instead of the type conversion to convert a value.
	:param prompt_suffix: A suffix that should be added to the prompt.
	:param show_default: Shows or hides the default value in the prompt.
	:param err: If :py:obj:`True` the file defaults to ``stderr`` instead of
		``stdout``, the same as with :func:`click.echo`.
	:param show_choices: Show or hide choices if the passed type is a :class:`click.Choice`.
		For example, if the choice is either ``day`` or ``week``,
		``show_choices`` is :py:obj:`True` and ``text`` is ``'Group by'`` then the
		prompt will be ``'Group by (day, week): '``.
	"""

	result = None  # noqa

	def prompt_func(text: Any) -> Any:
		try:
			return _prompt(text, err=err, hide_input=hide_input)
		except (KeyboardInterrupt, EOFError):
			if hide_input:
				click.echo(None, err=err)
			raise click.Abort()

	if value_proc is None:
		value_proc = convert_type(type, default)

	prompt = _build_prompt(
			text,
			prompt_suffix,
			show_default,
			default,
			show_choices,
			type,  # type: ignore[arg-type]
			)

	has_default = default is not None

	while True:
		while True:
			value = prompt_func(prompt)

			if value:
				break
			elif has_default:
				if isinstance(value_proc, Path):  # pylint: disable=loop-invariant-statement
					# validate Path default value (exists, dir_okay etc.)
					value = default
					break
				return default

		try:  # pylint: disable=loop-try-except-usage
			result = value_proc(value)
		except click.UsageError as e:
			click.echo(f"Error: {e.message}", err=err)  # pylint: disable=loop-invariant-statement
			continue

		if not confirmation_prompt:
			return result

		if confirmation_prompt is True:
			confirmation_prompt = "Repeat for confirmation: "

		while True:
			value2 = prompt_func(confirmation_prompt)
			if value2:
				break

		if value == value2:  # pylint: disable=loop-invariant-statement
			return result

		click.echo("Error: the two entered values do not match", err=err)


def confirm(  # noqa: MAN002
		text: str,
		default: bool = False,
		abort: bool = False,
		prompt_suffix: str = ": ",
		show_default: bool = True,
		err: bool = False,
		):
	"""
	Prompts for confirmation (yes/no question).

	If the user aborts the input by sending a interrupt signal this
	function will catch it and raise a :exc:`click.Abort` exception.

	.. latex:clearpage::

	:param text: The question to ask.
	:param default: The default for the prompt.
	:param abort: If :py:obj:`True` a negative answer aborts the exception by raising :exc:`click.Abort`.
	:param prompt_suffix: A suffix that should be added to the prompt.
	:param show_default: Shows or hides the default value in the prompt.
	:param err: If :py:obj:`True` the file defaults to ``stderr`` instead of ``stdout``, the same as with echo.
	"""

	prompt = _build_prompt(text, prompt_suffix, show_default, "Y/n" if default else "y/N")

	while True:
		try:  # pylint: disable=loop-try-except-usage
			value = _prompt(prompt, err=err, hide_input=False).lower().strip()
		except (KeyboardInterrupt, EOFError):
			raise click.Abort()

		if value in ('y', "yes"):
			rv = True
		elif value in ('n', "no"):
			rv = False
		elif value == '':
			rv = default
		else:
			click.echo("Error: invalid input", err=err)
			continue
		break

	if abort and not rv:
		raise click.Abort()

	return rv


def stderr_input(prompt: str = '', file: IO = sys.stdout) -> str:  # pragma: no cover
	"""
	Read a string from standard input, but prompt to standard error.

	The trailing newline is stripped.
	If the user hits EOF (Unix: :kbd:`Ctrl-D`, Windows: :kbd:`Ctrl-Z+Return`), raise :exc:`EOFError`.

	On Unix, GNU readline is used if enabled.

	The ``prompt`` string, if given, is printed to stderr without a trailing newline before reading.
	"""

	if file is sys.stdout:
		return input(prompt)

	try:
		stdin = sys.stdin
	except AttributeError:
		raise RuntimeError("stderr_input: lost sys.stdin")

	file.write(prompt)

	try:
		flush = file.flush
	except AttributeError:
		pass
	else:
		flush()

	try:
		file.softspace = 0  # type: ignore[attr-defined]
	except (AttributeError, TypeError):
		pass

	line = stdin.readline()

	if not line:  # inputting an empty line gives line == '\n'
		raise EOFError
	elif line[-1] == '\n':
		return line[:-1]

	return line


def _prompt(text: Any, err: bool, hide_input: bool):  # noqa: MAN002
	if sys.platform != "linux":
		# Write the prompt separately so that we get nice
		# coloring through colorama on Windows
		click.echo(text, nl=False, err=err)
		text = ''

	if hide_input:
		return hidden_prompt_func(text)
	elif err:
		return stderr_input(text, file=sys.stderr)
	else:
		return click.termui.visible_prompt_func(text)


@overload
def choice(
		options: List[str],
		text: str = ...,
		default: Optional[str] = ...,
		prompt_suffix: str = ...,
		show_default: bool = ...,
		err: bool = ...,
		start_index: int = ...
		) -> int: ...


@overload
def choice(
		options: Mapping[str, str],
		text: str = ...,
		default: Optional[str] = ...,
		prompt_suffix: str = ...,
		show_default: bool = ...,
		err: bool = ...,
		start_index: int = ...
		) -> str: ...


def choice(
		options: Union[List[str], Mapping[str, str]],
		text: str = '',
		default: Optional[str] = None,
		prompt_suffix: str = ": ",
		show_default: bool = True,
		err: bool = False,
		start_index: int = 0
		) -> Union[str, int]:
	"""
	Prompts a user for input.

	If the user aborts the input by sending an interrupt signal, this
	function will catch it and raise a :exc:`click.Abort` exception.

	:param options:
	:param text: The text to show for the prompt.
	:param default: The index of the default value to use if the user does not enter anything.
		If this is not given it will prompt the user until aborted.
	:param prompt_suffix: A suffix that should be added to the prompt.
	:param show_default: Shows or hides the default value in the prompt.
	:param err: If :py:obj:`True` the file defaults to ``stderr`` instead of
		``stdout``, the same as with echo.
	:param start_index: If ``options`` is a list of values, sets the start index.
	"""

	# TODO: completer for numbers?

	type_: click.ParamType

	if isinstance(options, Mapping):
		# (Y/I/N/O/D/Z) [default=N]

		text = f"{text} ({'/'.join(options.keys())})"
		type_ = click.STRING

		for choice, descripton in options.items():
			click.echo(f" {choice} : {descripton}")

	else:
		type_ = click.IntRange(start_index, len(options) + 1 - start_index)

		for idx, descripton in enumerate(options):
			idx += start_index
			click.echo(f" [{idx}] {descripton}")

	if default is not None and show_default:
		text += f" [default={default}]"

	while True:
		selection = prompt(
				text=text,
				default=default,
				type=type_,
				prompt_suffix=prompt_suffix,
				show_default=False,
				err=err,
				)
		# pylint: disable=loop-invariant-statement
		if isinstance(options, Mapping):
			selection = selection.strip().upper()
			if selection not in options:
				click.echo("Please enter a valid option.")
			else:
				return selection
		else:
			return selection - start_index
		# pylint: enable=loop-invariant-statement
