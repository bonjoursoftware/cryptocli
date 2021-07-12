ARG PYTHON_VERSION=3.9.6
FROM python:${PYTHON_VERSION}-slim-buster as builder
WORKDIR /cryptocli
RUN pip install --no-cache-dir pipenv==2021.5.29
COPY ./Pipfile.lock ./
RUN PIPENV_VENV_IN_PROJECT=1 pipenv sync

FROM python:${PYTHON_VERSION}-slim-buster
RUN useradd --create-home cryptocli
WORKDIR /home/cryptocli
USER cryptocli
COPY --from=builder /cryptocli/.venv/ /home/cryptocli/.local/
COPY ./cryptocli ./cryptocli
COPY ./cryptocli.py ./cryptocli.py
ENTRYPOINT ["python","-u","cryptocli.py"]
