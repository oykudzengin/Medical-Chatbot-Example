FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt . 

RUN pip install -r requirements.txt

RUN python --version && pip show langchain

COPY . .

CMD ["python3", "app.py"]