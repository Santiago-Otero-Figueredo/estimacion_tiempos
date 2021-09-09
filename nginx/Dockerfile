FROM python:3.8 AS build

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /aplicacion
WORKDIR /aplicacion
COPY . /aplicacion

RUN pip install -r requirements/base.pip
RUN pip install -r requirements/test.pip

RUN SECRET_KEY=secret python3 manage.py collectstatic

FROM nginx:1.14

# Configure NGINX
COPY nginx/conf.d/local.conf /etc/nginx/conf.d/default.conf

# Copy static files
COPY --from=build /aplicacion/apps/static/ /var/www/html/static
RUN chown -R nginx:nginx /var/www/html