FROM python:3.8-slim

RUN set -ex; \
    # Python dependencies \
    apt-get update; \
    apt-get full-upgrade -y; \
    apt-get install -y --no-install-recommends \
        tini; \
    apt-mark showmanual > /tmp/aptMark; \
    apt install -y --no-install-recommends \
        gcc \
        g++ \
        make; \
    pip install -U pip; \
    pip install uwsgi; \
    useradd -m -s /bin/bash uwsgi

COPY . /app
WORKDIR /app
ENTRYPOINT ["/usr/bin/tini", "--"]

RUN set -ex; \
    savedAptMark="$(cat /tmp/aptMark)"; \
    rm /tmp/aptMark; \
    pip install --no-cache-dir -r requirements.txt; \
    apt-mark auto '.*' > /dev/null; \
    apt-mark manual $savedAptMark; \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*

EXPOSE 80/tcp
EXPOSE 81/tcp

CMD [ "uwsgi", "--master", \
      "--uid", "1000", "--gid", "1000", \
      "--http", "0.0.0.0:80", \
      "--socket", "0.0.0.0:81", \
      "--processes", "4", \
      "--gevent", "100", \
      "--module", "app" ]
