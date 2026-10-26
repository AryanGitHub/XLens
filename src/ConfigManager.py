from gi.repository import Gio

from . import appLogger, constants

logger = appLogger.getLogger(__name__)
ConfigManager = Gio.Settings.new(constants.app_id)
