`` ``` ```
## Dockerfile. Часть 3
# Собираем контейнер с приложение, и запускаем оба контейнера

1. Создаём файл main.py в директории app. Содержимое его:

```
import requests
from time import sleep, time
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, select
import logging

logging.basicConfig(filename=f'/var/log/check-domain/log_{round(time())}.log', encoding='utf-8', level=logging.DEBUG)
logging.info(f'The container was run at {datetime.now()}')

Base = declarative_base()
# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
engine = create_engine('mysql+mysqlconnector://root:777@db:3306/check-domain')
Base.metadata.bind = engine

while True:
    domain = Table('domain', Base.metadata, autoload=True, autoload_with=engine)
    data = select(domain.c.value)
    with engine.connect() as conn:
        for row in conn.execute(data):
            domain = row[0]
            try:
                r = requests.get('http://'+domain, timeout=5, allow_redirects=True)
            except:
                satus = 'fail'
            else:
                status = 'ok' if r.status_code == requests.codes.ok else f'fail ({r.status_code})'
            out = f'{domain} ......... {status}'
            logging.info(out)
            print(out)
```

`mysql+mysqlconnector://root:777@db:3306/check-domain` - подключение к БД, если БД настроена на внешний мир из докер, db - название контейнера с ДБ, приложение и БД должны работать в одной сети

2. Создаём виртуальную сеть для проекта `docker network create cd`

3. Создаём виртуальный том, где будут хранится данные для БД (это не обязательно, но если хочется сохранить, то нужно) `docker volume create cd_db_data`

3. Редактируем Dockerfile для приложения:
```
FROM python:3

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt

VOLUME [ "/var/log/check-domain" ]

COPY ./app .

CMD [ "python", "-u", "main.py" ]
```
RUN - действия которые должны быть проделаны во время создания контейнера, в данном случае мы обновляем менеджер пакетов для python pip и устанавливаем зависимости из файла requirements.txt. Этот файл предварительно копируется.

VOLUME - указывает точку монтирования, докер создаёт для неё автоматически виртуальный том, но желательно подключить директорию на хосте или созданный вручную виртуальный том явно параметром -v. В данном случае в эту директорию попадают логи работы приложения и мы хотим их сохранить.

EXPOSE - открывает порт изнутри контейнера, с помощью параметра -p можно будет открыть порт для внешнего мира, это актуально например для веб сервера.

4. Собираем образ приложения. В консоли на рабочей машине заходим в корневую директорию нашего проекта и пишем команду для сборки образа `docker build -t cd_py_img3 .`

5. Удалим все работающие контейнеры в данным момент `docker rm -f $(docker ps -aq)` и запустим только что созданные немного по другому.

6. Запускам базу данных `docker run --network cd --name db cd_db_img1`

7. Запускаем приложение `docker run --network cd --name app -v $(pwd)/logs:/var/log/check-domain -p 8080:80 cd_py_img3` и должны увидеть бегущие строчки с доменом
