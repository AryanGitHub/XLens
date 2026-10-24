from . import appLogger

appLogger.configure_app_logging()
logger = appLogger.getLogger(__name__)
from collections.abc import Callable

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
