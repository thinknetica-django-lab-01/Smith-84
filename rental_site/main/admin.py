from django.contrib import admin

from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

# Register your models here.

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)