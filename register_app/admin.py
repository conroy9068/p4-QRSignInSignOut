from django.contrib import admin
from .models import Location, SignInOutRegister

# Register your models here.
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'description']

# Register the SignInOutRegister model
@admin.register(SignInOutRegister)
class SignInOutRegisterAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'sign_in_time', 'sign_out_time']