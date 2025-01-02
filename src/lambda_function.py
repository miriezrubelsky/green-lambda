
import logging
from image_handler import ImageHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def handler(event, context):
    imagehandler = ImageHandler(event, context)
    return imagehandler.process()