import os
from dataclasses import dataclass


@dataclass
class AppConfig:
    appname:str = "CythonBuilder"
    appcmd:str = os.path.splitext(os.path.basename(__file__))[0]

@dataclass
class LoggingConfig:
    loggingName:str = 'cybuilderlogger'

@dataclass
class DirConfig:
    dirname_extensions:str = "ext"
    dirname_pyxfiles:str = "pyxfiles"
    dirname_annotations:str = "annotations"

    root:str = os.path.realpath(os.curdir)
    ext:str = os.path.join(root, dirname_extensions)
    pyx:str = os.path.join(ext, dirname_pyxfiles)
    anno:str = os.path.join(ext, dirname_annotations)
    build:str = os.path.join(root, 'build')
