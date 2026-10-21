# main.py
#
# Copyright 2026 Oumuamua
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi

from gettext import gettext as _

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Xdp", "1.0")
gi.require_version("XdpGtk4", "1.0")

from gi.repository import Gtk, Adw, Gio
from gi.events import GLibEventLoopPolicy
import asyncio
from . import appLogger
from .window import XlensMainWindow

appLogger.configure_app_logging()
logger = appLogger.getLogger(__name__)


class XlensApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self, version):
        super().__init__(
            application_id="org.gnome.gitlab.oumuamua.XLens",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
            resource_base_path="/org/gnome/gitlab/oumuamua/XLens",
        )
        self.version = version
        logger.info("App started.")
        logger.info(f"Application_id={self.get_application_id()}")
        logger.info(f"Application version : {self.version}")
        self.create_action("quit", lambda *_: self.quit(), ["<control>q"])
        self.create_action("about", self.on_about_action)
        self.create_action("preferences", self.on_preferences_action)

        self.set_accels_for_action("win.open", ["<Ctrl>o"])
        logger.debug("Setting Ctrl+O to action 'open'")
        self.set_accels_for_action("win.paste", ["<Ctrl>v"])
        logger.debug("Setting Ctrl+P to action 'paste'")

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = XlensMainWindow(application=self)
            logger.info("Main Window Initilised")
        win.present()

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutDialog(
            application_name="XLens",
            application_icon="org.gnome.gitlab.oumuamua.XLens",
            developer_name="Oumuamua",
            version=self.version,
            # Translators: Replace "translator-credits" with your name/username, and optionally an email or URL.
            translator_credits=_("translator-credits"),
            developers=["Oumuamua"],
            copyright="© 2026 Oumuamua",
        )
        about.present(self.props.active_window)

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print("app.preferences action activated")

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    asyncio.set_event_loop_policy(GLibEventLoopPolicy())

    app = XlensApplication(version)
    return app.run(sys.argv)
