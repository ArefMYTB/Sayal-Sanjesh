#!/bin/bash

DB_USER="postgres"
DB_NAME="sayalsanjesh"
BACKUP_DIR="/backup"

DATE=$(date +%Y%m%d%H%M%S)

# Backup the database
pg_dump -U $DB_USER $DB_NAME > $BACKUP_DIR/$DB_NAME-$DATE.sql

# Send backup via email (optional)
#mutt -s "Database Backup" -a $BACKUP_DIR/$DB_NAME-$DATE.sql -- ahmadian.mahziyar@gmail.com < /dev/null