#FROM python:3.11-slim
FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 80

HEALTHCHECK CMD curl --fail http://localhost:80/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]