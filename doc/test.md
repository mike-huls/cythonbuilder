python -m coverage run -m unittest discover && coverage html
start chrome %cd%/htmlcov/index.html 
