FROM python:slim
WORKDIR /cryptocli
RUN pip install pipenv
COPY ./Pipfile.lock ./
RUN pipenv install --dev --ignore-pipfile
COPY ./ ./
ENTRYPOINT ["/usr/local/bin/pipenv", "run"]
