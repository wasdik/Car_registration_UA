from django.contrib import admin

from .models import Car, Brand, Model, Fuel, Kind, Body, Purpose


class BrandAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ('name',)
    search_fields = ['name']


class CarAdmin(admin.ModelAdmin):
    list_filter = ['model']
    search_fields = ['license_plate']


admin.site.register(Car, CarAdmin)

admin.site.register(Brand, BrandAdmin)
admin.site.register(Model)
admin.site.register(Fuel)
admin.site.register(Kind)
admin.site.register(Body)
admin.site.register(Purpose)
