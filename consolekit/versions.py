#!/usr/bin/env python3
#
#  versions.py
"""
Tool to get software versions.

.. versionadded:: 1.6.0
"""
#
#  Copyright © 2023 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import platform
import sys
import textwrap
from typing import Any, Callable, Iterable, Mapping, Union

# 3rd party
import click
from domdf_python_tools.compat import importlib_metadata
from domdf_python_tools.stringlist import StringList
from domdf_python_tools.words import LF

__all__ = ("get_formatted_versions", "get_version_callback")


def get_formatted_versions(
		dependencies: Union[Iterable[str], Mapping[str, str]] = (),
		show_python: bool = True,
		show_platform: bool = True,
		) -> StringList:
	"""
	Return the versions of software dependencies, one per line.

	:param dependencies: Either a list of dependency names,
	    or a mapping of dependency name to a more human-readable form.
	:param show_python:
	:param show_platform:
	"""

	versions = StringList()

	if not isinstance(dependencies, Mapping):
		dependencies = {d: d for d in dependencies}

	for dependency_name, display_name in dependencies.items():

		dep_version = importlib_metadata.version(dependency_name)
		versions.append(f"{display_name}: {dep_version}")

	if show_python:
		versions.append(f"Python: {sys.version.replace(LF, ' ')}")

	if show_platform:
		versions.append(' '.join(platform.system_alias(platform.system(), platform.release(), platform.version())))

	return versions


def get_version_callback(
		tool_version: str,
		tool_name: str,
		dependencies: Union[Iterable[str], Mapping[str, str]] = (),
		) -> Callable[[click.Context, click.Option, int], Any]:
	"""
	Creates a callback for :class:`~.version_option`.

	With each ``--version`` argument the callback displays the package version,
	then adds the python version, and finally adds dependency versions.


	:param tool_version: The version of the tool to show the version of.
	:param tool_name: The name of the tool to show the version of.
	:param dependencies: Either a list of dependency names,
	    or a mapping of dependency name to a more human-readable form.
	"""

	def version_callback(ctx: click.Context, param: click.Option, value: int) -> None:
		"""
		Callback for displaying the package version (and optionally the Python runtime).
		"""

		if not value or ctx.resilient_parsing:
			return

		if value > 2:
			versions = textwrap.indent(
					get_formatted_versions(dependencies),  # type: ignore[arg-type]
					"  ",
					)
			click.echo(tool_name)
			click.echo(f"  Version: {tool_version}")
			click.echo(versions.rstrip())
		elif value > 1:
			python_version = sys.version.replace('\n', ' ')
			click.echo(f"{tool_name} version {tool_version}, Python {python_version}")
		else:
			click.echo(f"{tool_name} version {tool_version}")

		ctx.exit()

	return version_callback
