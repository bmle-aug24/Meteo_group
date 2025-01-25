FROM python:3.11.8

RUN mkdir /app &&  mkdir /app/model

COPY * /app

WORKDIR /app/

RUN pip install -r requirements.txt

CMD ["uvicorn", "app_model:api", "--host", "0.0.0.0", "--port", "8000"]