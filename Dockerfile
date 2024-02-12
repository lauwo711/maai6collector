FROM python:3.11.7-alpine
LABEL authors="lauwo"
RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    #create a new venv
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Installing dependencies before copying code, else every time code is modified -> have to re-install dependencies
# --no-root (skips installing the project package) and
# --no-directory (skips installing any local directory path dependencies, you can omit this if you don’t have any)
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-directory && rm -rf $POETRY_CACHE_DIR
COPY . .
RUN poetry install --no-dev
ENTRYPOINT ["poetry", "run", "python", "main.py"]