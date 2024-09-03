FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir matplotlib

CMD ["sh", "-c", "python -m unittest discover -s . && python task_script.py"]