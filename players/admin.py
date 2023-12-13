from django.contrib import admin

from .models import *


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team')
    list_display_links = ('name',)
    search_fields = ('name', 'team')
    list_filter = ('team',)
    prepopulated_fields = {"slug": ("name",)}


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_full', 'contacts')
    list_display_links = ('name',)
    list_editable = ('is_full',)
    list_filter = ('is_full',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
