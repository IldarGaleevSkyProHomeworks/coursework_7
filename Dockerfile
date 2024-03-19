FROM python:3.11-alpine as build

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /build/
RUN pip install --no-cache-dir poetry==1.6.1
COPY ./poetry.lock ./pyproject.toml /build/
RUN poetry install --without dev --no-interaction --no-ansi


FROM build as production

ENV DJANGO_SETTINGS_MODULE=config.settings
ENV APPLICATION_HOSTNAME='127.0.0.1'

WORKDIR /app
COPY . .
RUN mkdir static
RUN python manage.py collectstatic --noinput