import sys

import typer

from cythonbuilder import cython_builder
from cythonbuilder import appsettings
from cythonbuilder import helpers
from cythonbuilder import set_logger_debug_mode
from cythonbuilder.definitions import DefaultArgs
from cythonbuilder.services import logger

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
#
#
# def display_help():
#     print(f"""{appsettings.package_name}
#         Automatically builds and packages your Cython code
#         1. Initialize {appsettings.package_name} with `{appsettings.console_name} init`
#         3. Call `{appsettings.console_name} build` to build and package all .pyx files in your project
#
#         Commands:
#         (call either command with -v to display more information)
#         help        Show this screen
#         init        Create 'ext' and 'ext/annotations' folders
#         list        Lists all pyx files in your project that can be built
#                     Pass a space-separated list of filenames (with or without .pyx) to filter
#         build       Finds and builds all pyx files in your project (excluding venv directories) package cython files. Then cleans the project (see cybuilder clean)
#                     Pass a space-separated list of filenames (with or without .pyx) to filter.
#                     Options:
#                       --no-interfaces   Prevents creating .pyi interface files (default False)
#                       --include-numpy   Includes numpy (default False)
#                       --no-annotation   Disables generating the annotations html (default True)
#                       --no-cleanup      Prevents removal of intermediate C files generated by Cython (default True)
#         clean       Moves all generated .html files to ext/annotations
#                     Pass a space-separated list of filenames (with or without .pyx) to filter.
#                     Options:
#                       --keep-c      Prevents removal of intermediate C files generated by Cython (default False)
#         interface   Generates all pyi files that serve as an interface for IDE's
#                     Pass a space-separated list of filenames (with or without .pyx) to filter.
#     """)
#     sys.exit(0)
#
#
# def main():
#     """ Parse command line """
#
#
#     args = sys.argv[1:]
#
#     # Preferences
#     # FORCE = '-f' in args or '--force' in args
#     VERBOSE = '-v' in args or '--verbose' in args
#     ACCEPT = '-y' in args or '--yes' in args
#     # OVERWRITE = '-o' in args or '--overwrite' in args
#     for flag in ['-f', '--force', '-v', '--verbose', '-y', '--accept', '-o', '--overwrite']:
#         args.remove(flag) if (flag in args) else None
#
#     return
#     # Logging level
#     if (VERBOSE):
#         set_logger_debug_mode(logger=logger)
#         # from cythonbuilder.logs import set_format
#         # set_format(logger=logger, format=f"[%(name)s] %(asctime)s %(module)-8s %(lineno)-3d  %(message)s")
#         # logger.setLevel(logging.DEBUG)
#
#
#
#     # Parse arguments - Must provide at least one argument
#     if (len(args) == 0):
#         display_help()
#     cmd1 = helpers.CliTools.pop_arg_or_exit(arglist=args, errormessage=f"[{appsettings.package_name}] {appsettings.package_name} expects at least one argument. Check out [helpy help] for more information")
#     logger.debug(msg=f"{cmd1=}")
#
#
#     # HELPY functions
#     if (cmd1 == 'ok'):
#         pass
#     # elif (cmd1 == 'init'):
#     #     logger.info(msg=f"[{cmd1}] - Initializing..")
#     #     cython_builder.cy_init()
#     #     logger.info(msg=f"[{cmd1}] - Initialized")
#     #     sys.exit(0)
#     # elif (cmd1 == 'list'):
#     #     # Lists all pyx files that can be built
#     #     target_filenames = args if (len(args) > 0) else None
#     #     filtermsg = f" (filtered by {' '.join(target_filenames)}) " if (target_filenames) else ""
#     #     logger.info(msg=f"Listing all pyx files{filtermsg}..")
#     #     found_pyx_files: [str] = cython_builder.cy_list(target_files=target_filenames)
#     #     if (len(found_pyx_files) >0):
#     #         found_files_string = "\n".join([f"\t - {fle}" for fle in found_pyx_files])
#     #         logger.info(msg=f"Found files:\n{found_files_string}")
#     #     else:
#     #         logger.info(msg=f"No pyx files found")
#     # elif (cmd1 == 'build'):
#     #     # Get arguments
#     #     include_numpy = '--include-numpy' in args
#     #     dont_generate_annotations = '--no-annotations' in args
#     #     dont_generate_pyi = '--no-interfaces' in args
#     #     keep_c_files = '--no-cleanup' in args
#     #     encoding = 'UTF-8'
#     #     args = [a for a in args if (a not in ['--no-annotations', '--include-numpy', '--no-cleanup', '--no-interfaces'])]
#     #     target_filenames = args if (len(args) > 0) else None
#     #
#     #     # Validate arguments
#     #     numpy_is_installed = helpers.package_is_installed(package_import_name='numpy')
#     #     if (include_numpy and not numpy_is_installed):
#     #         if (input(f"[{appsettings.package_name} {cmd1}] You want to include numpy but your current project does not have numpy installed. Install numpy? (y/n)").lower() == 'y'):
#     #             logger.warning(msg=f"Please install numpy with [pip install numpy]")
#     #             sys.exit(0)
#     #         else:
#     #             include_numpy = False
#     #     if (not include_numpy and numpy_is_installed):
#     #         if (input(f"[{appsettings.package_name} {cmd1}] Your current project uses numpy. Do you want to include numpy in your Cython build? (y/n)").lower() == 'y'):
#     #             include_numpy = True
#     #
#     #     logger.info(msg=f"[{cmd1}] - Building Cython files..")
#     #     try:
#     #         # 1. Find pyx files
#     #         found_pyx_files: [str] = cython_builder.cy_list(target_files=target_filenames)
#     #         if (len(found_pyx_files) == 0):
#     #             logger.info(msg="No .pyx files found")
#     #             sys.exit(0)
#     #         logger.debug(msg=f"Found {len(found_pyx_files)} to build")
#     #
#     #         # 2. Confirm that we want to build
#     #         if (not ACCEPT):
#     #             __formatted_package_list = "\n".join(f"\t - {file}" for file in found_pyx_files)
#     #             if (input(f"[{appsettings.package_name} {cmd1}] these {len(found_pyx_files)} pyx files?\n(y/n) \n {__formatted_package_list}").lower() != "y"):
#     #                 logger.info(msg="Exiting..", )
#     #                 sys.exit(0)
#     #         logger.debug(msg=f"Building {len(found_pyx_files)} pyx files..")
#     #
#     #         # 3. Build
#     #         cython_builder.cy_build(
#     #             target_files=found_pyx_files,
#     #             create_annotations=not dont_generate_annotations,
#     #             include_numpy=include_numpy,
#     #         )
#     #         logger.debug(msg=f"Built {len(found_pyx_files)} pyx files, cleaning up..")
#     #
#     #         # 4. Cleanup after build
#     #         cython_builder.cy_clean(target_files=found_pyx_files, keep_c_files=keep_c_files)
#     #         logger.debug(msg=f"Cleanup complete")
#     #
#     #         # 5.  Generate pyi files
#     #         if (not dont_generate_pyi):
#     #             logger.debug(msg=f"Generating interface files..")
#     #             cython_builder.cy_interface(target_files=found_pyx_files, encoding='zzz')
#     #             logger.debug(msg=f"Generated pyi files")
#     #
#     #         logger.info(msg=f"[{cmd1}] - Cython build success")
#     #     except Exception as e:
#     #         logger.error(msg=f"[{cmd1}] build error: {e}")
#     #         sys.exit(1)
#     # elif (cmd1 == 'clean'):
#     #     # Get arguments
#     #     keep_c_files = '--keep-c' in args
#     #     args = [a for a in args if (a not in ['--keep-c'])]
#     #     target_filenames = args if (len(args) > 0) else None
#     #
#     #     # Clean
#     #     logger.info(msg=f"[{cmd1}] - Cleaning Cython files..")
#     #     try:
#     #         # 1. Find pyx files
#     #         found_pyx_files: [str] = cython_builder.cy_list(target_files=target_filenames)
#     #         if (len(found_pyx_files) == 0):
#     #             logger.info(msg="No .pyx files found")
#     #             sys.exit(0)
#     #         logger.debug(msg=f"Found {len(found_pyx_files)} to clean")
#     #
#     #         # 2. Confirm that we want to build
#     #         if (not ACCEPT):
#     #             __formatted_package_list = "\n".join(f"\t - {file}" for file in found_pyx_files)
#     #             if (input(f"[{appsettings.package_name} {cmd1}] these {len(found_pyx_files)} pyx files?\n(y/n) \n {__formatted_package_list}").lower() != "y"):
#     #                 logger.info(msg="Exiting..", )
#     #                 sys.exit(0)
#     #         logger.debug(msg=f"Cleaning {len(found_pyx_files)} pyx files..")
#     #
#     #         # 3. Clean
#     #         cython_builder.cy_clean(target_files=found_pyx_files, keep_c_files=keep_c_files)
#     #         logger.debug(msg=f"Cleanup complete")
#     #         logger.info(msg=f"[{cmd1}] - Cython build success")
#     #     except Exception as e:
#     #         logger.error(msg=f"[{cmd1}] build error: {e}")
#     #         sys.exit(1)
#     elif (cmd1 in ['interface', 'pyi']):
#
#         target_filenames = args if (len(args) > 0) else None
#
#         logger.info(msg=f"[{cmd1}] - Generating interface files..")
#         try:
#             # 1. Find pyx files
#             found_pyx_files: [str] = cython_builder.cy_list(target_files=target_filenames)
#             if (len(found_pyx_files) == 0):
#                 logger.info(msg="No .pyx files found")
#                 sys.exit(0)
#             logger.debug(msg=f"Found {len(found_pyx_files)} to create pyi files for")
#
#             # 2. Confirm that we want to build
#             if (not ACCEPT):
#                 __formatted_package_list = "\n".join(f"\t - {file}" for file in found_pyx_files)
#                 if (input(f"[{appsettings.package_name} {cmd1}] these {len(found_pyx_files)} pyx files?\n(y/n) \n {__formatted_package_list}").lower() != "y"):
#                     logger.info(msg="Exiting..", )
#                     sys.exit(0)
#             logger.debug(msg=f"Creating {len(found_pyx_files)} pyi files..")
#
#             # 3. Generate pyi files
#             logger.debug(msg=f"Generating pyi files..")
#             cython_builder.cy_interface(target_files=found_pyx_files)
#             logger.debug(msg=f"Generated pyi files")
#             logger.info(msg=f"[{cmd1}] - Generating interface files success")
#         except Exception as e:
#             logger.error(msg=f"[{cmd1}] build error: {e}")
#             sys.exit(1)
#
#     elif (cmd1 == 'help'):
#         display_help()
#     else:
#         logger.warning(msg=f"unknown command: '{cmd1}'")
#         display_help()
#
