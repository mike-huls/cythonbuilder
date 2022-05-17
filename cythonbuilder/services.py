import logging

from cythonbuilder import appsettings
from cythonbuilder.logs import create_logger, LoggerSettings



# Logger
loggername = appsettings.package_name
loggerSettings = LoggerSettings(format=f'[%(name)s] %(message)s', level=logging.INFO)
loggerSettings.set_level_style(level='debug', color='green')
loggerSettings.set_level_style(level='info', color='white')
logger = create_logger(name=loggername, settings=loggerSettings)