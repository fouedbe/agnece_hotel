# voyage/admin.py

from django.contrib import admin
from .models import Customer,Hotel,Voiture
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Customer, CustomerAdmin)

class HotelAdmin(admin.ModelAdmin):
    pass
admin.site.register(Hotel, HotelAdmin)
class VoitureAdmin(admin.ModelAdmin):
    pass
admin.site.register(Voiture, VoitureAdmin)
