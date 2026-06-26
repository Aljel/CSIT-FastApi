FROM python:3.12-slim

ENV PATH="${PATH}:/root/.local/bin"
COPY ./src /app/src
COPY migrations /app/migrations
COPY alembic.ini /app/
COPY requirements.txt /app/
COPY start.sh /app/
COPY main.py /app/

ENV PYTHONPATH=/app/src
WORKDIR /app
RUN pip install -r ./requirements.txt
RUN chmod +x ./start.sh
EXPOSE 8000
