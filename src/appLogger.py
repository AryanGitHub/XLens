import logging.config
import pathlib, json
from gi.repository import Gio
from .constants import loggingConfigPath, app_id


def configure_app_logging():

    gbytes = Gio.resources_lookup_data(
        "/org/gnome/gitlab/oumuamua/XLens/logging_config.json",
        Gio.ResourceLookupFlags.NONE,
    )

    logging_config_content_json = gbytes.get_data().decode("utf-8")
    config = json.loads(logging_config_content_json)
    logging.config.dictConfig(config)


def getLogger(name):
    return logging.getLogger(f"{app_id}.{name}")
