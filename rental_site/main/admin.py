from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as FlatpageFormOld
from django.contrib.flatpages.models import FlatPage

from ckeditor.widgets import CKEditorWidget
from .models import *

# Register your models here.

admin.site.unregister(FlatPage)


class FlatPageAdmin(FlatpageFormOld):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


admin.site.register(FlatPage, FlatPageAdmin)


admin.site.register(Region)
admin.site.register(Ad)
