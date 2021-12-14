# CythonBuilder
CythonBuilder; automated compiling and packaging of Cython code


[comment]: <> ([![Implementation]&#40;https://img.shields.io/pypi/implementation/cythonbuilder&#41;]&#40;https://cython.org/&#41;)
[comment]: <> ([![Source]&#40;https://img.shields.io/pypi/format/cythonbuilder&#41;]&#40;https://pypi.org/project/cythonbuilder&#41;)
[![PythonVersion](https://img.shields.io/pypi/pyversions/cythonbuilder)]()
[![Version](https://img.shields.io/pypi/v/cythonbuilder)](https://pypi.org/project/cythonbuilder/)
[![PyPiStatus](https://img.shields.io/pypi/status/cythonbuilder)](https://pypi.org/project/cythonbuilder/)
[![Downloads Badge](https://img.shields.io/pypi/dm/cythonbuilder)](https://pypi.org/project/cythonbuilder/)

## Installation
```commandline
pip install cythonbuilder
```

## How to use
CythonBuilder makes it easy to use Cython in your Python project by automating the compilation, building and packaging process.
You can use CythonBuilder from the commandline or import it as a package in Python. 


### Commandline Demonstration:
1. <b>Initialize</b>  
In your project directory, call `cybuilder init`. This creates the `/ext` folder.

2. <b>Organize</b>  
Place all of your Cython files in `/ext/pyxfiles`

3. <b>Compile and package</b>  
Simply call `cybuilder build` to build all Cythonfiles in `/ext/pyxfiles`. 
Alternatively call `cybuilder build filename` to package specific files (no .pyx needed)

4. <b>Import</b>
All packages en up in `/ext` so you can simply `from ext import yourfilename`.


### Python demonstration

```python
import cythonbuilder as cybuilder

cybuilder.init()
cybuilder.just_build(targetfilenames=["my_cy_package"])

from ext import my_cy_package

my_cy_package.some_function()
```

### In-depth, step by step Explanation
I've written a few articles that explain why Python is slow, why we need Cython and how CythonBuilder helps us develop fast code easily:
- [Why Python is so slow and how to speed it up](https://mikehuls.medium.com/why-is-python-so-slow-and-how-to-speed-it-up-485b5a84154e)
- [Getting started with Cython; how to perform >1.7 billion calculations per second with Python](https://mikehuls.medium.com/getting-started-with-cython-how-to-perform-1-7-billion-calculations-per-second-in-python-b83374cfcf77)
- [Cython for data science: 6 steps to make this Pandas dataframe operation over 100x faster](https://mikehuls.medium.com/cython-for-data-science-6-steps-to-make-this-pandas-dataframe-operation-over-100x-faster-1dadd905a00b)
