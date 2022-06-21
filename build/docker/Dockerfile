FROM python:3.10-slim

RUN mkdir /app

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN python3 -m pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src/app.py /app/app.py
COPY ./src/formatting.py /app/formatting.py

CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
