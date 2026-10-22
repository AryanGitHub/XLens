import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk

from . import appLogger
from .ConfigManager import ConfigManager
from .constants import configPath

logger = appLogger.getLogger(__name__)

import gettext

_ = gettext.gettext


@Gtk.Template(resource_path="/org/gnome/gitlab/oumuamua/XLens/PreferencesPage.ui")
class PreferencesPage(Adw.NavigationPage):
    __gtype_name__ = "PreferencesPage"
    configManager = ConfigManager(configPath)

    switch_auto_copy = Gtk.Template.Child()
    switch_save_screenshot = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("XLens - " + _("Preferences"))
        logger.info("Settings Window Initialized")
        self._load_switch_auto_copy()
        self._connect_switch_auto_copy()

    def _load_switch_auto_copy(self) -> None:
        value: str = self.configManager.get("Enable_Save_Images")
        self.switch_auto_copy.set_active(value)
        logger.debug(f"Loaded Settings 'switch_auto_copy' to '{value}'")

    def _connect_switch_auto_copy(self) -> None:
        def callback(switch_row: Gtk.Switch, pspec):
            is_active = switch_row.props.active
            self.configManager.set("Enable_Save_Images", is_active)

        self.switch_auto_copy.connect("notify::active", callback)
