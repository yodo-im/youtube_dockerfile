FROM python

WORKDIR /usr/src/app

COPY ./app .

CMD ["python", "test.py"]
