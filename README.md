# CythonBuilder: automated compiling and packaging of Cython code
![coverage](https://img.shields.io/codecov/c/github/mike-huls/cythonbuilder)
![Tests](https://github.com/mike-huls/cythonbuilder/actions/workflows/tests.yml/badge.svg)
![version](https://img.shields.io/pypi/v/cythonbuilder?color=%2334D058&label=pypi%20package)
![dependencies](https://img.shields.io/librariesio/release/pypi/cythonbuilder)
![PyPI Downloads](https://img.shields.io/pypi/dm/cythonbuilder.svg?label=PyPI%20downloads)
![versions](https://img.shields.io/pypi/pyversions/cythonbuilder.svg?color=%2334D058)
<br>
![tweet](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fmike-huls%2Fcythonbuilder) ![xfollow](https://img.shields.io/twitter/follow/mike_huls?style=social) 


CythonBuilder makes it easy to use Cython in your Python project by automating the building process.
You can use CythonBuilder from the commandline or import it as a package in Python. 
Generated files can be imported in Python directly

```sh
pip install cythonbuilder
```


### Normal
Add `-v` (verbose) for more information 
1. Listing files with and without filter
```commandline
cybuilder list
cybuilder list --files file1 file2.pyx
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

### With Python
1. Listing files with and without filter

```python
import cythonbuilder

print(cythonbuilder.cy_list())  # without a filter
print(cythonbuilder.cy_list(target_files=['some_name.pyx']))  # with a filter
```

2. Build with and without optional build arguments  (cleans automatically afterwards)

```python
import cythonbuilder

cythonbuilder.cy_build()

found_files = cythonbuilder.cy_build(target_files=['some_name'])
cythonbuilder.cy_build(target_files=found_files, include_numpy=False, create_annotations=False)
```

3. Clean

```python
import cythonbuilder

cythonbuilder.cy_clean()

found_files = cythonbuilder.cy_build(target_files=['some_name'])
cythonbuilder.cy_clean(target_files=['some_name'])
```

4. Setting debug level for verbose logging

```python
import logging
from . import logger

logger.setLevel(logging.DEBUG)
```

### In-depth, step by step Explanation
I've written a few articles that explain why Python is slow, why Cython can be a solution and how CythonBuilder helps us develop fast code easily:
- [Why Python is so slow and how to speed it up](https://mikehuls.com/why-is-python-so-slow-and-how-to-speed-it-up-6720e14a1ca260001b1c0cba)
- [Getting started with Cython; how to perform >1.7 billion calculations per second with Python](https://mikehuls.com/getting-started-with-cython-how-to-perform-1-7-billion-calculations-per-second-in-python-6720e14a1ca260001b1c0ccf)
- [Cython for data science: 6 steps to make this Pandas dataframe operation over 100x faster](https://mikehuls.com/cython-for-data-science-6-steps-to-make-this-pandas-dataframe-operation-over-100x-faster-6720e14a1ca260001b1c0d07/)
