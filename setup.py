import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='cythonbuilder',  # should match the package folder
    packages=['cythonbuilder'],  # should match the package folder
    version='0.0.5',  # important for updates
    license='MIT',  # should match your chosen license
    description='CythonBuilder; automated compiling and packaging of Cython code',
    long_description=long_description,  # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Mike Huls',
    author_email='mikehuls42@gmail.com',
    url='https://github.com/mike-huls/cythonbuilder',
    project_urls={  # Optional
        "Bug Tracker": "https://github.com/mike-huls/cythonbuilder/issues"
    },
    install_requires=['Cython'],  # list all packages that your package uses
    keywords=["pypi", "Cython", "setup", "packaging", "compilation"],  # descriptive meta-data
    classifiers=[
        # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    download_url="https://github.com/mike-huls/cythonbuilder/archive/refs/tags/v0.0.5.tar.gz",
)