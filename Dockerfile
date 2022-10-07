FROM python:3.8.14-slim
WORKDIR /app

COPY . /app
RUN apt-get update && apt-get install -y poppler-utils \
  && pip install pipenv --no-cache-dir \
  && pipenv install --system --deploy

CMD ["python", "run.py"]
