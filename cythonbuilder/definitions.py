import os
import sys

from helpycli import appsettings

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
PACKAGE_ROOT = sys.modules[appsettings.helpy_package_name].__path__[0]

