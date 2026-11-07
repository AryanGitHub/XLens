import gi

gi.require_version("Gdk", "4.0")
import asyncio
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor
from enum import Enum

from gi.repository import Gdk, Gtk
from PIL import Image, UnidentifiedImageError

from . import TextExtractor, app_utils, appLogger
from .ConfigManager import ConfigManager
from .constants import configPath
from .OutputViewer import OutputViewerWindow as OVW

logger = appLogger.getLogger(__name__)


class SetImageException(Exception):
    pass


class ImageProcessingContext:
    class ImageInputSourceType(Enum):
        FILE_PATH = 1
        URL = 2
        IMAGE = 3

    def __init__(self, path: str, application: Gtk.Application):
        self.image: Image | None = None
        self.outputText: str | None = None
        self.errorStatus = None
        self.application: Gtk.Application = application
        logger.debug(f"ImageProcessingContext initialized. {self}")

    @app_utils.debug_log
    async def getText(self) -> str:

        if not self.image:
            logger.error("self.image is None, cannot Proceed further to extract text.")
            raise TextExtractor.ImageProcessingException("Image Not Found")

        elif not self.outputText:
            logger.info(
                f"Current Image Processing Module going to be used is: {ConfigManager.get_string('image-processing-module')}"
            )
            try:
                task = None
                match ConfigManager.get_string("image-processing-module"):
                    case "Tesseract_4":
                        task = TextExtractor.getTextFromTesseract4
                    # case "EasyOCR_version": #dream cases
                    #    task = getTextFromEasyOCR()
                    case _:
                        logger.critical(
                            "Unrecognised Image Processing Module. Should be unreachable. Something wrong in code."
                        )
                        raise TextExtractor.ImageProcessingException(
                            "Unrecognised Image Processing Module"
                        )
                event_loop = asyncio.get_running_loop()
                with ProcessPoolExecutor() as executor:
                    logger.debug("Setting new Process to extract Text.")
                    self.outputText = await event_loop.run_in_executor(
                        executor, task, self.image
                    )

                self.outputText = self.outputText.strip()
                if not self.outputText:
                    raise TextExtractor.ImageProcessingException("No Text To Extract")

                if (self.outputText is not None) and (
                    not ConfigManager.get_boolean("view-image-in-output")
                ):
                    logger.debug(
                        "Image already Processed, and 'view-image-in-output' is False, so the Image is not required further, hence releasing the memory."
                    )
                    self.image = None

                return self.outputText

            except TextExtractor.ImageProcessingException as ipe:
                logger.error(
                    f"Error Occurred during Image Processing. Error Message: {ipe}"
                )
                raise  # for correct toast error

    @app_utils.debug_log
    def setImageFromUrl(self, url: str) -> None:
        import urllib.error
        import urllib.request
        from io import BytesIO

        logger.info(f"URL To get Image From {url}")
        try:
            with urllib.request.urlopen(url) as response:
                image_data = response.read()
                logger.debug(f"successfully got response. Response = {response}")
                self.image = Image.open(BytesIO(image_data))
                logger.info("successfully set Image from URL")
        # --- AI-assisted (modified) start ---
        except urllib.error.URLError as e:
            logger.error(f"Network error while fetching image from {url}: {e}")
            raise SetImageException("Network error")
        except ValueError as ve:
            logger.error(f"Invalid URL {ve}.")
            raise SetImageException("Invalid URL")
        # --- AI-assisted (modified) end ---
        except (UnidentifiedImageError, OSError) as e:
            logger.error(
                f"Failed to process the downloaded image data: {e}. The type of Exception is {type(e)}"
            )
            raise SetImageException("Invalid Image Data") from e

    @app_utils.debug_log
    def setImageFromFilePath(self, filePath: str) -> None:

        logger.info(f"File Path To get Image From {filePath}")

        try:
            self.image = Image.open(filePath)
            logger.info(f"successfully set Image from File Path: {filePath}")
        except (FileNotFoundError, PermissionError) as e:
            logger.error(f"Unable to access file at {filePath}, Error : {e}")
            raise SetImageException("Unable to access Image") from e
        except UnidentifiedImageError as e:
            logger.error(f"File {filePath} is not valid Image, Error : {e}")
            raise SetImageException("Invalid image format") from e
        except OSError as e:
            logger.error(
                f"Unable to load Image from filePath: {filePath}, got Exception : {e}"
            )
            raise SetImageException("Unable to load Image") from e

    @app_utils.debug_log
    def setImageFromImage(self, image: Image) -> None:

        self.image = image
        logger.info(f"successfully set Image from Another Image {self.image}")

    @app_utils.debug_log
    def setOutputWindowPresent(self) -> None:
        if self.outputText:
            # get ID as static variable, that gets updated for every of this call
            self.outputWindow = OVW(application=self.application)
            self.outputWindow.setOutputText(self.outputText)
            self.outputWindow.present()
        else:
            logger.error("Output Text is Empty")

    @staticmethod
    @app_utils.debug_log
    async def getOutput(
        inputSourceType: ImageInputSourceType,
        source: str | Image | None,
        errorCallbackFunction: Callable[[str], None],
        application: Gtk.Application,
    ) -> bool:
        logger.debug(f"Image source type {inputSourceType}")
        ipc: ImageProcessingContext = ImageProcessingContext(configPath, application)
        try:
            match inputSourceType:
                case ImageProcessingContext.ImageInputSourceType.FILE_PATH:
                    ipc.setImageFromFilePath(source)
                case ImageProcessingContext.ImageInputSourceType.URL:
                    ipc.setImageFromUrl(source)
                case ImageProcessingContext.ImageInputSourceType.IMAGE:
                    ipc.setImageFromImage(source)
                case _:
                    logger.critical(
                        "Unrecognised Image Source. Should be unreachable. Something wrong in code."
                    )
                    raise SetImageException("Unrecognised Image Source")
        except SetImageException as e:
            errorCallbackFunction(str(e))
        else:
            try:
                await ipc.getText()
                ipc.setOutputWindowPresent()
                if ConfigManager.get_boolean("auto-copy-output-text"):
                    logger.debug("Setting output text to clipboard.")
                    clipboard = Gdk.Display.get_default().get_clipboard()
                    clipboard.set(ipc.outputText)
                return True
            except (TextExtractor.ImageProcessingException, KeyError) as e:
                logger.error(f"Error: {e!s}")
                errorCallbackFunction(str(e))
                # maybe try another model??

        finally:
            pass
