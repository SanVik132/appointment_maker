from django.contrib import admin
from api.models import *
from import_export.admin import ImportExportModelAdmin

@admin.register(Out1)
class ServicesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['flag', 'date']
    search_fields = ['date']


admin.site.register(Appointment)
admin.site.register(Time)    