build project
`poetry build`

Set testpypi repository
`poetry config repositories.testpypi https://test.pypi.org/legacy/`

Set testpypi token
`poetry config pypi-token.testpypi <your-token>`


publish to testpypi
`poetry publish -r testpypi`

install and check
`pip install --index-url https://test.pypi.org/simple/ cythonbuilder`

Publish to PyPi
`poetry publish`