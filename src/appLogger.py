import json
import logging.config
from logging import Logger

from gi.repository import Gio

from .constants import app_id


def configure_app_logging() -> None:

    # --- AI-assisted (modified) start ---
    gbytes = Gio.resources_lookup_data(
        "/org/gnome/gitlab/oumuamua/XLens/logging_config.json",
        Gio.ResourceLookupFlags.NONE,
    )
    # --- AI-assisted (modified) end ---

    logging_config_content_json: str = gbytes.get_data().decode("utf-8")
    config: dict = json.loads(logging_config_content_json)
    logging.config.dictConfig(config)


def getLogger(name: str) -> Logger:
    return logging.getLogger(f"{app_id}.{name}")
