FROM python:3.9-slim as builder

WORKDIR /home/app

COPY . .
RUN pip install -r requirements.txt

CMD [ "uvicorn", "api:app","--reload", "--host", "0.0.0.0", "--port", "8000"]
