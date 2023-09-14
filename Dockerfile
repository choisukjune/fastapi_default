FROM python:3.10

WORKDIR /usr/src/app
COPY krampoline/ ./

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]