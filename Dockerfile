FROM python:3.8.3-slim-buster

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

ENV LC_ALL C.UTF-8

ENV LANG C.UTF-8

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN python -m spacy download en_core_web_lg

EXPOSE 5065

CMD python3 ./app.py

