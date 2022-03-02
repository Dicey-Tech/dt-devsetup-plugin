FROM docker.io/ubuntu:20.04
LABEL maintainer="Sofiane Bebert <s.bebert@diceytech.co.uk>"

RUN apt update && \
    apt install -y curl git-core language-pack-en libmysqlclient-dev python3 python3-pip python3-venv

ARG APP_USER_ID=1000
RUN useradd --home-dir /openedx --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

# Create python venv
RUN python3 -m venv /openedx/venv/
ENV PATH "/openedx/venv/bin:$PATH"
RUN pip install setuptools==44.1.0 pip==20.3.4 wheel==0.37.0

# Install learninghub
ARG LEARNINGHUB_REPOSITORY=https://github.com/Dicey-Tech/dt-classroom.git
ARG LEARNINGHUB_VERSION={{ OPENEDX_COMMON_VERSION }}
RUN mkdir -p /openedx/dt-classroom && \
    git clone https://github.com/Dicey-Tech/dt-classroom --branch main --depth 1 /openedx/dt-classroom
# --branch {{ OPENEDX_COMMON_VERSION }}
WORKDIR /openedx/dt-classroom

# Setup empty yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV CLASSROOM_CFG /openedx/config.yml

# python requirements
RUN pip3 install -r requirements/production.txt

# Install django-redis for using redis as a django cache
RUN pip install django-redis==5.0.0

# Install uwsgi
RUN pip install uwsgi==2.0.20

{{ patch("dt-learninghub-dockerfile-post-python-requirements") }}

RUN python manage.py collectstatic --noinput

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
