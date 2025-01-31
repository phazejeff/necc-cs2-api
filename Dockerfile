FROM python:3

RUN apt-get update && apt-get install -y cron
RUN echo "0 * * * * /usr/local/bin/python3 /app/populate_db.py >> /var/log/cron.log 2>&1" > /etc/cron.d/populate-db-cron

RUN chmod 0644 /etc/cron.d/populate-db-cron
RUN crontab /etc/cron.d/populate-db-cron
RUN touch /var/log/cron.log

# Copy your existing files
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY app.py .
COPY populate_db.py .
COPY faceit ./faceit
COPY necc ./necc
COPY database ./database

ARG workers=4
ENV WORKERS=${workers}

CMD cron && gunicorn -w $WORKERS -b 0.0.0.0 app:app