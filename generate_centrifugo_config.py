import os
import json
from pathlib import Path
import sys


config = {
    "secret": os.getenv('CENTRIFUGO_SECRET_KEY'),
    "admin_password": os.getenv('CENTRIFUGO_ADMIN_PASSWORD'),
    "admin_secret": os.getenv('CENTRIFUGO_ADMIN_SECRET'),
    "api_key": os.getenv('CENTRIFUGO_API_KEY'),
    "allowed_origins": os.getenv('CENTRIFUGO_ALLOWED_ORIGINS', '').split(','),
    "web": os.getenv('CENTRIFUGO_WEB', 'false').lower() == 'true',
    "admin": os.getenv('CENTRIFUGO_ADMIN', 'false').lower() == 'true',
    "publish": os.getenv('CENTRIFUGO_PUBLISH', 'false').lower() == 'true',
    "anonymous": os.getenv('CENTRIFUGO_ANONYMOUS', 'false').lower() == 'true',
    "presence": os.getenv('CENTRIFUGO_PRESENCE', 'false').lower() == 'true',
    "join_leave": os.getenv('CENTRIFUGO_JOIN_LEAVE', 'false').lower() == 'true',
    "history_size": int(os.getenv('CENTRIFUGO_HISTORY_SIZE', 10)),
    "history_ttl": os.getenv('CENTRIFUGO_HISTORY_TTL', '300s'),
    "debug": os.getenv('CENTRIFUGO_DEBUG', 'false').lower() == 'true',
    "log_level": os.getenv('CENTRIFUGO_LOG_LEVEL', 'info'),
    "allow_subscribe_for_client": os.getenv('CENTRIFUGO_ALLOW_SUBSCRIBE_FOR_CLIENT', 'false').lower() == 'true',
    "client_anonymous": os.getenv('CENTRIFUGO_CLIENT_ANONYMOUS', 'false').lower() == 'true',
    "http_stream": {
        "enabled": True,
        "extra_headers": ["Origin"]
    },
    "proxy_http_endpoints": [
        {
            "name": "django",
            "http_url": f"http://{os.getenv('DJANGO_HOST', 'web')}:{os.getenv('DJANGO_PORT', '8000')}",
            "extra_headers": [
                {
                    "name": "X-Real-IP",
                    "value": "$remote_addr"
                }
            ]
        }
    ]
}

config["allowed_origins"] = [origin.strip() for origin in config["allowed_origins"] if origin.strip()]
config_path = Path(os.getenv('CENTRIFUGO_CONFIG_PATH', '/centrifugo/config.json'))
config_path.parent.mkdir(parents=True, exist_ok=True)

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

sys.exit(0)
