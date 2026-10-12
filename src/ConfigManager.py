import os, json
from . import appLogger

logger = appLogger.getLogger(__name__)

DEFAULT_CONFIGS = {
    "Enable_Save_Images": False,
    #    "Save_Images_Path": None,
    "Image_Processing_Module": "Tesseract_4",
    #    "All_Available_Image_Processing_Modules": [],
    #    "Enable_View_Image_In_Output": False,
    #    "Enabled_Langs_List": ["English"],
    #    "All_Available_Langs_List": ["English", "Hindi"],
}


class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.configs = self._load()
        logger.info("Config Manager loaded")

    def _load(self):
        if not os.path.exists(self.config_path):
            logger.info("Configs json file Do not Exist, backing to default configs")
            return DEFAULT_CONFIGS
        with open(self.config_path) as file:
            return json.load(file)

    def get(self, key: str):
        logger.debug(f"Getting key {key} from config.")
        if self.isValidKey(key):
            if key in self.configs:
                return self.configs[key]
            else:
                self.configs[key] = DEFAULT_CONFIGS[key]
                logger.debug(f"key not found in config, using default configs")
                return self.configs[key]
        else:
            logger.critical("config key not found")
            return None

    def isValidKey(self, key: str):
        if key in DEFAULT_CONFIGS:
            return True
        else:
            logger.error("Not a Valid Key to Set")
            return False

    def set(self, key: str, value):
        logger.debug(f"Setting key {key} from config to value {value}.")
        if self.isValidKey(key):
            if self.configs.get(key) != None:
                if self.configs[key] != value:
                    self.configs[key] = value
                    self.save()
            else:
                self.configs[key] = value
                self.save()

    def save(self):
        try:
            with open(self.config_path, "w") as json_file:
                json.dump(self.configs, json_file, indent=4)
        except Exception as e:
            logger.critical(f"Unable of save config File. Error = {e}")
