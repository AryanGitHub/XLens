from pathlib import Path
from gi.repository import GLib

username = "oumuamua"
app_name = "XLens"
loggingConfigPath = "./logging_config.json"
app_id = f"org.gnome.gitlab.{username}.{app_name}"
toast_timeout = 1  # in seconds

appDir = Path(GLib.get_user_config_dir())
configPath = appDir / "conf.json"
