from django.contrib import admin

from main_app.models import House, Dragon, Quest


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'wins', 'is_ruling',]
    list_filter = ['is_ruling',]
    search_fields = ['name', 'motto',]
    ordering = ['-wins',]
    readonly_fields = ['modified_at',]


@admin.register(Dragon)
class DragonAdmin(admin.ModelAdmin):
    list_display = ['name', 'power', 'wins',  'breath', 'is_healthy',]
    list_filter = ['is_healthy', 'breath',]
    search_fields = ['name', 'breath',]
    ordering = ['-wins',]
    readonly_fields = ['modified_at', ]


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'reward', 'start_time',]
    list_filter = ['start_time', 'host__name',]
    search_fields = ['host__name',]
    ordering = ['start_time',]
    readonly_fields = ['modified_at',]

