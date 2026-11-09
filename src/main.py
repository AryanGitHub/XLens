# main.py
#
# Copyright 2026 Aryan Pandey
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
from gettext import gettext as _

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Xdp", "1.0")
gi.require_version("XdpGtk4", "1.0")

import asyncio

from gi.events import GLibEventLoopPolicy
from gi.repository import Adw, Gio, Gtk

from . import app_utils, appLogger
from .window import XlensMainWindow

appLogger.configure_app_logging()
logger = appLogger.getLogger(__name__)


class XlensApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self, version: str):
        super().__init__(
            application_id="org.gnome.gitlab.Oumuamua.XLens",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
            resource_base_path="/org/gnome/gitlab/Oumuamua/XLens",
        )
        self.version = version
        logger.info("App started.")
        logger.info(f"Application_id={self.get_application_id()}")
        logger.info(f"Application version : {self.version}")
        app_utils.create_action(self, "quit", lambda *_: self.quit(), ["<control>q"])
        app_utils.create_action(self, "about", self.on_about_action)
        app_utils.create_action(self, "preferences", self.on_preferences_action)

    @app_utils.debug_log
    def do_activate(self) -> None:
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = XlensMainWindow(application=self)
            logger.info("Main Window Initilised")
        win.present()

    @app_utils.debug_log
    def on_about_action(self, *args) -> None:
        """Callback for the app.about action."""
        about = Adw.AboutDialog(
            application_name="XLens",
            application_icon="org.gnome.gitlab.Oumuamua.XLens",
            developer_name="Aryan Pandey (@Oumuamua)",
            version=self.version,
            # Translators: Replace "translator-credits" with your name/username, and optionally an email or URL.
            # translator_credits=_("translator-credits"),
            developers=["Aryan Pandey (@Oumuamua) https://gitlab.gnome.org/Oumuamua"],
            copyright="© 2026 Aryan Pandey",
            license_type=Gtk.License.GPL_3_0,
            issue_url="https://gitlab.gnome.org/Oumuamua/XLens/-/issues",
            website="https://gitlab.gnome.org/Oumuamua/XLens",
        )
        about.present(self.props.active_window)

    @app_utils.debug_log
    def on_preferences_action(self, widget, _) -> None:
        """Callback for the app.preferences action."""
        print("app.preferences action activated")


@app_utils.debug_log
def main(version: str):
    """The application's entry point."""
    # --- AI-assisted (modified) start ---
    asyncio.set_event_loop_policy(GLibEventLoopPolicy())
    # --- AI-assisted (modified) end ---

    app = XlensApplication(version)
    return app.run(sys.argv)
