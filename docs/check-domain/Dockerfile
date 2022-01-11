FROM python

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install -U pip && \
  pip install --no-cache -r requirements.txt

COPY ./app .

VOLUME ["/var/log/check-domain"]

# EXPOSE 80

CMD ["python", "-u", "main.py"]
