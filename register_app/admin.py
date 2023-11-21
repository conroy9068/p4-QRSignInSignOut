from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Location, Project, Role, SignInOutRegister, UserProfile


# Inline admin for UserProfile
class UserProfileInline(admin.StackedInline):
    """
    Inline admin representation of UserProfile model.

    Attributes:
        model (Model): The associated UserProfile model.
        can_delete (bool): Determines if profiles can be deleted.
        verbose_name_plural (str): The verbose name for the inline admin.
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'


# Custom UserAdmin that includes UserProfile
class UserAdmin(BaseUserAdmin):
    """
    Custom UserAdmin that includes a section for UserProfile.

    Attributes:
        inlines (tuple): Tuple containing inlines for the admin. Here, UserProfileInline is included.
    """
    inlines = (UserProfileInline,)


# Re-register UserAdmin to include UserProfileInline
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Admin class for Project
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin class for Project model.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
    """
    list_display = ('project_name', 'project_code', 'project_status')


# Register ProjectAdmin
admin.site.register(Project, ProjectAdmin)

# Admin class for Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    Admin class for Location model.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        list_editable (tuple): Fields that can be edited directly in the admin list view.
    """
    list_display = ('name', 'address', 'is_active')
    list_editable = ('is_active',)


# Admin class for SignInOutRegister
@admin.register(SignInOutRegister)
class SignInOutRegisterAdmin(admin.ModelAdmin):
    """
    Admin class for SignInOutRegister model.

    Attributes:
        list_display (list): Fields to display in the admin list view.
    """
    list_display = ['user', 'location', 'sign_in_time', 'sign_out_time']
