import requests
from time import sleep, time
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, select
import logging

# local
# logging.basicConfig(filename=f'../log/log_{round(time())}.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(filename=f'/var/log/check-domain/log_{round(time())}.log', encoding='utf-8', level=logging.DEBUG)
logging.info(f'The container was run at {datetime.now()}')

Base = declarative_base()
# sqlalchemy connection
# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
# local
# engine = create_engine('mysql+mysqlconnector://root:777@0.0.0.0:3306/check-domain')
engine = create_engine('mysql+mysqlconnector://root:777@db:3306/check-domain')
Base.metadata.bind = engine

while True:
    domain = Table('domain', Base.metadata, autoload=True, autoload_with=engine)
    data = select(domain.c.name)
    with engine.connect() as conn:
        for row in conn.execute(data):
            domain = row[0]
            try:
                r = requests.get('https://'+domain, timeout=5, allow_redirects=False)
            except:
                status = 'fail'
            else:
                status = f'ok ({r.status_code})' if r.status_code == requests.codes.ok else f'other ({r.status_code})'
            out = f'{domain} ......... {status}'
            logging.info(out)
            print(out)
            sleep(1)
