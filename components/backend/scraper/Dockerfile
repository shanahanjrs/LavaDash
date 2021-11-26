## NOTE: To build this project go to the monorepo root and `docker-compose build scraper`

FROM python:3.8.5-alpine3.12

RUN apk add --update alpine-sdk libressl-dev libffi-dev

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.0.9 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # don't create virtualenvs
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN poetry config virtualenvs.create false

# Setup working dir
RUN mkdir -p /components/backend/scraper /components/modules/
COPY ./modules/analysis_utils /components/modules/analysis_utils

WORKDIR /components/backend/scraper

# Copy in Poetry files and install only dependencies
COPY ./backend/scraper/pyproject.toml ./backend/scraper/poetry.lock ./
RUN poetry install --no-root

COPY ./backend/scraper/ /components/backend
RUN poetry install

# START
EXPOSE 5100
CMD FLASK_APP=scraper.app poetry run flask run --host=0.0.0.0 --port=5100 --no-reload
