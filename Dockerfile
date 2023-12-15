FROM python:3.11-slim-buster
WORKDIR /code
COPY . /code/
RUN pip install --no-cache-dir -r /code/requirements.txt
RUN ruff format .
RUN isort .
RUN ruff check .
EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0"]
