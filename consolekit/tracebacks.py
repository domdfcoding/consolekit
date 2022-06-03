#!/usr/bin/env python3
#
#  tracebacks.py
"""
Functions for handling exceptions and their tracebacks.

.. versionadded:: 1.0.0
.. latex:vspace:: -10px
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
import sys
from typing import TYPE_CHECKING, Callable, ContextManager, List, Type, TypeVar, Union

# 3rd party
import click
from domdf_python_tools.compat import nullcontext

if sys.version_info >= (3, 7) or TYPE_CHECKING:
	# stdlib
	from typing import NoReturn

__all__ = ("TracebackHandler", "handle_tracebacks", "traceback_handler", "traceback_option")

_C = TypeVar("_C", bound=click.Command)


class TracebackHandler:
	"""
	Context manager to abort execution with a short error message
	on the following exception types:

	* :exc:`FileNotFoundError`
	* :exc:`FileExistsError`

	Other custom exception classes inheriting from :exc:`Exception` are also handled,
	but with a generic message.

	The following exception classes are ignored:

	* :exc:`EOFError`
	* :exc:`KeyboardInterrupt`
	* :exc:`click.ClickException`
	* :exc:`SystemExit` (new in version 1.1.2)

	How these exceptions are handled can be changed, and supported can be added for
	further exception classes by subclassing this class.
	Each method is named in the form :file:`handle_{<exception>}`, where ``exception``
	is the name of the exception class to handle.

	.. versionadded:: 1.0.0

	:param exception: The exception to raise after handling the traceback.
		If not running within a click command or group you'll likely
		want to set this to :exc:`SystemExit(1) <SystemExit>`.
	:default exception: :class:`click.Abort() <click.Abort>`

	.. versionchanged:: 1.4.0  Added the ``exception`` argument.

	.. seealso:: :func:`~.handle_tracebacks`.
	.. latex:clearpage::
	"""  # noqa: D400

	exception: Exception
	"""
	The exception to raise after handling the traceback.

	.. versionadded:: 1.4.0
	"""

	def __init__(self, exception: BaseException = click.Abort()):
		self.exception: BaseException = exception  # type: ignore[assignment]

	def abort(self, msg: Union[str, List[str]]) -> "NoReturn":
		"""
		Abort the current process by calling ``self.exception``.

		.. versionadded:: 1.4.0

		:param msg: The message to write to stderr before raising the exception.
			If a list of strings the strings are concatenated (i.e. ``''.join(msg)``).
		"""

		if not isinstance(msg, str):
			msg = ''.join(msg)

		if msg:
			click.echo(msg, err=True, color=False)

		raise self.exception

	def handle_EOFError(self, e: EOFError) -> "NoReturn":  # noqa: D102
		raise e

	def handle_KeyboardInterrupt(self, e: KeyboardInterrupt) -> "NoReturn":  # noqa: D102
		raise e

	def handle_ClickException(self, e: click.ClickException) -> "NoReturn":  # noqa: D102
		raise e

	def handle_Abort(self, e: click.Abort) -> "NoReturn":  # noqa: D102
		raise e

	def handle_SystemExit(self, e: SystemExit) -> "NoReturn":  # noqa: D102
		raise e

	def handle_FileNotFoundError(self, e: FileNotFoundError) -> "NoReturn":  # noqa: D102
		self.abort(f"File Not Found: {e}")

	def handle_FileExistsError(self, e: FileExistsError) -> "NoReturn":  # noqa: D102
		self.abort(f"File Exists: {e}")

	def handle(self, e: BaseException) -> bool:
		"""
		Handle the given exception.

		:param e:
		"""

		exception_name = e.__class__.__name__

		if hasattr(self, f"handle_{exception_name}"):
			return getattr(self, f"handle_{exception_name}")(e)

		for base in e.__class__.__mro__:
			if hasattr(self, f"handle_{base.__name__}"):
				return getattr(self, f"handle_{base.__name__}")(e)

		self.abort(f"An error occurred: {e}")

	@contextlib.contextmanager
	def __call__(self):  # noqa: MAN002
		"""
		Use the :class:`~.TracebackHandler` with a :keyword:`with` block, and handle any exceptions raised within.
		"""

		try:
			yield
		except BaseException as e:
			self.handle(e)


@contextlib.contextmanager
def traceback_handler():  # noqa: MAN002
	"""
	Context manager to abort execution with a short error message on the following exception types:

	* :exc:`FileNotFoundError`
	* :exc:`FileExistsError`

	Other custom exception classes inheriting from :exc:`Exception` are also handled,
	but with a generic message.

	The following exception classes are ignored:

	* :exc:`EOFError`
	* :exc:`KeyboardInterrupt`
	* :exc:`click.ClickException`

	.. versionadded:: 0.8.0

	.. seealso:: :func:`~.handle_tracebacks` and :class:`~.TracebackHandler`
	"""  # noqa: D400

	with TracebackHandler()():
		yield


def handle_tracebacks(
		show_traceback: bool = False,
		cls: Type[TracebackHandler] = TracebackHandler,
		) -> ContextManager:
	"""
	Context manager to conditionally handle tracebacks, usually based on the value of a command line flag.

	.. versionadded:: 0.8.0

	:param show_traceback: If :py:obj:`True`, the full Python traceback will be shown on errors.
		If :py:obj:`False`, only the summary of the traceback will be shown.
		In either case the program execution will stop on error.
	:param cls: The class to use to handle the tracebacks.

	:rtype:

	.. versionchanged:: 1.0.0  Added the ``cls`` parameter.
	.. seealso:: :func:`~.traceback_handler` and :class:`~.TracebackHandler`
	"""

	if show_traceback:
		return nullcontext()
	else:
		return cls()()


def traceback_option(help_text: str = "Show the complete traceback on error.") -> Callable[[_C], _C]:
	"""
	Decorator to add the ``-T / --traceback`` option to a click command.

	The value is exposed via the parameter ``show_traceback``: :class:`bool`.

	.. versionadded:: 1.0.0

	:param help_text: The help text for the option.
	"""

	# this package
	from consolekit.options import flag_option

	return flag_option("-T", "--traceback", "show_traceback", help=help_text)
