FROM python:3

WORKDIR /code

COPY requirements.txt requirements.txt 

RUN pip3 install -r requirements.txt

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc \
                                        libsndfile1 

COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

