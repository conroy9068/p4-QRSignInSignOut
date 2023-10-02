from django.contrib import admin
from .models import Location, Project, Role, SignInOutRegister
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Role)


admin.site.register(Project)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'is_active') 
    list_editable = ('is_active',) 


# Register the SignInOutRegister model
@admin.register(SignInOutRegister)
class SignInOutRegisterAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'sign_in_time', 'sign_out_time']