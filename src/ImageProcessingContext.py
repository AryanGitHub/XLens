from collections.abc import Callable
from enum import Enum

from gi.repository import Gtk
from PIL import Image

from . import appLogger
from .ConfigManager import ConfigManager
from .constants import configPath
from .OutputViewer import OutputViewerWindow as OVW

logger = appLogger.getLogger(__name__)


class SetImageException(Exception):
    pass


class ImageProcessingException(Exception):
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

    def getText(self) -> str:
        logger.debug("getText method called.")
        if not self.image:
            logger.error("self.image is None, cannot Proceed further to extract text.")
            raise ImageProcessingException("Image Not Found")

        elif not self.outputText:
            logger.info(
                f"Current Image Processing Module going to be used is: {ConfigManager.get_string('image-processing-module')}"
            )
            try:
                match ConfigManager.get_string("image-processing-module"):
                    case "Tesseract_4":
                        self.outputText = self.getTextFromTesseract4()
                    # case "EasyOCR_version": #dream case
                    #    self.outputText = getTextFromEasyOCR(self.image)
                    case _:
                        logger.critical(
                            "Should be unreachable. Something wrong in code."
                        )

                self.outputText = self.outputText.strip()
                if self.outputText:
                    logger.info(
                        f"Output Extracted Text from Image is {self.outputText}"
                    )
                else:
                    raise ImageProcessingException("No Text To Extract")

                if (self.outputText is not None) and not ConfigManager.get_boolean(
                    "view-image-in-output"
                ):
                    logger.debug(
                        "Image already Processed, and 'view-image-in-output' is False, so the Image is not required further, hence releasing the memory."
                    )
                    self.image = None

                return self.outputText

            except ImageProcessingException as ipe:
                logger.error(
                    f"Error Occurred during Image Processing. Error Message: {ipe}"
                )
                raise  # for correct toast error

    def setImageFromUrl(self, url: str) -> None:
        import urllib.error
        import urllib.request
        from io import BytesIO

        logger.debug("Set Image from URL.")
        logger.info(f"URL To get Image From {url}")
        try:
            with urllib.request.urlopen(url) as response:
                image_data = response.read()
                logger.debug(f"successfully got response. Response = {response}")
                self.image = Image.open(BytesIO(image_data))
                logger.info("successfully set Image from URL")
        except urllib.error.URLError as e:
            logger.error(f"Network error while fetching image from {url}: {e}")
            raise SetImageException("Network error")
        except ValueError as ve:
            logger.error(f"Invalid URL {ve}.")
            raise SetImageException("Invalid URL")
        except Exception as e:
            logger.error(
                f"Failed to process the downloaded image data: {e}. The type of Exception is {type(e)}"
            )
            raise SetImageException("Invalid Image Data")

    def setImageFromFilePath(self, filePath: str) -> None:
        import os.path

        logger.debug("Set Image from FilePath")
        logger.info(f"File Path To get Image From {filePath}")

        if not os.path.isfile(filePath):
            logger.error("FilePath is not a file.")
            raise SetImageException("Invalid FilePath")
        else:
            try:
                self.image = Image.open(filePath)
                logger.info(f"successfully set Image from File Path: {filePath}")
            except Exception as e:
                logger.error(
                    f"Unable to load Image from filePath: {filePath}, got Exception : {e}"
                )
                raise SetImageException("Unable to load Image")

    def setImageFromImage(self, image: Image) -> None:
        logger.debug("Set Image from another Image")
        self.image = image
        logger.info(f"successfully set Image from Another Image {self.image}")

    def getTextFromTesseract4(self) -> str:
        try:
            import pytesseract

            # should happen async
            return pytesseract.image_to_string(self.image)
        except Exception as e:
            logger.error(f"Unable to Process Image via Tesseract4, error message = {e}")
            raise ImageProcessingException("unable to Process Image via Tesseract4")

    def setOutputWindowPresent(self) -> None:
        if self.outputText:
            # get ID as static variable, that gets updated for every of this call
            self.outputWindow = OVW(application=self.application)
            self.outputWindow.setOutputText(self.outputText)
            self.outputWindow.present()
        else:
            logger.error("Output Text is Empty")

    @staticmethod
    def getOutput(
        inputSourceType: ImageInputSourceType,
        source: str | Image | None,
        errorCallbackFunction: Callable[[str], None],
        application: Gtk.Application,
    ) -> None:
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
                    logger.critical("Should be unreachable. Something wrong in code.")
        except SetImageException as e:
            logger.info("Error Callback Function called.")
            errorCallbackFunction(str(e))
            logger.debug("Exiting from Callback")
        else:
            try:
                ipc.getText()
                ipc.setOutputWindowPresent()
                return True
            except ImageProcessingException as ipe:
                logger.info("Error Callback Function called.")
                errorCallbackFunction(str(ipe))
                logger.debug("Exiting from Callback")
                # maybe try another model??
            except Exception as e:
                logger.info("Error Callback Function called.")
                errorCallbackFunction(str(e))
                logger.debug("Exiting from Callback")
        finally:
            pass
