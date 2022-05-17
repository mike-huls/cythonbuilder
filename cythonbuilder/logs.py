import os

import coloredlogs
from coloredlogs import ColoredFormatter

import logging
from logging.handlers import TimedRotatingFileHandler

import cythonbuilder

DEFAULT_DATE_FORMAT = '%H:%M:%S'

DEFAULT_FIELD_STYLES = dict(
    asctime=dict(color='white'),
    hostname=dict(color='white'),
    levelname=dict(color='white', bold=True),
    name=dict(color='white'),
    programname=dict(color='white'),
    username=dict(color='white'),
    lineno=dict(color='white'),
    module=dict(color='white'),
    funcName=dict(color='white')
)

DEFAULT_LEVEL_STYLES = dict(
    # spam=dict(color='white', faint=True),
    # success=dict(color='green', bold=True),
    # notice=dict(color='magenta'),
    # verbose=dict(color='blue'),
    debug=dict(color='white'),
    info=dict(color='blue'),
    warning=dict(color='yellow', bright=True),
    error=dict(color='red', bold=True),
    critical=dict(color='black', bold=True, background='red'),
)
#endregion


class LoggerSettings:
    _format:str
    _dateformat:str
    _field_styles:dict
    _level_style:dict
    _log_file:str
    _level:int
    _valid_colors:[str] = ['black', 'blue', 'cyan', 'green', 'magenta', 'red', 'white', 'yellow']


    def __init__(
            self,
            level:int=logging.DEBUG,
            log_file:str=None,
            spacing:int=12,
            format:str=None,
            date_format:str=None,
    ):
        DEFAULT_FORMAT = f'[%(name)s] %(asctime)s %(module)-{spacing}s %(lineno)-3d  %(message)s'
        self._format = DEFAULT_FORMAT if (format == None) else format
        self._dateformat = DEFAULT_DATE_FORMAT if (date_format == None) else date_format
        self._field_styles = DEFAULT_FIELD_STYLES.copy()
        self._level_style = DEFAULT_LEVEL_STYLES.copy()
        self._level = level
        self._log_file = log_file


    def set_format(self, format:str):
        """" Sets the format of which fields will be taken """
        self._format = format

    def set_date_format(self, dateformat: str):
        """ Format the way asctime is displayed """

        self._dateformat = dateformat

    def set_level_style(self, level:str, color:str, background:str=None, bold:bool=False, bright:bool=False, faint:bool=False) -> None:
        """ Sets the styling of a certain level of the logger """

        level = level.lower()

        # Check inputs
        if (level == 'exception'):
            raise ValueError("Cannot set style of 'exception' directly since 'exception' is styled similar to 'error'. Set the style of 'error' instead")
        if (self._level_style.get(level) == None):
            raise ValueError(f"Level '{level}' does not exits. Existing levels: {list(self._level_style)}")

        # Cleanup
        color = color.lower()
        if (background != None):
            background = background.lower()

        # Set styles
        self._level_style[level] = {"color": color}
        if (background != None):
            self._level_style[level]['background'] = background
        if (bold != None):
            self._level_style[level]['bold'] = bold
        if (bright != None):
            self._level_style[level]['bright'] = bright
        if (faint != None):
            self._level_style[level]['faint'] = faint

    def set_field_styles(self, field:str, color:str, background:str=None, bold:bool=False, bright:bool=False, faint:bool=False) -> None:
        """ Sets the styling of fields in the logs """

        # Check inputs
        if (self._field_styles.get(field) == None):
            raise ValueError(f"Field '{field}' does not exits. Existing levels: {list(self._field_styles)}")

        # Cleanup
        color = color.lower()
        if (background != None):
            background = background.lower()

        # Set styles
        self._field_styles[field] = {"color": color}
        if (background != None):
            self._field_styles[field]['background'] = background
        if (bold != None):
            self._field_styles[field]['bold'] = bold
        if (bright != None):
            self._field_styles[field]['bright'] = bright
        if (faint != None):
            self._field_styles[field]['faint'] = faint


def create_logger(name:str, log_file:str=None, settings:LoggerSettings=None):
    """ Creates a logger """

    # 0. Check if logger with that name already exists
    if (name in list_all_loggers()):
        raise ValueError("a logger with this name already exists")

    # 1. Fall back to default settings if none passed
    if (settings == None):
        settings = LoggerSettings()

    # 2. Instantiate the logging module
    logging.basicConfig()
    logger = logging.getLogger(name=name)

    # 3. Set up a coloredformatter that determines the color styles and install it
    coloredFormatter = ColoredFormatter(
        fmt=settings._format,
        datefmt=settings._dateformat,
        level_styles=settings._level_style,
        field_styles=settings._field_styles
    )
    coloredlogs.install(
        level=settings._level,
        logger=logger,
        fmt=settings._format,
        datefmt=settings._dateformat
    )
    logger.propagate = False  # prevents logs to pass to the root logger (needs to be after coloredlogs.install)

    # 4. Set up handlers for logfile and the console
    if (log_file != None):
        fh = TimedRotatingFileHandler(filename=log_file, when='D', interval=1, backupCount=90, encoding='utf-8', delay=False)
        fh.setFormatter(fmt=coloredFormatter)
        logger.addHandler(hdlr=fh)
    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(fmt=coloredFormatter)
    logger.addHandler(hdlr=ch)    # def set_

    return logger

def list_all_loggers():
    """ Return the names of all active loggers """
    return list(logging.root.manager.loggerDict)

def set_only_active_loggers(active_logger_names:[str], level:int, other_loggers_level:int):
    """ Only these loggers will be set to 'level'. All other loggers will be set to 'other_loggers_level' """
    for loggername in list_all_loggers():
        if (loggername in active_logger_names):
            set_level(loggername=loggername, level=level)
        else:
            set_level(loggername=loggername, level=other_loggers_level)

def set_format(logger:logging.Logger, format:str):
    """ Sets the level of a logger """
    handler:logging.Handler
    for handler in logger.handlers:

        formatter:ColoredFormatter = handler.formatter
        coloredFormatter = ColoredFormatter(
            fmt=format,
            datefmt=formatter.datefmt,
            level_styles=formatter.level_styles,
            field_styles=formatter.field_styles
        )
        handler.setFormatter(fmt=coloredFormatter)

def set_logger_debug_mode(logger:logging.Logger=None):
    """ Set the debug mode of the logger """
    from cythonbuilder.services import logger
    set_format(logger=logger, format=f"[%(name)s] %(asctime)s %(module)-8s %(lineno)-3d  %(message)s")
    logger.setLevel(logging.DEBUG)
