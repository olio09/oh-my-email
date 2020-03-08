init:
	pip install twine

publish:
	rm -rf dist
	python setup.py sdist
	twine upload dist/* -r pypi