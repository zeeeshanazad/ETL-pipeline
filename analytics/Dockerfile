FROM python:3-slim
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 sqlalchemy pymysql cryptography

WORKDIR /app
COPY . .
RUN pip install --ignore-installed -e .
CMD [ "python", "./analytics.py" ]