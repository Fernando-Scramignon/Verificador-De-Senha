FROM python:latest

# don't utilize pycache
ENV PYTHONDONTWRITEBYTECODE 1

# not missing logs
ENV PYTHONUNBUFFERED 1


WORKDIR /code
COPY . /code/


RUN pip install -U pip
RUN pip install -r requirements.txt


CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]