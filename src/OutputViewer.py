import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gdk, Gio
from . import appLogger

logger = appLogger.getLogger(__name__)


@Gtk.Template(resource_path="/org/gnome/gitlab/oumuamua/XLens/OutputViewer.ui")
class OutputViewerWindow(Adw.ApplicationWindow):
    __gtype_name__ = "OutputViewerWindow"
    outputTextView = Gtk.Template.Child()
    ID = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        OutputViewerWindow.ID = OutputViewerWindow.ID + 1
        self.set_title(f"Output {OutputViewerWindow.ID}")
        logger.info(f"Output Window Initialized, title = '{self.get_title()}'")

    def setOutputText(self, text: str):
        buffer = self.outputTextView.get_buffer()
        buffer.set_text(text)
        logger.debug("Successfully set text on output window.")
