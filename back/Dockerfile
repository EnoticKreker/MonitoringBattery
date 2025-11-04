FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev netcat-openbsd

RUN pip install --upgrade pip uv


COPY pyproject.toml uv.lock /app/

RUN uv sync

COPY app /app/app
RUN chmod +x /app/app/migrate_db.sh

EXPOSE 8000

CMD ["uv", "run", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
