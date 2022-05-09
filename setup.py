import setuptools

from cythonbuilder.__version__ import __version__, __author__, __license__, __email__, __package_name__, __project_url__, __description__


# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=__package_name__,
    packages=[__package_name__],
    # For including non-python files (in this example all files in the ./files folder)
    # package_data={'': ['files/*']},
    version=__version__,
    license=__license__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=__author__,
    author_email=__email__,
    url=__project_url__,
    project_urls={
        "Source": "https://github.com/mike-huls/cythonbuilder/",
        "Bug Tracker": "https://github.com/mike-huls/cythonbuilder/issues",
        "Documentation": "https://github.com/mike-huls/cythonbuilder/blob/main/README.md/",
    },
    # Entry points make CLI access possible
    entry_points={
        'console_scripts': [
            f'cythonbuilder=cythonbuilder.cli:main',
            f'cybuilder=cythonbuilder.cli:main',
        ],
    },
    # Add packages that need to be installed along this package:
    install_requires=['Cython', 'coloredlogs'],
    python_requires='>=3',
    # Describe this package in a few keywords:
    keywords=["pypi", "Cython", "setup", "packaging", "compilation"],  # descriptive meta-data
    # https://pypi.org/classifiers
    classifiers=[                                   
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ]
)