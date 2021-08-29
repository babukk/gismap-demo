
# from django.contrib import admin
from django.contrib.gis import admin

from task_manager.models import Task, Checkpoint

# admin.site.register(Task)
# admin.site.register(Checkpoint)

@admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
class TaskAdmin(admin.OSMGeoAdmin):
    list_display = ('id', 'when_created', 'lat', 'lon', 'assigned_user', 'when_in', 'when_out', 'status',)

    def when_created(self, obj):
        try:
            return obj.datetime_created.strftime("%d.%m.%Y %H:%M")
        except AttributeError:
            return None

    def when_in(self, obj):
        try:
            return obj.datetime_in.strftime("%d.%m.%Y %H:%M")
        except AttributeError:
            return None

    def when_out(self, obj):
        try:
            return obj.datetime_out.strftime("%d.%m.%Y %H:%M")
        except AttributeError:
            return None

    when_created.short_description = "Дата-время создания"
    when_in.short_description = "Дата-время прибытия"
    when_out.short_description = "Дата-время выбытия"

    def lat(self, object):
        return object.lat

    lat.short_description = "Широта"

    def lon(self, object):
        return object.lon

    lon.short_description = "Долгота"


@admin.register(Checkpoint)
# class CheckpointAdmin(admin.ModelAdmin):
class CheckpointAdmin(admin.OSMGeoAdmin):
    list_display = ('id', 'when_created', 'lat', 'lon', 'user', )
    # list_editable = ('point', 'user', )

    def when_created(self, obj):
        return obj.datetime_created.strftime("%d.%m.%Y %H:%M")

    when_created.short_description = "Дата-время создания"

    def lat(self, object):
        return object.lat

    lat.short_description = "Широта"

    def lon(self, object):
        return object.lon

    lon.short_description = "Долгота"

