
install:
	if [ ! -d .venv ]; then virtualenv -p `which python3.7` .venv; fi; \
	. .venv/bin/activate; \
	which python; \
	pip install --upgrade pip; \
	pip install -r requirements.txt; \
	deactivate

make_migr:
	. .venv/bin/activate; \
	# python manage.py makemigrations users; \
	python manage.py makemigrations task_manager; \
	python manage.py makemigrations; \
	deactivate

migr:
	. .venv/bin/activate; \
	python manage.py migrate; \
	deactivate

fix_migr:
	. .venv/bin/activate; \
	# python manage.py makemigrations task_manager --empty; \
	python manage.py makemigrations; \
	python manage.py migrate --fake-initial; \
	python manage.py migrate; \
	#python manage.py makemigrations task_manager; \
	#python manage.py migrate --fake task_manager zero; \
	#python manage.py migrate task_manager; \
	deactivate

test:
	. .venv/bin/activate; \
	python manage.py test; \
	deactivate

super:
	. .venv/bin/activate; \
	python manage.py createsuperuser; \
	deactivate

shell:
	. .venv/bin/activate; \
	python manage.py shell; \
	deactivate

run:
	. .venv/bin/activate; \
	# python manage.py collectstatic --noinput; \
	python manage.py runserver 0.0.0.0:1818; \
	deactivate
