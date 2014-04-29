from cms.models import PluginModelBase
from django.contrib import admin
from timeline import models as tm
from django.contrib.admin.sites import AlreadyRegistered
from django.db.models.base import ModelBase


if '__all__' in dir(tm):
    models = filter(lambda x: x[0] in tm.__all__, tm.__dict__.items())
else:
    models = tm.__dict__.items()
for name, var in models:
    if type(var) in [ModelBase, PluginModelBase]:
        try:
            admin.site.register(var)
        except AlreadyRegistered, ex:
            pass

