FROM python:3.10-slim-bullseye

COPY requirements.txt /app/requirements.txt

RUN python -m pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app

CMD ["python", "main.py"]