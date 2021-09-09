FROM python:3.8

EXPOSE 8000

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /aplicacion
WORKDIR /aplicacion
COPY . /aplicacion

RUN pip install -r requirements/base.pip
RUN pip install -r requirements/test.pip

COPY python/custom-entrypoint /usr/local/bin/
RUN chmod u+x /usr/local/bin/custom-entrypoint
ENTRYPOINT ["custom-entrypoint"]

CMD ["gunicorn", "-b", "0.0.0.0", "-w", "2", "config.wsgi"]