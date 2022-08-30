from os import environ
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import pandas as pd
from time import time
from utils import parse_json, distance, connect_mysql


def extract(conn):
    temp_query = """SELECT * FROM devices 
    WHERE to_timestamp(CAST("time" AS double precision)) 
    BETWEEN now() - interval '1 hour' 
    AND now();"""
    data = pd.read_sql(temp_query, conn)
    return data


def transform(data):
    max_temp = data.groupby('device_id')['temperature'].max().reset_index(name='max_temperature')
    data_points = data.groupby('device_id')['device_id'].count().reset_index(name='total_data_points')
    data['location_parsed'] = data['location'].apply(parse_json)
    distances = data.groupby('device_id').apply(distance).reset_index(name='distance')
    df = max_temp.merge(data_points)
    df = df.merge(distances)
    times = [str(int(time())) for i in range(len(df))]
    df['time'] = times
    return df


def load(data, conn):
    connect_mysql()
    try:
        print('trying insert query')
        data.to_sql('devices_analytics', conn, if_exists='append', index=False)
    except ValueError as err:
        print('apna kuch')
        print(err)
    else:
        print('Values added to MYSQL successful')


print('Waiting for the data generator...')
sleep(20)

while True:
    try:
        psql_engine = create_engine(environ["POSTGRESQL_CS"], pool_pre_ping=True, pool_size=10)
        break
    except OperationalError:
        sleep(0.1)
print('Connection to PostgresSQL successful.')

while True:
    try:
        mysql_engine = create_engine(environ["MYSQL_CS"], pool_pre_ping=True, pool_size=10)
        break
    except OperationalError:
        sleep(0.1)

# Write the solution here

psql = psql_engine.connect()
mysql = mysql_engine.connect()
data = extract(psql)
data = transform(data)
load(data, mysql)

