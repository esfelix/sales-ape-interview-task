.PHONY: start

start:
	docker-compose run --rm --entrypoint /.venv/bin/python backend spotify/scripts/load_spotify_data.py
	docker-compose up