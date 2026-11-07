from . import appLogger

appLogger.configure_app_logging()
logger = appLogger.getLogger(__name__)
import asyncio
from collections.abc import Callable
from functools import wraps
from typing import Any

from gi.repository import Gio, Gtk


def create_action(
    actionMap: Gio.ActionMap,
    name: str,
    callback: Callable[..., None],
    shortcuts=None,
    app: Gtk.Application = None,
) -> None:
    """Add an application action.

    Args:
        name: the name of the action
        callback: the function to be called when the action is
                    activated
        shortcuts: an optional list of accelerators
    """
    action = Gio.SimpleAction.new(name, None)
    action.connect("activate", callback)
    actionMap.add_action(action)
    logger.debug(
        f"Added action Named: {action.get_name()} , with callback {callable.__name__}"
    )
    if shortcuts:
        if app:
            app.set_accels_for_action(f"win.{name}", shortcuts)
        else:
            actionMap.set_accels_for_action(f"app.{name}", shortcuts)
        logger.debug(f"Added shortcut '{shortcuts}' on action: '{action.get_name()}'")


def async_handler(async_function: Callable) -> Callable:
    _background_task = set()

    @wraps(async_function)
    def wrapper(*args, **kwargs) -> asyncio.Task:

        task: asyncio.Task = asyncio.create_task(async_function(*args, **kwargs))
        logger.debug(f"Async Task on Funtion: '{async_function.__name__}' called.")
        _background_task.add(task)
        task.add_done_callback(_background_task.discard)
        return task

    return wrapper


import os

XLENS_ENABLE_TRACE_LOGS = (
    os.getenv("XLENS_ENABLE_TRACE_LOGS", "False").lower() == "true"
)
logger.debug(f"ENABLE_TRACE_LOGS: {XLENS_ENABLE_TRACE_LOGS}")


if XLENS_ENABLE_TRACE_LOGS:
    import inspect

    def debug_log(func: Callable) -> Callable:

        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def wrapper(*args, **kwargs) -> Any:
                logger.debug(
                    "Async Function: '%s' called, with args=%s and kw=%s",
                    func.__name__,
                    args,
                    kwargs,
                )
                ret: Any = await func(*args, **kwargs)
                logger.debug(f"Async Function: '{func.__name__}' returned {ret}")
                return ret

            return wrapper

        else:

            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                logger.debug(
                    "Function: '%s' called, with args=%s and kw=%s",
                    func.__name__,
                    args,
                    kwargs,
                )
                ret: Any = func(*args, **kwargs)
                logger.debug(f"Function: '{func.__name__}' returned {ret}")
                return ret

            return wrapper

else:

    def debug_log(func: Callable) -> Callable:
        return func
