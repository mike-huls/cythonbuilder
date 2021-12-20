import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version_number = "0.0.9"

setuptools.setup(
    name='cythonbuilder',  # should match the package folder
    packages=['cythonbuilder'],  # should match the package folder
    version=f'{version_number}',  # important for updates
    license='MIT',  # should match your chosen license
    description='CythonBuilder; automated compiling and packaging of Cython code',
    long_description=long_description,  # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Mike Huls',
    author_email='mikehuls42@gmail.com',
    url='https://github.com/mike-huls/cythonbuilder',
    project_urls={  # Optional
        "Source": "https://github.com/mike-huls/cythonbuilder/",
        "Bug Tracker": "https://github.com/mike-huls/cythonbuilder/issues",
        "Documentation": "https://github.com/mike-huls/cythonbuilder/blob/main/README.md/",
},
    entry_points={
        'console_scripts': [
            'cythonbuilder=cythonbuilder.cythonbuilder:main',
            'cybuilder=cythonbuilder.cythonbuilder:main'
        ],
    },
    install_requires=['Cython'],  # list all packages that your package uses
    python_requires='>=3',
    keywords=["pypi", "Cython", "setup", "packaging", "compilation"],  # descriptive meta-data
    classifiers=[
        # https://pypi.org/classifiers
        'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Compilers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.7',
        # 'Programming Language :: Python :: 3.8',
        # 'Programming Language :: Python :: 3.9',
    ],
    download_url=f"https://github.com/mike-huls/cythonbuilder/archive/refs/tags/v{version_number}.tar.gz",
)

# python setup.py sdist
# python -m twine upload dist/cythonbuilder-0.0.8.tar.gz
