FROM python:3.11.8

RUN mkdir /app &&  mkdir /app/data && mkdir /app/data/raw

COPY * /app

WORKDIR /app/

RUN pip install -r requirements.txt

CMD ["python", "script_meteo.py"]