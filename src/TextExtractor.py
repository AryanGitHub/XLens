from . import appLogger

logger = appLogger.getLogger(__name__)

from PIL import Image


class ImageProcessingException(Exception):
    pass


def getTextFromTesseract4(image: Image) -> str:
    try:
        import pytesseract

        return pytesseract.image_to_string(image)
    except Exception as e:
        logger.error(f"Unable to Process Image via Tesseract4, error message = {e}")
        raise ImageProcessingException("unable to Process Image via Tesseract4")
