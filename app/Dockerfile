FROM python:3.13.13-alpine

ENV PATH="${PATH}:/root/.local/bin"
COPY ./src /app/src
COPY migrations /app/migrations
COPY alembic.ini /app/
COPY requirements.txt /app/
COPY start.sh /app/
COPY main.py /app/
COPY sqlite.db /app/

ENV PYTHONPATH=/app/src
WORKDIR /app
RUN pip install -r ./requirements.txt
RUN chmod +x ./start.sh
EXPOSE 8000
