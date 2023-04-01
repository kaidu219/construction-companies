from functools import lru_cache
import json
import os

from django.conf import settings


def building_info(request):
    with open(os.path.join(settings.BASE_DIR, 'storage.json')) as f:
        ctx = json.load(f)

        return ctx