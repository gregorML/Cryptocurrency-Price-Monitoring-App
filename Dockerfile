FROM python:3.9-slim

ENV PYTHONPATH=/app:$PYTHONPATH

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED 1

EXPOSE 8501

CMD ["bash", "scripts/start.sh"]

