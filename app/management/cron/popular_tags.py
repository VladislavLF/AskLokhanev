import os
from app.models import *
from django.core.cache import cache
from django.db.models import Count


def update_popular_tags() -> None:
    ttl = int(os.getenv('POPULAR_TAGS_CACHE_TTL', '2678400'))
    object_list = Tag.objects.all()
    cache.set('popular_tags', object_list.annotate(num_questions=Count('question')).order_by('-num_questions')[:20], ttl)
