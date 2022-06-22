from django.contrib import admin

from django.contrib import admin
from .models import City


class CitiesAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(City, CitiesAdmin)
