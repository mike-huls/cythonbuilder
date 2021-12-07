# CythonBuilder
CythonBuilder; automated compiling and packaging of Cython code

This tool makes it easy to use Cython files. 
Follow the instructions below
 1. Initialize CythonBuilder with `cythonbuilder init`
 2. Place all .pyx Cython files in ext/pyxfiles
 3. Call `cythonbuilder build` to find, build and package of your .pyx files  
    Alternatively call `cythonbuilder build filename1, filename2` (without .pyx extension) to build specific files
 4. Import your compile package from ext/ like `from ext import filename`
