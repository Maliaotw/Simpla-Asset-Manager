FROM python:3.6
ENV PYTHONUNBUFFERED 1
WORKDIR /AutoCmdb
ADD AutoCmdb /AutoCmdb
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
libsqlite3-dev
RUN pip install -U pip setuptools
RUN pip install -r /AutoCmdb/requirements.txt

CMD ["python", "manage.py", "runserver","0.0.0.0:8000"]
EXPOSE 8000