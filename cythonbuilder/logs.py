import logging

from coloredlogs import ColoredFormatter

from cythonbuilder import appsettings

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
    debug=dict(color='green'),
    info=dict(color='white'),
    warning=dict(color='yellow', bright=True),
    error=dict(color='red', bold=True),
    critical=dict(color='black', bold=True, background='red'),
)

logger = logging.getLogger(name=appsettings.package_name)
ch = logging.StreamHandler()
spacing = 20
coloredFormatter = ColoredFormatter(
    fmt=f'[%(name)s] %(asctime)s %(module)-{spacing}s %(lineno)-3d  %(message)s',
    datefmt='%H:%M:%S',
    level_styles=DEFAULT_LEVEL_STYLES,
    field_styles=DEFAULT_FIELD_STYLES
)


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

def set_logger_debug_mode(logger:logging.Logger):
    """ Set the debug mode of the logger """
    set_format(logger=logger, format=f"[%(name)s] %(asctime)s %(module)-8s %(lineno)-3d  %(message)s")
    logger.setLevel(logging.DEBUG)

logger.setLevel(level=logging.INFO)


ch.setFormatter(fmt=coloredFormatter)
logger.addHandler(hdlr=ch)


