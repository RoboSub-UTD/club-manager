#!/usr/bin/env bash

set -e

venv/bin/pipenv install --deploy
venv/bin/pipenv run python manage.py migrate
venv/bin/pipenv run python manage.py collectstatic --noinput --clear
sudo systemctl restart gunicorn
sudo systemctl restart discord_bot