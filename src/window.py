# window.py
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

from collections.abc import Callable

from gi.repository import Adw, Gdk, Gio, GLib, Gtk, Xdp, XdpGtk4

from . import appLogger
from .constants import toast_timeout
from .FromURLPage import FromURLPage
from .ImageProcessingContext import ImageProcessingContext as IPC
from .PreferencesPage import PreferencesPage

appLogger.configure_app_logging()
logger = appLogger.getLogger(__name__)

import gettext

_ = gettext.gettext


@Gtk.Template(resource_path="/org/gnome/gitlab/oumuamua/XLens/window.ui")
class XlensMainWindow(Adw.ApplicationWindow):
    __gtype_name__ = "XlensMainWindow"

    portal = Xdp.Portal()
    app_nav_view = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        logger.info(
            f"Currently displayed Navigation Page is '{self.app_nav_view.get_visible_page().get_tag()}'"
        )

        open_action = Gio.SimpleAction(name="open")
        open_action.connect("activate", self.open_file_dialog)
        self.add_action(open_action)
        logger.info(
            f"Added action '{open_action.get_name()}' and connected to function '{self.open_file_dialog.__name__}'"
        )

        paste_action = Gio.SimpleAction(name="paste")
        paste_action.connect("activate", self.start_paste_procedure)
        self.add_action(paste_action)
        logger.info(
            f"Added action '{paste_action.get_name()}' and connected to function '{self.start_paste_procedure.__name__}'"
        )

        self.connect("close-request", self.on_close_request)

        self.restrict_actions_to_main_page()

        self.PreferencesPage = PreferencesPage()
        self.app_nav_view.add(self.PreferencesPage)

        self.FromURLPage = FromURLPage(
            app_nav_view=self.app_nav_view,
            application=self.get_application(),
            getErrorCallbackGenerateToastFunction=self.getErrorCallbackGenerateToastFunction,
        )
        self.app_nav_view.add(self.FromURLPage)

        self.app_nav_view.connect("popped", self.FromURLPage.on_back_from_url_page)

    def on_close_request(self, window) -> bool:

        self.get_application().quit()

        # Return False so GTK handles the default window destruction
        return False

    def open_file_dialog(self, action, parameter) -> None:
        logger.info("Open Action Started.")

        def on_open_response(dialog: Gtk.FileDialog, result: Gio.AsyncResult) -> None:
            try:
                file: Gio.File | None = dialog.open_finish(result)
                # If the user selected a file...
                if file is not None:
                    # ... open it
                    logger.info(f"File Selected. {file}")
                    open_file(file)
            except GLib.Error as err:
                self.getErrorCallbackGenerateToastFunction()("User Cancelled")
                logger.error(f"Gtk File Dialog Error: {err!s}")

        def open_file(file: Gio.File) -> None:
            file_path = file.peek_path()
            logger.info(f"file path = {file_path}")
            sourceType = IPC.ImageInputSourceType.FILE_PATH
            IPC.getOutput(
                sourceType,
                file_path,
                self.getErrorCallbackGenerateToastFunction(),
                self.get_application(),
            )

        # Create a new file selection dialog, using the "open" mode
        native = Gtk.FileDialog()
        native.open(self, None, on_open_response)
        logger.info("Gtk File Dialog Opened")

    def start_paste_procedure(self, action, parameter) -> None:

        logger.debug("started paste action")

        from io import BytesIO

        from PIL import Image

        # 1. Get the clipboard from the default display
        clipboard = Gdk.Display.get_default().get_clipboard()

        # 3. This callback runs when the clipboard data is ready
        def on_paste_image(clipboard, result) -> None:
            try:
                # Retrieve the Gdk.Texture from the async result
                texture = clipboard.read_texture_finish(result)

                if texture is not None:
                    # Convert the texture to a GLib.Bytes object containing PNG data
                    gbytes = texture.save_to_png_bytes()

                    # Extract the raw python bytes using .get_data() and wrap in BytesIO
                    img = Image.open(BytesIO(gbytes.get_data()))
                    logger.debug(
                        f"Success! Loaded {img.format} image of size {img.size}"
                    )
                    sourceType = IPC.ImageInputSourceType.IMAGE
                    IPC.getOutput(
                        sourceType,
                        img,
                        self.getErrorCallbackGenerateToastFunction(),
                        self.get_application(),
                    )

                else:
                    logger.info("No image data found on the clipboard.")
                    raise Exception("No image data found on the clipboard")

            except Exception as e:
                logger.info(f"Error reading clipboard: {e}")
                self.getErrorCallbackGenerateToastFunction()("Error reading clipboard")

        # 2. Request the image asynchronously
        # (Passing 'None' for the cancellable, and our callback function)
        clipboard.read_texture_async(None, on_paste_image)

    @Gtk.Template.Callback()
    def menu_button_clicked(self, button) -> None:
        logger.info("Preferences button clicked.")
        self.app_nav_view.push_by_tag("preferences_page")

    @Gtk.Template.Callback()
    def take_screenshot_button_clicked(self, button) -> None:
        logger.debug("take screenshot button clicked")

        def take_screenshot_callback_function(portal, result, user_data) -> None:
            try:
                image_uri = portal.take_screenshot_finish(result)

                logger.info(
                    f"Screenshot successfully saved by the system to: {image_uri}"
                )

                sourceType = IPC.ImageInputSourceType.URL
                IPC.getOutput(
                    sourceType,
                    image_uri,
                    self.getErrorCallbackGenerateToastFunction(),
                    self.get_application(),
                )

            except GLib.Error as e:
                logger.error(f"Screenshot canceled or failed: {e.message}")

        try:
            parent = XdpGtk4.parent_new_gtk(self)
            self.portal.take_screenshot(
                parent,
                Xdp.ScreenshotFlags.INTERACTIVE,
                None,
                take_screenshot_callback_function,
                None,
            )
        except Exception as e:
            logger.error(f"Failed to initiate screenshot: {e}")

    @Gtk.Template.Callback()
    def from_url_button_clicked(self, button) -> None:
        logger.info(f"{button} clicked.")
        self.app_nav_view.push_by_tag("from_url_page")
        logger.info("Pushed to 'from_url_page'")

    def restrict_actions_to_main_page(self) -> None:
        def on_visible_page_changed(nav_view, param_spec, window):

            current_page = nav_view.get_visible_page()
            paste_action = window.lookup_action("paste")
            open_action = window.lookup_action("open")

            if not paste_action or not current_page:
                return
            if current_page.get_tag() == "main_page":
                paste_action.set_enabled(True)
                open_action.set_enabled(True)
            else:
                paste_action.set_enabled(False)
                open_action.set_enabled(False)

        self.app_nav_view.connect("notify::visible-page", on_visible_page_changed, self)
        logger.info(
            "Successfully, put the restrictions of actions to only work on main page."
        )

    def getErrorCallbackGenerateToastFunction(self) -> Callable[[str, int], None]:
        toast_overlay = self.toast_overlay

        def errorCallbackGenerateToastFunction(
            message: str, timeout: int = toast_timeout
        ) -> None:
            toast = Adw.Toast.new(message)
            toast.set_timeout(timeout)
            toast_overlay.add_toast(toast)

        return errorCallbackGenerateToastFunction
