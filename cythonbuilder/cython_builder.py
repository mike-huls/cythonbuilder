from pathlib import Path
import os
import shutil
import sys

from cythonbuilder.helpers import FilesAndFolders
from cythonbuilder.services import logger
from cythonbuilder import appsettings
from cythonbuilder import pyigenerator

project_dir = os.getcwd()


def cy_init():
    """ Creates projdir.ext, projdir.ext.annotations """

    # create root.ext, root.ext.annotations
    FilesAndFolders.create_folder(folderpath=os.path.join(project_dir, appsettings.cython_extensions_dirname))
    FilesAndFolders.create_folder(folderpath=os.path.join(project_dir, appsettings.cython_anno_dirname))
    logger.debug(msg=f"[{cy_init.__name__}] - Initialized cybuilder at {project_dir}")



def cy_list(target_files:[str]=None) -> [str]:
    """ Target files is optional filter. Returns a list of fullpaths to pyxfiles """
    # 1. Find all fullpaths to pyx files in all folders but the /venv
    venv_paths_folders = [os.path.dirname(path) for path in Path(project_dir).rglob('pyvenv.cfg')]
    pyx_fullpaths = [str(pyxpath) for pyxpath in Path(project_dir).rglob('*.pyx')]
    for venvpath in venv_paths_folders:
        pyx_fullpaths = [pf for pf in pyx_fullpaths if (venvpath not in pf)]

    # 2. Apply optional file name filter
    if (target_files != None):
        my_pyx_file_names = [os.path.splitext(os.path.basename(p))[0] for p in pyx_fullpaths]
        target_file_names = [os.path.splitext(p)[0] for p in target_files]

        # Calculate overlap and difference
        diff = set(target_file_names).difference(set(my_pyx_file_names))
        intersection = set(my_pyx_file_names).intersection(set(target_file_names))

        # if (len(diff) > 0):
        #     raise ValueError(f"Cannot find provided target files: {[f'{f}.pyx' for f in diff]}")

        _pyx_fullpaths = []
        for pyx in pyx_fullpaths:
            for ins in intersection:
                if (f"{ins}.pyx" in pyx):
                    _pyx_fullpaths.append(pyx)
        pyx_fullpaths = _pyx_fullpaths
    return pyx_fullpaths
def cy_build(target_files:[str] = None, create_annotations:bool=True, include_numpy:bool=False):
    """ Builds all pyx files in the /ext folder """

    # 1. Get target files
    if (target_files == None):
        target_files = cy_list()


    # We want to build in place
    sys.argv = [sys.argv[0], 'build_ext', '--inplace']

    from setuptools import setup, Extension
    from Cython.Distutils import build_ext
    from Cython.Build import cythonize
    import Cython.Compiler.Options

    # Annotation is whether or not the html should be created
    Cython.Compiler.Options.annotate = create_annotations

    # Create Extension objects
    ext_modules = []
    for n in target_files:
        if (not os.path.isfile(n)):
            logger.info(msg=f"File '{n}' not found; skipping..")
            continue
        logger.debug(msg=f"C {n}")
        module_name, extension = os.path.splitext(os.path.basename(n))
        # The name must be plain, no path
        obj = Extension(
            name=module_name,
            sources=[n],
            # extra_compile_args=["-O2", "-march=native"]
        )
        ext_modules.append(obj)

    # Extra include folders. Mainly for numpy.
    include_dirs = []
    if (include_numpy):
        try:
            import numpy
            include_dirs += [numpy.get_include()]
        except:
            raise ValueError('Numpy is required, but not found. Please install')

    # build
    setup(
        cmdclass={'build_ext': build_ext},
        include_dirs=include_dirs,
        ext_modules=cythonize(ext_modules),
        # buid_dir=path_build_dir
    )

def cy_clean(target_files:[str] = None, keep_c_files:bool=False):
    """ Clean up all files """
    logger.debug(msg=f"[{cy_clean.__name__}] - start cy_clean with {target_files}")

    # 1. Get target files
    if (target_files == None):
        target_files = cy_list()

    # Make sure cybuilder is init because we need to move files to /ext/annotations
    cy_init()

    annotations_dir = os.path.join(project_dir, appsettings.cython_anno_dirname)

    # Remove build folder
    build_folder_path = os.path.join(project_dir, 'build')
    if (os.path.isdir(build_folder_path)):
        shutil.rmtree(path=build_folder_path)

    for built_file in target_files:
        if (not os.path.isfile(built_file)):
            logger.info(msg=f"File {built_file} not found; skipping..")
            continue

        _filename = os.path.splitext(os.path.basename(built_file))[0]    # no ext

        # Clean up C files
        if (not keep_c_files):
            filepath = f"{os.path.splitext(built_file)[0]}.c"
            if (not os.path.isfile(filepath)):
                logger.debug(msg=f"[{cy_clean.__name__}]: cannot remove file: does not exist {filepath}")
                continue

            FilesAndFolders.remove_file(targetfilename=f"{os.path.splitext(built_file)[0]}.c")
        # Move annotation html files
        src_htmlpath = f"{os.path.splitext(built_file)[0]}.html"
        dst_htmlpath = os.path.join(annotations_dir, os.path.basename(src_htmlpath))
        logger.debug(msg=f"[{cy_clean.__name__}] - Moving annotation files from {src_htmlpath} to {dst_htmlpath}")
        FilesAndFolders.move_file(
            srcfilename=src_htmlpath,
            dstfilename=dst_htmlpath,
            overwrite=True
        )
        # Move PYD files
        built_file_folder = os.path.dirname(built_file)
        pyd_file = ([fn for fn in os.listdir(project_dir) if (_filename in fn and ('.pyd' in fn or '.so' in fn))])[0]
        logger.debug(msg=f"[{cy_clean.__name__}] - Moving pyd files from {os.path.join(project_dir, pyd_file)} to {os.path.join(built_file_folder, pyd_file)}")
        FilesAndFolders.move_file(
            srcfilename=os.path.join(project_dir, pyd_file),
            dstfilename=os.path.join(built_file_folder, pyd_file),
            overwrite=True
        )
def cy_interface(target_files:[str] = None):
    """ Creates .pyi interface files from the provided target_files """


    # 1. Get target files
    if (target_files == None):
        target_files = cy_list()
    logger.debug(msg=f"[{cy_interface.__name__}] - generating interface files for {len(target_files)} found pyx files")


    for pyx_fullpath in target_files:
        if (not os.path.isfile(pyx_fullpath)):
            logger.info(msg=f"File {pyx_fullpath} not found; skipping..")
            continue
        pyi_fullpath = f"{os.path.splitext(pyx_fullpath)[0]}.pyi"
        logger.debug(msg=f"Creating .pyi for {pyx_fullpath}")

        pyigenerator.read_write_pyx_to_pyi(target_pyx_path=pyx_fullpath, target_pyi_path=pyi_fullpath)

