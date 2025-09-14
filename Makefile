install:
	uv sync
	uv add gunicorn

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

