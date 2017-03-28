from django.contrib import admin
from services.models import Option
import utils

class OptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']
    ordering = ['name']

admin.site.site_header = "Example Admin"
admin.site.site_url = "http://www.example.com"
admin.site.register(Option, OptionAdmin)
