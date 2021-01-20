from django.contrib import admin
from django.db import models
from django.contrib.flatpages.admin import FlatPageAdmin as FlatpageFormOld
from django.contrib.flatpages.models import FlatPage

from ckeditor.widgets import CKEditorWidget

# Register your models here.

admin.site.unregister(FlatPage)


class FlatPageAdmin(FlatpageFormOld):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


admin.site.register(FlatPage, FlatPageAdmin)
