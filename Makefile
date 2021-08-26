
export PYPI_PACKAGE_NAME = trulede.linbus


default: build

setup:
	pip install -r requirements.txt

build:
	python3 setup.py sdist bdist_wheel

install:
	pip install --no-cache-dir -e .

test:
	pytest -rx tests -W ignore::DeprecationWarning

clean:
	-pip uninstall -y $(PYPI_PACKAGE_NAME)
	rm -rf ./dist
	rm -rf ./*.egg-info
	rm -rf .pytest_cache
	py3clean .


.PHONY default setup build install test clean
