import logging

from . import logs
from .logs import logger



def set_logger_debug_mode(logger:logging.Logger):
    """ Set the debug mode of the logger """
    logs.set_format(logger=logger, format=f"[%(name)s] %(asctime)s %(module)-8s %(lineno)-3d  %(message)s")
    logger.setLevel(logging.DEBUG)

logger.setLevel(level=logging.INFO)
