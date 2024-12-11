
import os

if os.getenv("DJANGO_ENV") == "production":
    from .production import *
elif os.getenv("DJANGO_ENV") == "local":
    from .local import *
else:
    from .base import *
