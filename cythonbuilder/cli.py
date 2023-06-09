import sys
import typing

import typer

from . import helpers, appsettings, cython_builder
from .logs import logger, set_logger_debug_mode
from .definitions import DefaultArgs

_VERBOSE = '-v' in sys.argv or '--verbose' in sys.argv
if (_VERBOSE):
    set_logger_debug_mode(logger=logger)

app = typer.Typer(name="main_helpy", pretty_exceptions_enable=_VERBOSE)


@app.command(name="init", help=f"Initialize cythonbuilder", short_help="Initialize Cython Builder")
def init_cb(
        VERBOSE: bool = DefaultArgs.verbose
):
    logger.info(msg="Initializing..")
    cython_builder.cy_init()
    logger.info(msg="Initialized")
    sys.exit(0)


@app.command(name="list", help="List all .pyx files", short_help="List all .pyx files")
def list_(
    target_filenames: typing.List[str] = typer.Option(None, "--files", help="Filter by these files"),
    VERBOSE: bool = DefaultArgs.verbose
):

    logger.debug(target_filenames)

    # Lists all pyx files that can be built
    filtermsg = f" (filtered by {' '.join(target_filenames)}) " if (target_filenames) else ""
    logger.info(msg=f"Listing all pyx files{filtermsg}..")
    found_pyx_files: [str] = cython_builder.cy_list(target_files=target_filenames)
    if (len(found_pyx_files) > 0):
        found_files_string = "\n".join([f"\t - {fle}" for fle in found_pyx_files])
        logger.info(msg=f"Found files:\n{found_files_string}")
    else:
        logger.info(msg=f"No pyx files found")


@app.command(name="build", help="compile all .pyx files", short_help="Compile all .pyx files to C")
def build(
        target_filenames: typing.List[str] = typer.Option(None, "--files", help="Target .pyx file names"),
        include_numpy: bool = typer.Option(False, "--include-numpy", help="Include numpy if numpy is installed in your project"),
        dont_generate_annotations: bool = typer.Option(False, "--no-annotation", help="Skip generating annotations (html)"),
        dont_generate_pyi: bool = typer.Option(False, "--no-interface", help="Skip generating .pyi stub files"),
        keep_c_files: bool = typer.Option(False, "--no-cleanup", help="Skip removing generated C-files"),
        encoding: str = typer.Option('UTF-8', "--encoding", help="Encoding of your .pyx files"),
        ACCEPT: bool = DefaultArgs.accept, VERBOSE: bool = DefaultArgs.verbose
        # VERBOSE: bool = DefaultArgs.verbose, OVERWRITE: bool = DefaultArgs.overwrite, ACCEPT: bool = DefaultArgs.accept
):
    # Validate arguments
    numpy_is_installed = helpers.package_is_installed(package_import_name='numpy')
    if (include_numpy and not numpy_is_installed):
        if (input(f"[{appsettings.package_name}] You want to include numpy but your current project does not have numpy installed. Install numpy? (y/n)").lower() == 'y'):
            logger.warning(msg=f"Please install numpy with [pip install numpy]")
            sys.exit(0)
        else:
            include_numpy = False
    if (not include_numpy and numpy_is_installed):
        if (input(f"[{appsettings.package_name}] Your current project uses numpy. Do you want to include numpy in your Cython build? (y/n)").lower() == 'y'):
            include_numpy = True

    # Building
    logger.info(msg=f"Building Cython files..")
    try:
        # 1. Find pyx files
        found_pyx_files: [str] = cython_builder.cy_list(target_files=target_filenames)
        if (len(found_pyx_files) == 0):
            logger.info(msg="No .pyx files found")
            sys.exit(0)
        logger.debug(msg=f"Found {len(found_pyx_files)} to build")

        # 2. Confirm that we want to build
        if (not ACCEPT):
            __formatted_package_list = "\n".join(f"\t - {file}" for file in found_pyx_files)
            if (input(f"[{appsettings.package_name}] these {len(found_pyx_files)} pyx files?\n(y/n) \n {__formatted_package_list}").lower() != "y"):
                logger.info(msg="Exiting..", )
                sys.exit(0)
        logger.debug(msg=f"Building {len(found_pyx_files)} pyx files..")

        # 3. Build
        cython_builder.cy_build(
            target_files=found_pyx_files,
            create_annotations=not dont_generate_annotations,
            include_numpy=include_numpy,
        )
        logger.debug(msg=f"Built {len(found_pyx_files)} pyx files, cleaning up..")

        # 4. Cleanup after build
        cython_builder.cy_clean(target_files=found_pyx_files, keep_c_files=keep_c_files)
        logger.debug(msg=f"Cleanup complete")

        # 5.  Generate pyi files
        if (not dont_generate_pyi):
            logger.debug(msg=f"Generating interface files..")
            cython_builder.cy_interface(target_files=found_pyx_files, encoding=encoding)
            logger.debug(msg=f"Generated pyi files")

        logger.info(msg=f"Cython build success")
    except Exception as e:
        logger.error(msg=f"build error: {e}")
        sys.exit(1)

@app.command(name="clean", help="Clean your project; remove all .c ", short_help="Clean your project")
def cb_clean(
        target_filenames: typing.List[str] = typer.Option(None, "--files", help="Target .pyx file names"),
        keep_c_files: bool = typer.Option(False, "--no-cleanup", help="Skip removing generated C-files"),
        ACCEPT: bool = DefaultArgs.accept, VERBOSE: bool = DefaultArgs.verbose
        # VERBOSE: bool = DefaultArgs.verbose, OVERWRITE: bool = DefaultArgs.overwrite, ACCEPT: bool = DefaultArgs.accept
):
    # Clean
    logger.info(msg=f"Cleaning Cython files..")
    try:
        # 1. Find pyx files
        found_pyx_files: [str] = cython_builder.cy_list(target_files=target_filenames)
        if (len(found_pyx_files) == 0):
            logger.info(msg="No .pyx files found")
            sys.exit(0)
        logger.debug(msg=f"Found {len(found_pyx_files)} to clean")

        # 2. Confirm that we want to build
        if (not ACCEPT):
            __formatted_package_list = "\n".join(f"\t - {file}" for file in found_pyx_files)
            if (input(f"[{appsettings.package_name}] these {len(found_pyx_files)} pyx files?\n(y/n) \n {__formatted_package_list}").lower() != "y"):
                logger.info(msg="Exiting..", )
                sys.exit(0)
        logger.debug(msg=f"Cleaning {len(found_pyx_files)} pyx files..")

        # 3. Clean
        cython_builder.cy_clean(target_files=found_pyx_files, keep_c_files=keep_c_files)
        logger.debug(msg=f"Cleanup complete")
        logger.info(msg=f"Cython build success")
    except Exception as e:
        logger.error(msg=f"build error: {e}")
        sys.exit(1)

@app.command(name="interface", help="Create .pyi files for use in your Python project", short_help="generate interface files")
def cb_interface(
        target_filenames: typing.List[str] = typer.Option(None, "--files", help="Target .pyx file names"),
        ACCEPT: bool = DefaultArgs.accept, VERBOSE: bool = DefaultArgs.verbose
):
    logger.info(msg=f"Generating interface files..")
    try:
        # 1. Find pyx files
        found_pyx_files: [str] = cython_builder.cy_list(target_files=target_filenames)
        if (len(found_pyx_files) == 0):
            logger.info(msg="No .pyx files found")
            sys.exit(0)
        logger.debug(msg=f"Found {len(found_pyx_files)} to create pyi files for")

        # 2. Confirm that we want to build
        if (not ACCEPT):
            __formatted_package_list = "\n".join(f"\t - {file}" for file in found_pyx_files)
            if (input(f"[{appsettings.package_name}] these {len(found_pyx_files)} pyx files?\n(y/n) \n {__formatted_package_list}").lower() != "y"):
                logger.info(msg="Exiting..", )
                sys.exit(0)
        logger.debug(msg=f"Creating {len(found_pyx_files)} pyi files..")

        # 3. Generate pyi files
        logger.debug(msg=f"Generating pyi files..")
        cython_builder.cy_interface(target_files=found_pyx_files)
        logger.debug(msg=f"Generated pyi files")
        logger.info(msg=f"Generating interface files success")
    except Exception as e:
        logger.error(msg=f"build error: {e}")
        sys.exit(1)