from django.contrib import admin
from main.models import *
from django.db.models import Model

for var_name, var in dict(locals()).iteritems():
    if isinstance(var, type) and issubclass(var, Model) and var is not Model:
        class Admin(admin.ModelAdmin):
            pass
        admin.site.register(var, Admin)