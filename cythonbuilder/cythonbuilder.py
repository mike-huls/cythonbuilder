from __future__ import print_function, division
import sys
import os
import logging
import shutil
from os.path import splitext
from pathlib import Path
from glob import glob


dirname_extensions = "ext"
dirname_pyxfiles = "pyxfiles"
dirname_annotations = "annotations"

path_root_dir = os.path.realpath(os.curdir)
path_extensions_dir = os.path.join(path_root_dir, dirname_extensions)
path_pyx_dir = os.path.join(path_extensions_dir, dirname_pyxfiles)
path_annotations_dir = os.path.join(path_extensions_dir, dirname_annotations)
path_setuppy_build_dir = os.path.join(path_root_dir, 'build')

appname = "CythonBuilder"
appcmd = os.path.splitext(os.path.basename(__file__))[0]


logging.basicConfig(
    level=logging.NOTSET,
    format=f'[{appname}] - %(levelname)s [%(asctime)s] %(message)s',
    datefmt='%H:%M:%S',
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)


def init():
    """ Creates a folder-structure for all pyx-files and resulting so-files like
    - root
        - ext (holds all so-files)
            - cythonfiles
   """


    required_folders = [path_root_dir, path_extensions_dir, path_pyx_dir, path_annotations_dir]


    # Ensure folder structure exists
    for folder in required_folders:
        if (not os.path.isdir(folder)):
            os.mkdir(folder)

    # Warn if folder contain files
    for _dir in [path_extensions_dir, path_pyx_dir]:
        file_list = next(os.walk(_dir), (None, None, []))[2]  # [] if no file
        if (len(file_list) > 0):
            logging.warning(f"{_dir} folder is not empty")

    logging.info("Initialized")

def help():
    print(f"""{appname}
    Automatically builds and packages your Cython code 
    1. Initialize {appname} with `{appcmd} init` 
    2. Place all .pyx Cython files in {dirname_extensions}/{dirname_pyxfiles}
    3. Call `{appcmd} build` to build and package all .pyx files in {dirname_extensions}/{dirname_pyxfiles} 
        Alternatively call `{appcmd} build filename1, filename2` (without .pyx extension) to build specific files
    4. Import your compile package from {dirname_extensions}/ like `from {dirname_extensions} import filename`

    init        Initialized the folders
    build       Build and package cython files
      --debug             Debugging mode (default False)
      --no-annotation     Disables generating the annotations html (default True)
      --no-numpy-include  Prevents numpy being included in setup.py include_dirs (default True)
      --no-cleanup        Prevents removal of intermediate C files that Cython generates (default True)
    help        Show this screen
    
""")




def build(annotation:bool=True, numpy_includes:bool=True, debugmode:bool=False, keep_c_files:bool=False, filenames:[str] = []):
    """ pyx -> c -> so
    annotation: whether or not to generate the annotation html
    """

    if (debugmode):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


    # The filename args are allowed to be globs
    logger.debug(f'Input filenames: {filenames})')
    target_pyx_filepaths = [y for x in os.walk(path_extensions_dir) for y in glob(os.path.join(x[0], '*.pyx'))]
    target_pyx_filenames = [os.path.basename(p) for p in target_pyx_filepaths]

    # Optionally apply filter by filenames argument
    if (len(filenames) > 0):
        # Check if all provided file names exist
        missing_pyx_filepaths = [p for p in filenames if f"{p}.pyx" not in target_pyx_filenames]
        if (len(missing_pyx_filepaths) > 0):
            logger.error('Could not find these files:')
            for f in missing_pyx_filepaths:
                logger.error(f'\t{f}')
            logger.error('Aborting.')
            sys.exit(2)

        # Filter our target files with the provided file names
        target_pyx_filepaths = [p for p in target_pyx_filepaths for f in filenames if f"{f}.pyx" in p]

    # NO pyx files found
    if (len(target_pyx_filepaths) == 0):
        logging.error('No pyx files found to compile')
        sys.exit(1)


    sys.argv = [sys.argv[0], 'build_ext', '--inplace']


    from setuptools import setup, Extension
    from Cython.Distutils import build_ext
    from Cython.Build import cythonize
    import Cython.Compiler.Options

    # Annotation is whether or not the html should be created
    Cython.Compiler.Options.annotate = annotation

    # Create module objects
    ext_modules = []
    for n in target_pyx_filepaths:
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
    if numpy_includes:
        try:
            import numpy
            include_dirs += [numpy.get_include()]
        except:
            logging.exception('Numpy is required, but not found. Please install it')

    setup(
        cmdclass = {'build_ext': build_ext},
        include_dirs=include_dirs,
        ext_modules = cythonize(ext_modules),
        # buid_dir=path_build_dir
    )

    # Cleanup
    for pyxpath in target_pyx_filepaths:
        # delete intermediate C files.
        if (not keep_c_files):
            cpath = pyxpath.replace(".pyx", ".c")
            if os.path.exists(cpath):
                os.remove(cpath)
            else:
                print(f"{cpath} doesn't exist")

        # Move all annotations
        htmlpath = pyxpath.replace(".pyx", ".html")
        shutil.move(htmlpath, os.path.join(path_annotations_dir, os.path.basename(htmlpath)))

        # Move all pyd files to the build dir
        for file in [f for f in os.listdir(path_root_dir) if '.pyd' in f]:
            shutil.move(
                src=os.path.join(path_root_dir, file),
                dst=os.path.join(path_extensions_dir, file)
            )

    # Remove setup.py build dir that contains compiled c
    shutil.rmtree(path_setuppy_build_dir)



def main():
    _args = sys.argv[1:]

    if (len(_args) == 0):
        help()
        sys.exit(1)



    if (_args[0] == 'init'):
        init()
    elif (_args[0] in ('--help', 'h', 'help')):
        help()
    elif (_args[0] in ('build')):
        do_annotate_html = len(set(_args) & {'--no-annotation'}) == 0
        do_debug = len(set(_args) & {'--debug'}) > 0
        do_include_numpy = len(set(_args) & {'--no-numpy-include'}) == 0
        do_cleanup_c_files = len(set(_args) & {'--no-cleanup-c'}) == 0

        _args = [a for a in _args if a not in ['build', '--no-annotation', '--debug', '--no-numpy-include', '--no-cleanup-c']]
        build(do_annotate_html, do_debug, do_include_numpy, keep_c_files=not do_cleanup_c_files, filenames=_args)
    else:
        help()

if (__name__ == "__main__"):
    main()