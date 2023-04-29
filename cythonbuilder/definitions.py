import os
import sys
from dataclasses import dataclass

import typer

from cythonbuilder import appsettings

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
PACKAGE_ROOT = sys.modules[appsettings.package_name].__path__[0]

@dataclass
class DefaultArgs:
    verbose:bool =   typer.Option(False, "--verbose", '-v', help="Higher verbosity of commands")
    force:bool =     typer.Option(False, "--force", '-f', help="Force this operation")#, prompt=f"{helpy_mascotte} Are you sure you want to delete the user?", )
    overwrite:bool = typer.Option(False, "--overwrite", '-o', help="Overwrite existing")
    accept:bool =    typer.Option(False, "--accept", '-y', help="Yes to all prompts")
