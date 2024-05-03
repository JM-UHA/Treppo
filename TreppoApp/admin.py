from django.contrib import admin

from .models import MODELS

# Register your models here.

for model in MODELS:
    admin.site.register(model)
