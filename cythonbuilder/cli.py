import logging
import sys
import typing

import typer

from . import helpers, appsettings, cython_builder
from .definitions import DefaultArgs

_VERBOSE = '-v' in sys.argv or '--verbose' in sys.argv



app = typer.Typer(name="main_helpy", pretty_exceptions_enable=False)


@app.command(name="init", help=f"Initialize cythonbuilder", short_help="Initialize Cython Builder")
def init_cb():
    cython_builder.cy_init()
    sys.exit(0)


@app.command(name="list", help="List all .pyx files", short_help="List all .pyx files")
def list_(
    target_filenames: typing.List[str] = typer.Option(None, "--files", help="Filter by these files"),
    VERBOSE: bool = DefaultArgs.verbose,
):
    # Lists all pyx files that can be built
    filtermsg = f" (filtered by {' '.join(target_filenames)}) " if (target_filenames) else ""
    typer.secho(message=f"Listing all pyx files{filtermsg}..", color=typer.colors.GREEN)
    found_pyx_files: [str] = cython_builder.cy_list(target_files=target_filenames)
    if (len(found_pyx_files) > 0):
        found_files_string = "\n".join([f"\t - {fle}" for fle in found_pyx_files])
        typer.secho(message=f"Found files:\n{found_files_string}", color=typer.colors.GREEN)
    else:
        typer.secho(message=f"No pyx files found", color=typer.colors.GREEN)


@app.command(name="build", help="compile all .pyx files", short_help="Compile all .pyx files to C")
def build(
        target_filenames: typing.List[str] = typer.Option(None, "--files", help="Target .pyx file names"),
        include_numpy: bool = typer.Option(False, "--include-numpy", help="Include numpy if numpy is installed in your project"),
        dont_generate_annotations: bool = typer.Option(False, "--no-annotation", help="Skip generating annotations (html)"),
        dont_generate_pyi: bool = typer.Option(False, "--no-interface", help="Skip generating .pyi stub files"),
        keep_c_files: bool = typer.Option(False, "--no-cleanup", help="Skip removing generated C-files"),
        encoding: str = typer.Option('UTF-8', "--encoding", help="Encoding of your .pyx files"),
        ACCEPT: bool = DefaultArgs.accept, VERBOSE: bool = DefaultArgs.verbose
):
    # Validate arguments
    numpy_is_installed = helpers.package_is_installed(package_import_name='numpy')
    if include_numpy and not numpy_is_installed:
        typer.secho(message=f"You want to include numpy but your current project does not have numpy installed. Please install numpy and try again", color=typer.colors.YELLOW)
        sys.exit(1)
    if (not include_numpy and numpy_is_installed):
        use_numpy = typer.confirm("[{appsettings.package_name}] Your current project uses numpy. Do you want to include numpy in your Cython build? (y/n)")
        if use_numpy:
            include_numpy = True

    # Building
    typer.secho(message=f"Building Cython files..", color=typer.colors.GREEN)
    try:
        # 1. Find pyx files
        found_pyx_files: [str] = cython_builder.cy_list(target_files=target_filenames)
        if (len(found_pyx_files) == 0):
            typer.secho(message=f"No .pyx files found", color=typer.colors.GREEN)
            sys.exit(0)
        typer.secho(message=f"Found {len(found_pyx_files)} to build", color=typer.colors.GREEN)

        # 2. Confirm that we want to build
        if (not ACCEPT):
            __formatted_package_list = "\n".join(f"\t - {file}" for file in found_pyx_files)
            do_build = typer.confirm(f"[{appsettings.package_name}] these {len(found_pyx_files)} pyx files?\n(y/n) \n {__formatted_package_list}")
            if not do_build:
                print(msg="Exiting..")
                typer.secho(message="Exiting..", color=typer.colors.GREEN)
                sys.exit(0)
        typer.secho(message=f"Building {len(found_pyx_files)} pyx files..", color=typer.colors.GREEN)

        # 3. Build
        cython_builder.cy_build(
            target_files=found_pyx_files,
            create_annotations=not dont_generate_annotations,
            include_numpy=include_numpy,
        )
        typer.secho(message=f"Built {len(found_pyx_files)} pyx files, cleaning up..", color=typer.colors.GREEN)

        # 4. Cleanup after build
        cython_builder.cy_clean(target_files=found_pyx_files, keep_c_files=keep_c_files)

        # 5.  Generate pyi files
        if (not dont_generate_pyi):
            cython_builder.cy_interface(target_files=found_pyx_files, encoding=encoding)
            typer.secho(message=f"Generated pyi interface files", color=typer.colors.GREEN)

        typer.secho(message=f"Cython build success", color=typer.colors.GREEN)
    except Exception as e:
        typer.secho(message=f"build error: {e}", color=typer.colors.RED)
        sys.exit(1)

@app.command(name="clean", help="Clean your project; remove all .c ", short_help="Clean your project")
def cb_clean(
        target_filenames: typing.List[str] = typer.Option(None, "--files", help="Target .pyx file names"),
        keep_c_files: bool = typer.Option(False, "--no-cleanup", help="Skip removing generated C-files"),
        ACCEPT: bool = DefaultArgs.accept, VERBOSE: bool = DefaultArgs.verbose
):
    # Clean
    try:
        # 1. Find pyx files
        found_pyx_files: [str] = cython_builder.cy_list(target_files=target_filenames)
        if (len(found_pyx_files) == 0):
            typer.secho(message=f"No .pyx files found", color=typer.colors.GREEN)
            sys.exit(0)
        typer.secho(message=f"Found {len(found_pyx_files)} to clean", color=typer.colors.GREEN)

        # 2. Confirm that we want to build
        if (not ACCEPT):
            __formatted_package_list = "\n".join(f"\t - {file}" for file in found_pyx_files)
            do_accept = typer.confirm(f"[{appsettings.package_name}] these {len(found_pyx_files)} pyx files?\n(y/n) \n {__formatted_package_list}")
            if not do_accept:
                typer.secho(message=f"Exiting..", color=typer.colors.GREEN)
                sys.exit(0)

        # 3. Clean
        typer.secho(message=f"Cleaning {len(found_pyx_files)} pyx files..", color=typer.colors.GREEN)
        cython_builder.cy_clean(target_files=found_pyx_files, keep_c_files=keep_c_files)
        typer.secho(message=f"Cleanup complete", color=typer.colors.GREEN)
    except Exception as e:
        typer.secho(message=f"Cleanup error: {e}", color=typer.colors.RED)
        sys.exit(1)

@app.command(name="interface", help="Create .pyi files for use in your Python project", short_help="generate interface files")
def cb_interface(
        target_filenames: typing.List[str] = typer.Option(None, "--files", help="Target .pyx file names"),
        ACCEPT: bool = DefaultArgs.accept, VERBOSE: bool = DefaultArgs.verbose
):
    try:
        # 1. Find pyx files
        found_pyx_files: [str] = cython_builder.cy_list(target_files=target_filenames)
        if (len(found_pyx_files) == 0):
            typer.secho(message=f"No .pyx files found", color=typer.colors.GREEN)
            sys.exit(0)
        typer.secho(message=f"Found {len(found_pyx_files)} to generate pyi interfaces for", color=typer.colors.GREEN)

        # 2. Confirm that we want to build
        if (not ACCEPT):
            __formatted_package_list = "\n".join(f"\t - {file}" for file in found_pyx_files)
            do_accept = f"[{appsettings.package_name}] these {len(found_pyx_files)} pyx files?\n(y/n) \n {__formatted_package_list}"
            if not do_accept:
                typer.secho(message=f"Exiting..", color=typer.colors.GREEN)
                sys.exit(0)

        # 3. Generate pyi files
        typer.secho(message=f"Generating {len(found_pyx_files)} interface files..", color=typer.colors.GREEN)
        cython_builder.cy_interface(target_files=found_pyx_files)
        typer.secho(message=f"Generating interface files complete", color=typer.colors.GREEN)
    except Exception as e:
        typer.secho(message=f"Error generating interface(s): {e}", color=typer.colors.RED)
        sys.exit(1)