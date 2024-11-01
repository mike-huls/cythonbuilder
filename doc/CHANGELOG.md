# Changelog
All notable changes to this project will be documented in this file.
 - `Added` for new features.
 - `Changed` for changes in existing functionality.
 - `Deprecated` for soon-to-be removed features.
 - `Removed` for now removed features.
 - `Fixed` for any bug fixes.
 - `Security` in case of vulnerabilities.
<hr>
 

## Upcoming features
- check if name of the built file (pyd/so) is the same as the pyx file. This makes importing difficult. Maybe before build check if there is a .py file of the same name?
---

## Logs
## 2024-11-01 - Cleanup - add CI/CD pipeline [0.1.21]
### ADDED
- .drone.yml for CI/CD pipeline
### CHANGED
- cli.py - replaced logger with typer echo
- logs.py - simplified logger a lot
- bumped version
### REMOVED 
- superfluous dependencies
- logs.py default loggersettings
- __version__ in __init__.py 
<hr>


## 2023-06-12 - Minor fixes [0.1.20]
### Fixed
- Corrected relative import in __main__.py
- Added coloredlogs as dependency in pyproject.toml
<hr>


## 2023-06-09 - Upgraded package - added emum support for pyi generator - [0.1.19]
### Added
- `.coveragerc` to exclude files from coverage
### Changed
- pyigenerator now skips anything in `if __name__ == "__main__"`
### Fixed
- error in listing *.pyx files
- README -> `cybuilder list file1 file2` --> `cybuilder list --files file1 file2`
<hr>


## 2023-04-24 - Upgraded package - added emum support for pyi generator - [0.1.15]
### Added
- coverage badge
- pyigenerator now includes support for enums
### Changed
- updated development status
### Fixed
- error in listing *.pyx files
- Project now build with buildtools - uses pyproject.toml
<hr>


## 2023-03-25 - Upgraded package - added emum support for pyi generator - [0.1.14]
### Changed
- Upgraded cli
### Fixed
- pyigenerator now reads in utf-8
<hr>


## 2022-06-01 - fixed interface - [0.1.13]
### Fixed
- `pyigenerator.py` - `convert_type_cy_to_py()` added cytype void --> pytype None
- `pyigenerator.py` - `py_line` took default values into account
- 


## 2022-05-22 - fixed interface - [0.1.12]
### Fixed
- `pyigenerator.py` - `convert_type_cy_to_py()` now returns cy_type if non-built-in type is provided
<hr>

## 2022-05-16 [0.1.11]
### ADDED
- `cli` returns a special message if no pyx files can be found and exits
- `pyigenerator.py` added support for class attributes
### Fixed
- `pyigenerator.py` `line_is_import` now also includes `from XX import YY`

<hr>

## 2022-05-13 [0.1.10]
### Added
- `__main__.py` for using cybuilder as a module like `python -m cythonbuilder help`
### Changed
- `pyigenerator.py pyx_line_to_pyi` - takes `-> int:` function return type into account
- `pyigenerator.py pyx_line_to_pyi` - flips ctype function parameters around `int age` --> `age:in`
<hr>

## 2022-05-10
### Changed
- Added support for function return types in `pyigenerator.py`  
- Added support for imports in `pyigenerator.py`
<hr>


## 2022-05-09
### Added
- `cybuilder init` 
- `cybuilder help` 
- `cybuilder list` 
- `cybuilder build`
- `cybuilder clean` to clean up like after a build
- `pyigenerator.py` -> Generate .pyi files from the .pyx files
- Added pyi generator implementation to ui and help function
### Changed
- README.md - new workflow
<hr>