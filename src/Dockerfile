FROM python:3.4-alpine
ADD . /code
WORKDIR /code
RUN apk add libssl
RUN pip install -r requirements.txt
RUN apk del libssl
CMD ["python", "app.py"]
