import logging

from . import logs
from .logs import logger



# Logger
# loggername = appsettings.package_name
# loggerSettings = LoggerSettings(format=f'[%(name)s] %(message)s', level=logging.INFO)
# loggerSettings.set_level_style(level='debug', color='green')
# loggerSettings.set_level_style(level='info', color='white')
# logger = create_logger(name=loggername, settings=loggerSettings)

def set_logger_debug_mode(logger:logging.Logger):
    """ Set the debug mode of the logger """
    logs.set_format(logger=logger, format=f"[%(name)s] %(asctime)s %(module)-8s %(lineno)-3d  %(message)s")
    logger.setLevel(logging.DEBUG)

logger.setLevel(level=logging.INFO)
