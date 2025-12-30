FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN python --version && pip show langchain

CMD ["python3", "app.py"]