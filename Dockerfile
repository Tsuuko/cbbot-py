FROM python:3.8.14-slim
WORKDIR /app

RUN apt-get update\
  && apt-get install -y poppler-utils\
  && pip install pipenv --no-cache-dir

COPY . /app
RUN  pipenv install --system --deploy

CMD ["python", "run.py"]
