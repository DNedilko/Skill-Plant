RUN apt-get update && apt-get install -y cron
COPY crontab-scripts /etc/cron.d/crontab-scripts
RUN chmod 0644 /etc/cron.d/crontab-scripts && \
    crontab /etc/cron.d/crontab-scripts