FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-libmysqlclient-dev \
    pkg-config \
    nginx \
    curl \
    netcat-openbsd \
    cron \
    gettext-base \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /etc/nginx/conf.d && \
    mkdir -p /var/log/nginx && \
    mkdir -p /app/nginx/cache && \
    mkdir -p /app/logs && \
    mkdir -p /app/static && \
    mkdir -p /app/media

RUN touch /var/log/cron.log

COPY nginx/nginx.template.conf /app/nginx/nginx.template.conf

RUN cat > /etc/cron.d/django-cron << 'EOF'
* * * * * root cd /app && python manage.py crontab run $(crontab -l 2>/dev/null | grep -o '[a-f0-9]\{32\}') >> /var/log/cron.log 2>&1
EOF

RUN chmod 0644 /etc/cron.d/django-cron

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/app/entrypoint.sh"]