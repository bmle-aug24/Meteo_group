FROM python:3.11.8

RUN mkdir /app && mkdir /app/mlruns

COPY * /app

WORKDIR /app/

RUN pip install -r requirements.txt

CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "8100"]