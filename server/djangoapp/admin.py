from django.contrib import admin
from .models import CarMake, CarModel


class CarModelInline(admin.TabularInline):
    model = CarModel

class CarModelAdmin(admin.ModelAdmin):
    fields = ["name", "dealer_id", "type", "year", "make"]

class CarMakeAdmin(admin.ModelAdmin):
    fields = ["name", "description"]
    inlines = [CarModelInline]


# Register your models here.

admin.site.register(CarMake, CarMakeAdmin)

admin.site.register(CarModel, CarModelAdmin)

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
