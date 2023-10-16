conda-update:
	conda env update --prune -f environment.yml

pip-tools:
	python -m pip install pip-tools
	pip-compile requirements/base.in

# execute after pull this repo
	pip-sync requirements/base.txt

run:
	python .

watch:
	uvicorn app.app:app --reload
	
restore:
	docker cp ./backup.gz mongodb-garderobe:./backup.gz
	docker exec -it mongodb-garderobe mongorestore --archive=./backup.gz -u root -p root

seed:
	docker-copmpose exec app exec python -m app.seeder.seeder