FROM python:3.9-slim

WORKDIR /iipa_backend

COPY pyproject.toml poetry.lock /iipa_backend/
RUN pip install --no-cache-dir poetry && poetry install --no-dev

COPY . /iipa_backend

EXPOSE 8000
RUN poetry install
CMD ["poetry", "run", "uvicorn", "iipa_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["./start.sh"]

