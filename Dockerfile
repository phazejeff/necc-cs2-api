FROM python:3

RUN apt-get update && apt-get install -y cron

# Copy your existing files
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY app.py .
COPY remove_wrong_ff.py .
COPY populate_db.py .
COPY faceit ./faceit
COPY necc ./necc
COPY database ./database

# Create cron job
RUN echo "*/1 * * * * /usr/local/bin/python3 /populate_db.py >> /var/log/cron.log 2>&1" > /etc/cron.d/populate-db-cron

RUN chmod 0644 /etc/cron.d/populate-db-cron
RUN crontab /etc/cron.d/populate-db-cron
RUN touch /var/log/cron.log

ARG workers=4
ENV WORKERS=${workers}

# Create entrypoint script
RUN echo '#!/bin/bash\nprintenv > /etc/environment\ncron\nexec gunicorn -w $WORKERS -b 0.0.0.0 app:app' > /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
