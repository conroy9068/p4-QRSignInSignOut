from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Role(models.Model):
    """
    Model for users job role in the system.

    Attributes:
        name (str): The name of the role.
        description (str): A description of the users job role.
    """
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """
    The UserProfile model is an extension of Django's built-in User model.
    It uses a one-to-one relationship with the User model to associate
    additional information with each user.

    Attributes:
        user (User): A one-to-one field representing the user associated
        with the profile.
        role (Role): A foreign key representing the a users role
        associated with the profile.
        company_name (str): A string representing the name of the
        company associated with the profile.
        date_of_birth (date): A date representing the date of birth
        associated with the profile.
        phone_number (str): A string representing the phone number
        associated with the profile.
        created_at (datetime): A datetime representing the date and
        time the profile was created.
        updated_at (datetime): A datetime representing the date and
        time the profile was last updated.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    company_name = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Project(models.Model):
    """
    Model for project information.

    Attributes:
        project_name (str): The name of the project.
        project_code (str): The code of the project.
        project_status (str): The status of the project. Can be either
        'Active' or 'Inactive'.
        project_url (str): The URL of the project.
        site_manager_name (str): The name of the site manager.
        site_manager_email (str): The email of the site manager.
        project_manager_name (str): The name of the project manager.
        project_manager_email (str): The email of the project manager.
        created_at (datetime): The date and time when the project was created.
        updated_at (datetime): The date and time when the project was
        last updated.
    """
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]

    project_name = models.CharField(max_length=50)
    project_code = models.CharField(max_length=50)
    project_status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=ACTIVE,
        null=True
    )
    project_url = models.CharField(max_length=200, null=True)
    site_manager_name = models.CharField(max_length=100, null=True)
    site_manager_email = models.EmailField(null=True)
    project_manager_name = models.CharField(max_length=100, null=True)
    project_manager_email = models.EmailField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.project_name


class Location(models.Model):
    """
    A model for location(s) info that is associated with a project.

    Attributes:
        name (str): The name of the location.
        project (ForeignKey): The project associated with the location.
        address (str): The address of the location.
        description (str): A description of the location.
        is_active (bool): Whether the location is currently active.
        qr_code (FileField): The QR code associated with the location.
        created_at (DateTimeField): The date and time the location was created.
        updated_at (DateTimeField): The date and time the location was
        last updated.
    """
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    address = models.TextField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    qr_code = models.FileField(upload_to='qr_codes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class SignInOutRegister(models.Model):
    """
    A model to represent the sign-in and sign-out times of users at
    various locations.

    Attributes:
        user (ForeignKey): The user associated with the sign-in/sign-out.
        location (ForeignKey): The location associated with
        the sign-in/sign-out.
        sign_in_time (DateTimeField): The date and time the user signed in.
        sign_out_time (DateTimeField): The date and time the user signed out.
        created_at (DateTimeField): The date and time the sign-in/sign-out
        was created.
        updated_at (DateTimeField): The date and time the sign-in/sign-out
        was last updated.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    sign_in_time = models.DateTimeField()
    sign_out_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.location.name}"
