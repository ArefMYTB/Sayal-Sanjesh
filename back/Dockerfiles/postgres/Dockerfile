FROM postgres:12

# Install necessary packages
RUN apt-get update && apt-get install -y cron mutt
COPY sayalsanjesh.sql /
## Copy the backup script into the container
#COPY backup_script.sh /usr/local/bin/backup_script.sh
#
## Set permissions for the backup script
#RUN chmod +x /usr/local/bin/backup_script.sh
#
## Add a cron job to run the backup script daily at midnight
#RUN echo "0 0 * * * /usr/local/bin/backup_script.sh" | crontab -
#
## Start cron service
#CMD ["cron", "-f"]