from . import appLogger

logger = appLogger.getLogger(__name__)

from PIL import Image


class ImageProcessingException(Exception):
    pass


def getTextFromTesseract4(image: Image) -> str:
    try:
        import pytesseract
    except ImportError as e:
        logger.error(f"pytesseract not installed = {e}")
        raise ImageProcessingException("pytesseract not installed") from e

    try:
        return pytesseract.image_to_string(image)
    except (
        pytesseract.TesseractError,
        pytesseract.TesseractNotFoundError,
        RuntimeError,
    ) as e:
        logger.error(f"Unable to Process Image via Tesseract4, error message = {e}")
        raise ImageProcessingException("unable to Process Image via Tesseract4") from e
