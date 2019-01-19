.PHONY: test ship

test:
	flake8 muckrock
	coverage run test.py
	coverage report -m

ship:
	python setup.py sdist bdist_wheel
	twine upload dist/* --skip-existing
