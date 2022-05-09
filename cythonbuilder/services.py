import logging
import os

from cythonbuilder import appsettings
from cythonbuilder.definitions import PACKAGE_ROOT
from cythonbuilder.logs import create_logger, LoggerSettings


# Logger
# spacing = max([len(os.path.splitext(file)[0]) for file in os.listdir(PACKAGE_ROOT) if (file[:2] != "__")])
loggername = appsettings.package_name
loggerSettings = LoggerSettings(format=f'[%(name)s] %(message)s', level=logging.INFO)
loggerSettings.set_level_style(level='debug', color='green')
loggerSettings.set_level_style(level='info', color='white')
logger = create_logger(name=loggername, settings=loggerSettings)


# for lname, logger in logging.root.manager.loggerDict.items():
#     if (not isinstance(logger, logging.Logger)):
#         continue
#     if (loggername != logger):
#         logger.setLevel(level=logging.ERROR)
