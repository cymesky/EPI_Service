# Install python
FROM python:3.10

# Set workdir
WORKDIR /opt/data

# Copy files
COPY requirements.txt .
COPY app.py .
COPY settings.py .
COPY __init__.py .

# Copy crontab to container
COPY crontab /etc/cron.d/data-cron-job

# Copy folders
COPY db_tools/ ./db_tools/
COPY markets/ ./markets/

# Install requirements modules
RUN pip install --no-cache-dir -r requirements.txt

# Install cron
RUN apt-get update && apt-get install -y cron

# Rights for cronjob
RUN chmod 0644 /etc/cron.d/data-cron-job

# Enable logs for cron
RUN touch /var/log/cron.log

# Set environment
ENV PYTHONPATH=/opt/

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Magic happens
RUN apt-get install -y google-chrome-stable

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Start data service and cron
CMD cron && python /opt/data/app.py >> /var/log/cron.log 2>&1 && tail -f /var/log/cron.log
# CMD python /opt/data/app.py