#!/bin/bash

echo "Starting MySQL initialization..."

until mysqladmin ping -h localhost -u root -p$MYSQL_ROOT_PASSWORD --silent; do
    echo "Waiting for MySQL..."
    sleep 2
done

echo "MySQL is ready. Configuring..."

mysql -u root -p$MYSQL_ROOT_PASSWORD << EOF
DELETE FROM mysql.user WHERE User='';

DROP DATABASE IF EXISTS test;

CREATE DATABASE IF NOT EXISTS \`$MYSQL_DATABASE\`
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';

GRANT ALL PRIVILEGES ON \`$MYSQL_DATABASE\`.* TO '$MYSQL_USER'@'%';
GRANT CREATE, ALTER, DROP, REFERENCES ON *.* TO '$MYSQL_USER'@'%';

FLUSH PRIVILEGES;

SELECT 'Database users:' AS '';
SELECT user, host FROM mysql.user;
SELECT '' AS '';
SELECT 'Grants for $MYSQL_USER:' AS '';
SHOW GRANTS FOR '$MYSQL_USER'@'%';
EOF

echo "========================================"
echo "MySQL initialization COMPLETE!"
echo "Database: $MYSQL_DATABASE"
echo "User: $MYSQL_USER"
echo "Connect from Django: mysql://$MYSQL_USER:$MYSQL_PASSWORD@db:3306/$MYSQL_DATABASE"
echo "========================================"