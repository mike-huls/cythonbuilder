import os
import sys

from cythonbuilder import appsettings

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
PACKAGE_ROOT = sys.modules[appsettings.package_name].__path__[0]

