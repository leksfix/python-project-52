install:
	uv sync
	uv add gunicorn


collectstatic:
	uv run django-admin compilemessages


migrate:
	uv run manage.py migrate


build:
	./build.sh

run:
	uv run manage.py runserver

render-start:
	gunicorn task_manager.wsgi


lint:
	uv run ruff check .