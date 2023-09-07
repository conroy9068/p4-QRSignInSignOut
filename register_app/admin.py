from django.contrib import admin
from .models import Location, SignInOutRegister


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'is_active') 
    list_editable = ('is_active',) 


# Register the SignInOutRegister model
@admin.register(SignInOutRegister)
class SignInOutRegisterAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'sign_in_time', 'sign_out_time']