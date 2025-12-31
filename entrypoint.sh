#!/bin/bash
set -e

echo "Starting web container"

echo "Generating centrifugo config"
python /app/generate_centrifugo_config.py

if [ -f "/centrifugo/config.json" ]; then
    echo "Centrifugo config generated"
else
    echo "Centrifugo config not generated!"
    exit 1
fi

echo "Creating directories..."
mkdir -p /app/static
mkdir -p /app/media
mkdir -p /app/logs
mkdir -p /app/nginx/cache

echo "Running cron..."
cron

echo "Setting up Nginx variables..."
export NGINX_WORKER_CONNECTIONS=${NGINX_WORKER_CONNECTIONS:-1024}
export NGINX_CACHE_PATH=${NGINX_CACHE_PATH:-/app/nginx/cache}
export NGINX_ACCESS_LOG_PATH=${NGINX_ACCESS_LOG_PATH:-/var/log/nginx/access.log}
export NGINX_ERROR_LOG_PATH=${NGINX_ERROR_LOG_PATH:-/var/log/nginx/error.log}
export NGINX_GZIP_COMP_LEVEL=${NGINX_GZIP_COMP_LEVEL:-6}
export NGINX_GZIP_BUFFERS=${NGINX_GZIP_BUFFERS:-"16 8k"}
export NGINX_CACHE_ZONE_SIZE=${NGINX_CACHE_ZONE_SIZE:-10m}
export NGINX_CACHE_MAX_SIZE=${NGINX_CACHE_MAX_SIZE:-50m}
export NGINX_CACHE_INACTIVE=${NGINX_CACHE_INACTIVE:-24h}
export NGINX_PORT=${NGINX_PORT:-80}
export NGINX_SERVER_NAME=${NGINX_SERVER_NAME:-localhost}
export STATIC_ROOT=${STATIC_ROOT:-/app/static}
export MEDIA_ROOT=${MEDIA_ROOT:-/app/media}
export GUNICORN_HOST=${GUNICORN_HOST:-0.0.0.0}
export GUNICORN_PORT=${GUNICORN_PORT:-8000}
export NGINX_CACHE_VALID_TIME=${NGINX_CACHE_VALID_TIME:-10m}

echo "Generating Nginx config..."
envsubst '${NGINX_WORKER_CONNECTIONS} ${NGINX_CACHE_PATH} ${NGINX_ACCESS_LOG_PATH} ${NGINX_ERROR_LOG_PATH} ${NGINX_GZIP_COMP_LEVEL} ${NGINX_GZIP_BUFFERS} ${NGINX_CACHE_ZONE_SIZE} ${NGINX_CACHE_MAX_SIZE} ${NGINX_CACHE_INACTIVE} ${NGINX_PORT} ${NGINX_SERVER_NAME} ${STATIC_ROOT} ${MEDIA_ROOT} ${GUNICORN_HOST} ${GUNICORN_PORT} ${NGINX_CACHE_VALID_TIME}' < /app/nginx/nginx.template.conf > /etc/nginx/nginx.conf

echo "Running Nginx..."
nginx

echo "Waiting for database..."
counter=0
max_attempts=${DB_MAX_ATTEMPTS:-30}
while ! nc -z ${MYSQL_HOST:-db} ${MYSQL_PORT:-3306}; do
    echo "MySQL Waiting... ($((counter+1))/$max_attempts)"
    counter=$((counter+1))
    if [ $counter -eq $max_attempts ]; then
        echo "Failed to connect to database after $max_attempts attempts"
        break
    fi
    sleep 2
done

echo "Waiting for Memcached..."
counter=0
max_attempts=${MEMCACHED_MAX_ATTEMPTS:-10}
while ! nc -z ${MEMCACHED_HOST:-memcached} ${MEMCACHED_PORT:-11211}; do
    echo "Waiting for Memcached... ($((counter+1))/$max_attempts)"
    counter=$((counter+1))
    if [ $counter -eq $max_attempts ]; then
        echo "Failed to connect to Memcached after $max_attempts attempts"
        break
    fi
    sleep 2
done

echo "Creating database migrations..."
python manage.py makemigrations --noinput
echo "Migrations created"

echo "Database migrations..."
python manage.py migrate --noinput
echo "Migrations completed successfully"

echo "Checking if database needs cleaning..."
if [ "${RESET_DB_ON_START}" = "True" ] || [ "${RESET_DB_ON_START}" = "true" ] || [ "${RESET_DB_ON_START}" = "1" ]; then
    echo "Clearing database..."

    python manage.py shell -c "
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
    cursor.execute('SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE()')
    tables = [row[0] for row in cursor.fetchall() if row[0] != 'django_migrations']
    for table in tables:
        try:
            cursor.execute(f'TRUNCATE TABLE \`{table}\`;')
            print(f'Cleared: {table}')
        except Exception as e:
            print(f'Clearing error {table}: {e}')
    cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
print('The database has been cleared.')
"
else
    echo "Skipping database cleaning (RESET_DB_ON_START=${RESET_DB_ON_START})"
fi

echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os

User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')

if username and password and email:
    try:
        user, created = User.objects.update_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True
            }
        )
        user.set_password(password)
        user.save()

        if created:
            print(f'Superuser created: {username}')
        else:
            print(f'Superuser updated: {username}')
    except Exception as e:
        print(f'Error creating superuser: {e}')
else:
    print('Superuser environment variables not set. Skipping...')
"

if [ "${DEBUG}" = "True" ] || [ "${DEBUG}" = "true" ] || [ "${DEBUG}" = "1" ]; then
  echo "Filling the database with test data..."
  FILL_DB_RATIO=${FILL_DB_RATIO}
  echo "We use ratio=$FILL_DB_RATIO"
  python manage.py fill_db "$FILL_DB_RATIO"
fi

echo "Adding cron jobs..."
python manage.py crontab add
echo "Current cron jobs:"
python manage.py crontab show

echo "Initializing cache (first run)..."
python manage.py shell -c "
from django.core.cache import cache
from app.models import Tag, Profile
from django.db.models import Count
import os

cache.delete('popular_tags')
cache.delete('top_users')

try:
    tags_cache_ttl = int(os.getenv('TAGS_CACHE_TTL', '2678400'))
    tags = list(Tag.objects.annotate(num_questions=Count('question')).order_by('-num_questions')[:20])
    cache.set('popular_tags', tags, tags_cache_ttl)
    print(f'Added to cache: {len(tags)} popular tags (TTL: {tags_cache_ttl} сек.)')
except Exception as e:
    print(f'Error caching tags: {e}')

try:
    users_cache_ttl = int(os.getenv('USERS_CACHE_TTL', '604800'))
    users = list(Profile.objects.all().order_by('-rating')[:10])
    cache.set('top_users', users, users_cache_ttl)
    print(f'Added to cache: {len(users)} top users (TTL: {users_cache_ttl} сек.)')
except Exception as e:
    print(f'Error caching users: {e}')
"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Launching Gunicorn..."
exec gunicorn -c gunicorn/gunicorn.conf.py ask_lokhanev.wsgi:application