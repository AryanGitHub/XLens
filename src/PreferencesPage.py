import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, Gtk

from . import appLogger
from .ConfigManager import ConfigManager

logger = appLogger.getLogger(__name__)

import gettext

_ = gettext.gettext


@Gtk.Template(resource_path="/org/gnome/gitlab/oumuamua/XLens/PreferencesPage.ui")
class PreferencesPage(Adw.NavigationPage):
    __gtype_name__ = "PreferencesPage"

    switch_auto_copy = Gtk.Template.Child()
    switch_save_screenshot = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("XLens - " + _("Preferences"))
        logger.info("Settings Window Initialized")
        self._bind_switch_auto_copy()
        self._bind_switch_save_screenshot()

    def _bind_switch_auto_copy(self) -> None:
        ConfigManager.bind(
            "auto-copy-output-text",
            self.switch_auto_copy,
            "active",
            Gio.SettingsBindFlags.DEFAULT,
        )

    def _bind_switch_save_screenshot(self) -> None:
        ConfigManager.bind(
            "delete-taken-screenshot-image",
            self.switch_save_screenshot,
            "active",
            # --- AI-assisted (modified) start ---
            Gio.SettingsBindFlags.DEFAULT | Gio.SettingsBindFlags.INVERT_BOOLEAN,
            # --- AI-assisted (modified) end ---
        )
