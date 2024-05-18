FROM python:3.12-slim-bullseye

ENV APP_DIR=/opt/app
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal


WORKDIR ${APP_DIR}

COPY requirements.txt ${APP_DIR}/requirements.txt

RUN apt update  --fix-missing -y && \
    apt install -y \
    libpq-dev \
    gdal-bin \
    curl \
    libgdal-dev \
    gettext \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r ${APP_DIR}/requirements.txt

RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

COPY apps ${APP_DIR}/apps
COPY tickets ${APP_DIR}/tickets
COPY templates ${APP_DIR}/templates
COPY manage.py ${APP_DIR}/manage.py

EXPOSE 9600

CMD ["python", "manage.py", "runserver", "0.0.0.0:9600"]