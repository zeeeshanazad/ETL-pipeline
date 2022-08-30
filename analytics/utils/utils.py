from geopy.distance import geodesic as GD
import json
from os import environ
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy import Table, Column, Integer, String, MetaData, Float


def parse_json(x):
    x = json.loads(x)
    return (x['latitude'], x['longitude'])


def distance(x):
    data = x['location_parsed'].values.tolist()
    distances = [GD(data[i], data[i + 1]).km for i in range(len(data) - 1)]
    return sum(distances)


def connect_mysql():
    while True:
        try:
            mysql_engine = create_engine(environ["MYSQL_CS"], pool_pre_ping=True, pool_size=10)
            metadata_obj = MetaData()
            devices = Table(
                'devices_analytics', metadata_obj,
                Column('device_id', String(50)),
                Column('max_temperature', Integer),
                Column('total_data_points', Integer),
                Column('distance', Float),
                Column('time', String(50)),
            )
            metadata_obj.create_all(mysql_engine)
            print('Table created in MySQL')
            break
        except OperationalError:
            sleep(0.1)

