clean:
	rm -f *.pyc

flake8:
	find . -name "*.py" -exec flake8 {} \;
