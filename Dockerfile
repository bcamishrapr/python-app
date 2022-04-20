FROM python:3.6

WORKDIR /app

ENV FLASK_APP=hello.py

COPY src/requirements.txt ./

RUN pip install -r requirements.txt


COPY src /app

EXPOSE 8080

CMD ["flask","run", "--host=0.0.0.0"]
