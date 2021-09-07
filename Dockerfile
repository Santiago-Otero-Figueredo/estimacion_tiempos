FROM python:3.8

EXPOSE 8000

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /aplicacion
WORKDIR /aplicacion
COPY . /aplicacion

RUN pip install -r requirements/base.pip
RUN pip install -r requirements/test.pip

CMD ["gunicorn", "-c", "config/gunicorn/config.py", "--bind", ":8000", "--chdir", "config", "wsgi:application"],