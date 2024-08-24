FROM python:3.10-slim

WORKDIR /app

COPY . /app

CMD ["sh", "-c", "python -m unittest discover -s . && python task_script.py"]
