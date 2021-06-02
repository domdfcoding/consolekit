# stdlib
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, overload

# 3rd party
import click

# this package
from consolekit import commands as commands
from consolekit import input as input  # noqa: A001  # pylint: disable=redefined-builtin
from consolekit import terminal_colours as terminal_colours
from consolekit import tracebacks as tracebacks
from consolekit import utils as utils
from consolekit.commands import SuggestionGroup as SuggestionGroup
from consolekit.options import _Option

__author__: str
__copyright__: str
__license__: str
__version__: str
__email__: str
__all__: List[str]

_C = TypeVar("_C", bound=click.Command)
_G = TypeVar("_G", bound=click.Group)

CONTEXT_SETTINGS: Dict[str, Any]

@overload
def click_command(
		name: Optional[str] = ...,
		cls: None = ...,
		**attrs: Any,
		) -> Callable[[Callable], click.Command]: ...

@overload
def click_command(
		name: Optional[str] = ...,
		cls: Type[_C] = ...,
		**attrs: Any,
		) -> Callable[[Callable], _C]: ...

@overload
def click_group(
		name: Optional[str] = ...,
		cls: None = ...,
		**attrs: Any,
		) -> Callable[[Callable], click.Group]: ...

@overload
def click_group(
		name: Optional[str] = ...,
		cls: Type[_G] = ...,
		**attrs: Any,
		) -> Callable[[Callable], _G]: ...

def option(
		*param_decls: str,
		**attrs: Any,
		) -> Callable[[_C], _C]: ...
