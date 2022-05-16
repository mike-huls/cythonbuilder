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
- 


## Logs

## 2022-05-16 [0.1.9]
### ADDED
- `cli` returns a special message if no pyx files can be found
### Fixed
- `pyigenerator.py` `line_is_import` now also includes `from XX import YY`

<hr>

## 2022-05-13
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