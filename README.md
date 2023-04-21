# CythonBuilder
CythonBuilder; automated compiling and packaging of Cython code

<table>
    <tr>
        <th>Version</th>
        <td>
            <a href="https://pypi.org/project/cythonbuilder">
                <img alt="version" src="https://img.shields.io/pypi/v/cythonbuilder">
            </a>
        </td>
    </tr>
    <tr>
        <th>Package</th>
        <td>
            <a href="https://pypi.org/project/cythonbuilder">
                <img alt="PythonVersion" src="https://img.shields.io/pypi/pyversions/cythonbuilder">
            </a>
            <a href="https://pypi.org/project/cythonbuilder">
                <img alt="Platform" src="https://img.shields.io/badge/os-windows%20%7C%20linux-blue">
            </a>
            <a href="https://github.com/mike-huls/cythonbuilder/blob/main/license.txt">
                <img alt="License" src="https://img.shields.io/pypi/l/cythonbuilder">
            </a>
            <a href="https://cython.org/">
                <img alt="implementation" src="https://img.shields.io/pypi/implementation/cythonbuilder">
            </a>
        </td>
    </tr>
    <tr>
        <th>Status</th>
        <td>
            <a href="https://pypi.org/project/cythonbuilder">
                <img alt="status" src="https://img.shields.io/pypi/status/cythonbuilder">
            </a>
            <a href="https://pypi.org/project/cythonbuilder">
                <img alt="DependencyStatus" src="https://img.shields.io/librariesio/release/pypi/cythonbuilder">
            </a>
        </td>
    </tr>
    <tr>
        <th>Stats</th>
        <td>
            <a href="https://pypi.org/project/cythonbuilder/">
                <img alt="DownloadsCount" src="https://img.shields.io/pypi/dm/cythonbuilder">
            </a>
        </td>
    </tr>
    <tr>
        <th>Social</th>
        <td>
            <a href="https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fmike-huls%2Fcythonbuilder">
                <img alt="tweet" src="https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fmike-huls%2Fcythonbuilder">
            </a>
            <a href="https://img.shields.io/twitter/follow/mike_huls?style=social">
                <img alt="twitterfollow" src="https://img.shields.io/twitter/follow/mike_huls?style=social">
            </a>
        </td>
    </tr>
</table>


## Installation
```commandline
pip install cythonbuilder
```

## How to use
CythonBuilder makes it easy to use Cython in your Python project by automating the building process.
You can use CythonBuilder from the commandline or import it as a package in Python. 
Generated files can be imported in Python directly


### With Commandline
Add `-v` (verbose) for more information 
1. Listing files with and without filter
```commandline
cybuilder list
cybuilder list file1 file2.pyx
```

2. Build with and without optional build arguments 
```commandline
cybuilder build
cybuilder build --include-numpy --no-annotation --no-cleanup
```

3. Clean
```commandline
cybuilder clean 
cybuilder clean --no-cleanup
```

<hr>

### With python
1. Listing files with and without filter

```python

from src import cythonbuilder as cybuilder

print(cybuilder.cy_list())  # without a filter
print(cybuilder.cy_list(target_files=['some_name.pyx']))  # with a filter
```

2. Build with and without optional build arguments  (cleans automatically afterwards)

```python

from src import cythonbuilder as cybuilder

cybuilder.cy_build()

found_files = cybuilder.cy_build(target_files=['some_name'])
cybuilder.cy_build(target_files=found_files, include_numpy=False, create_annotations=False)
```

3. Clean

```python

from src import cythonbuilder as cybuilder

cybuilder.cy_clean()

found_files = cybuilder.cy_build(target_files=['some_name'])
cybuilder.cy_clean(target_files=['some_name'])
```

4. Setting debug level for verbose logging

```python
from src.cythonbuilder import logger
from src.cythonbuilder import set_logger_debug_mode

set_logger_debug_mode(logger=logger)
```

### In-depth, step by step Explanation
I've written a few articles that explain why Python is slow, why Cython can be a solution and how CythonBuilder helps us develop fast code easily:
- [Why Python is so slow and how to speed it up](https://mikehuls.medium.com/why-is-python-so-slow-and-how-to-speed-it-up-485b5a84154e)
- [Getting started with Cython; how to perform >1.7 billion calculations per second with Python](https://mikehuls.medium.com/getting-started-with-cython-how-to-perform-1-7-billion-calculations-per-second-in-python-b83374cfcf77)
- [Cython for data science: 6 steps to make this Pandas dataframe operation over 100x faster](https://mikehuls.medium.com/cython-for-data-science-6-steps-to-make-this-pandas-dataframe-operation-over-100x-faster-1dadd905a00b)
