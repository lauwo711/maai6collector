FROM python:3.10-slim
LABEL authors="me"
RUN pip install --quiet --upgrade pip
RUN pip install poetry --quiet

# passed in the docker build command -> to copy files needed for one single data source
ARG DATA_DIR

# poetry related
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    # create a new venv
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# allow DATA_DIR/main.py import from parent directory. i.e. util.Storage
ENV THIS_ROOT=/app/maai6-collector/
ENV PYTHONPATH="${THIS_ROOT}:${PYTHONPATH}"

# Installing dependencies before copying code, else every time code is modified -> have to re-install dependencies
# --no-root (skips installing the project package) and
# --no-directory (skips installing any local directory path dependencies, you can omit this if you don’t have any)
RUN mkdir -p ${THIS_ROOT}${DATA_DIR}
WORKDIR ${THIS_ROOT}${DATA_DIR}
COPY /${DATA_DIR}/pyproject.toml /${DATA_DIR}/poetry.lock ./
RUN poetry install --no-root --no-directory --without dev && rm -rf $POETRY_CACHE_DIR

# copy other files
WORKDIR ${THIS_ROOT}
COPY . .

# run from DATA_DIR
WORKDIR ${THIS_ROOT}${DATA_DIR}
RUN poetry install --without dev
ENTRYPOINT ["poetry", "run", "python", "main.py"]