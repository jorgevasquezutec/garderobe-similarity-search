conda-update:
	conda env update --prune -f environment.yml

pip-tools:
	python -m pip install pip-tools
	pip-compile requirements/requirements.in

# execute after pull this repo
	pip-sync requirements/requirements.txt

