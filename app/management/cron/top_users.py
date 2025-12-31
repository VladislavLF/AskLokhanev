import os
from app.models import *
from django.core.cache import cache


def update_top_users() -> None:
    ttl = int(os.getenv('TOP_USERS_CACHE_TTL', '604800'))
    top_users = Profile.objects.all().order_by('-rating')[:10]
    cache.set('top_users', top_users, ttl)
