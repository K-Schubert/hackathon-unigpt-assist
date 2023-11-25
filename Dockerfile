FROM python:3.11-slim

WORKDIR /root

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY rag rag
COPY unigpt unigpt
COPY chatbot chatbot
COPY templates templates
COPY server.py server.py
COPY manage.py manage.py
COPY unigpt/.env .env

RUN python3 manage.py migrate

ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:80"]
