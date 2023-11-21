from django.apps import AppConfig


class RegisterAppConfig(AppConfig):
    """
    AppConfig for the register_app Django app.

    This AppConfig sets the default_auto_field to
    "django.db.models.BigAutoField"
    and the name to "register_app".
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "register_app"
