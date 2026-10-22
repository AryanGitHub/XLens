import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk

from . import appLogger
from .ConfigManager import ConfigManager
from .constants import configPath
from .ImageProcessingContext import ImageProcessingContext as IPC

logger = appLogger.getLogger(__name__)


@Gtk.Template(resource_path="/org/gnome/gitlab/oumuamua/XLens/FromURLPage.ui")
class FromURLPage(Adw.NavigationPage):
    __gtype_name__ = "FromURLPage"
    configManager = ConfigManager(configPath)

    URL_entry = Gtk.Template.Child()

    def __init__(
        self, app_nav_view, application, getErrorCallbackGenerateToastFunction
    ):
        super().__init__()

        self.app_nav_view = app_nav_view
        self.application = application
        self.getErrorCallbackGenerateToastFunction = (
            getErrorCallbackGenerateToastFunction
        )

        logger.info(f"'FromURL' Page Initialized")

    def on_back_from_url_page(self, nav_view, popped_page):
        # clear search buffer when back button is pressed.
        if popped_page.get_tag() == "from_url_page":
            self.URL_entry.set_text("")

    @Gtk.Template.Callback()
    def on_extract_text_from_url_button_clicked(self, entry):
        logger.debug(f"Extract text from URL button clicked")
        url_link = self.URL_entry.get_text().strip()
        logger.debug(f"URL link from search entry : {url_link}")
        if not url_link:
            logger.error(f"URL link from search entry is empty")
            self.getErrorCallbackGenerateToastFunction()("Empty URL Entry")
        else:
            sourceType = IPC.ImageInputSourceType.URL
            result_success = IPC.getOutput(
                sourceType,
                url_link,
                self.getErrorCallbackGenerateToastFunction(),
                self.application,
            )
            if result_success:
                self.URL_entry.set_text("")
                ret = self.app_nav_view.pop()
                logger.debug(
                    f"returned to main screen : {ret} , entry buffered cleared."
                )
