FROM docker.io/ubuntu:20.04
LABEL maintainer="Sofiane Bebert <s.bebert@diceytech.co.uk>"

RUN apt update && \
    apt upgrade -y && \
    # python 3.8
    apt install -y language-pack-en git python3 python3-pip libmysqlclient-dev
RUN ln -s /usr/bin/python3 /usr/bin/python


RUN mkdir /openedx
RUN git clone https://github.com/Dicey-Tech/dt-classroom --branch main --depth 1 /openedx/dt-classroom
# --branch {{ OPENEDX_COMMON_VERSION }}
WORKDIR /openedx/dt-classroom

# Setup empty yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV CLASSROOM_CFG /openedx/config.yml

RUN pip3 install -r requirements/production.txt

# python requirements
# RUN pip3 install -r requirements/base.txt

# Install django-redis for using redis as a django cache
# RUN pip install django-redis==4.12.1

# Install uwsgi
RUN pip install uwsgi==2.0.19.1

{{ patch("dt-learninghub-dockerfile-post-python-requirements") }}

RUN python manage.py collectstatic --noinput

# TODO change to uswgi
EXPOSE 8000
CMD uwsgi \
    --static-map /static=/openedx/dt-classroom/classrooms/assets \
    --http 0.0.0.0:8000 \
    --thunder-lock \
    --single-interpreter \
    --enable-threads \
    --processes=2 \
    --buffer-size=8192 \
    --wsgi-file classrooms/wsgi.py
# CMD gunicorn --workers=2 --name classroom --bind=0.0.0.0:8000 --max-requests=1000 classrooms.wsgi:application
