from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as FlatpageFormOld
from django.contrib.flatpages.models import FlatPage

from ckeditor.widgets import CKEditorWidget
from .models import Ad, Region, Apartment, Room, Garage, LandPlot, Profile, Image, Tag
from django.db import models

# Register your models here.

admin.site.unregister(FlatPage)


class FlatPageAdmin(FlatpageFormOld):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


def make_published(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = 'published'
        obj.save()


def make_archival(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = 'archive'
        obj.save()


class TagFilter(admin.SimpleListFilter):
    title = 'Тэги'
    parameter_name = 'tag'

    def lookups(self, request, model_admin):
        return list([(tag['id'], tag['name']) for tag in Tag.objects.all().values('id', 'name').distinct()])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tag__id=self.value())



class AdAdmin(admin.ModelAdmin):
    actions = [make_published, make_archival]
    list_display = ('description', 'date_added', 'status')
    list_filter = (TagFilter,)


make_published.short_description = "Опубликовать объявления"
make_archival.short_description = "Отправить в архив"


admin.site.register(Ad, AdAdmin)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Region)
admin.site.register(Apartment)
admin.site.register(Room)
admin.site.register(Garage)
admin.site.register(LandPlot)
admin.site.register(Profile)
admin.site.register(Image)
admin.site.register(Tag)
