install:
	uv sync
	uv add gunicorn
	uv run django-admin compilemessages

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

