#!/usr/bin/env python3
#
#  tracebacks.py
"""
Functions for handling exceptions and their tracebacks.

.. versionadded:: 1.0.0
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
from typing import Callable, ContextManager, Type, TypeVar

# 3rd party
import click
from domdf_python_tools.compat import nullcontext

__all__ = ["TracebackHandler", "handle_tracebacks", "traceback_handler", "traceback_option"]

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

	How these exceptions are handled can be changed, and supported can be added for
	further exception classes by subclassing this class.
	Each method is named in the form :file:`handle_{<exception>}`, where ``exception``
	is the name of the exception class to handle.

	.. versionadded:: 1.0.0

	.. seealso:: :func:`~.handle_tracebacks`.
	"""  # noqa: D400

	def handle_EOFError(self, e: EOFError) -> bool:
		raise e

	def handle_KeyboardInterrupt(self, e: KeyboardInterrupt) -> bool:
		raise e

	def handle_ClickException(self, e: click.ClickException) -> bool:
		raise e

	def handle_Abort(self, e: click.Abort) -> bool:
		raise e

	def handle_FileNotFoundError(self, e: FileNotFoundError) -> bool:

		# this package
		from consolekit.utils import abort

		raise abort(f"File Not Found: {e}")

	def handle_FileExistsError(self, e: FileExistsError) -> bool:

		# this package
		from consolekit.utils import abort

		raise abort(f"File Exists: {e}")

	def handle(self, e: Exception) -> bool:

		# this package
		from consolekit.utils import abort

		if hasattr(self, f"handle_{e.__class__.__name__}"):
			return getattr(self, f"handle_{e.__class__.__name__}")(e)

		for base in e.__class__.__mro__:
			if hasattr(self, f"handle_{base.__name__}"):
				return getattr(self, f"handle_{base.__name__}")(e)

		raise abort(f"An error occurred: {e}")

	@contextlib.contextmanager
	def __call__(self):
		try:
			yield
		except Exception as e:
			self.handle(e)


@contextlib.contextmanager
def traceback_handler():
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

	.. seealso::

		* :func:`~.handle_tracebacks`
		* :class:`~.TracebackHandler`
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

	.. versionchanged:: 1.0.0  Added the ``cls`` parameter.

	.. seealso::

		* :func:`~.traceback_handler`
		* :class:`~.TracebackHandler`
	"""

	if show_traceback:
		return nullcontext()
	else:
		return cls()()


def traceback_option(help_text="Show the complete traceback on error.") -> Callable[[_C], _C]:
	"""
	Decorator to add the ``-T / --traceback`` option to a click command.

	The value is exposed via the parameter ``show_traceback``: :class:`bool`.

	.. versionadded:: 1.0.0

	:param help_text: The help text for the option.
	"""

	# this package
	from consolekit.options import flag_option

	return flag_option("-T", "--traceback", "show_traceback", help=help_text)
