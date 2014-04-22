from django.contrib import admin
from timeline import models as timeline_models
from django.db.models.base import ModelBase

for name, var in timeline_models.__dict__.items():
    if type(var) is ModelBase:
        try:
            admin.site.register(var)
        except:
            pass