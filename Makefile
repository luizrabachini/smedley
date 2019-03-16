SETTINGS=smedley.config.settings


clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf
	@find . -name ".cache" -type d | xargs rm -rf

conf-env:
	@cp -n contrib/localenv .env
	@echo 'Please configure params from .env file.'
	@read continue

requirements-pip:
	@pip install -U pip
	@pip install -r requirements/development.txt

run: clean
	@export settings=$(SETTINGS) && \
	python main.py run

shell: clean
	@export settings=$(SETTINGS) && \
	ipython

test: clean
	@export settings=$(SETTINGS) && \
	py.test --cov smedley 

test-matching: clean
	@export settings=$(SETTINGS) && \
	py.test -rxs -k $(test) smedley
