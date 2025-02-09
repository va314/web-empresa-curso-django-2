from django.contrib import admin
from .models import Service

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'available', 'created')
    list_editable = ('price', 'available')
    readonly_fields = ('created', 'updated')

admin.site.register(Service, ServiceAdmin)
