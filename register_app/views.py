import os
from datetime import datetime, time
from io import BytesIO

import qrcode
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View

from .forms import (CreateProjectForm, LocationFormSet, ProjectSelectionForm,
                    SelectLocationSignInOut, UserProfileForm,
                    UserRegistrationForm)
from .models import Location, Project, SignInOutRegister, UserProfile


# Render the landing page for the app.
def home(request):
    """
    Render the landing page for the app.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered landing page HTML.
    """
    return render(request, 'landing_page.html')

# View function for user registration.


def register(request):
    """
    Handle user registration.

    If the request method is POST, validate the user creation form and save the user's information.
    If the form is valid, log the user in and redirect to their dashboard.
    If the form is invalid, print the errors to the console.
    If the request method is not POST, render the user creation form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()  # Save now

            login(request, user)

            messages.success(request, 'You are now registered and logged in.')
            return redirect('user_dashboard')
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'register_app/register.html', {'form': form})

# Check if a user is an administrator or a staff member.


def is_admin(user):
    """
    Check if the user is an administrator or a staff member.

    Args:
        user (User): The user to check.

    Returns:
        bool: True if the user is a superuser or staff, False otherwise.
    """
    return user.is_superuser or user.is_staff

# Add a newly created user to the 'Users' group.


def add_to_group(sender, user, created, **kwargs):
    """
    Add a newly created user to the 'Users' group.

    Args:
        sender (Model Class): The model class sending the signal.
        user (User): The user instance to add to the group.
        created (bool): Flag indicating if the user was created.
        kwargs (dict): Additional keyword arguments.

    Side-effects:
        Adds the user to the 'Users' group if it exists and the user is newly created.
        Prints a message to the console if the 'Users' group does not exist.
    """
    if created:
        try:
            group = Group.objects.get(name='Users')
            user.groups.add(group)
        except ObjectDoesNotExist:
            print("Group 'Users' does not exist.")


# Render the 'no_access.html' template.
def no_access(request):
    """
    Render the 'no_access.html' template when access is denied.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 'no_access.html' template.
    """
    return render(request, 'register_app/no_access.html')


# Render the admin panel page.
@login_required
@user_passes_test(is_admin, login_url='/no_access/')
def admin_panel(request):
    """
    Render the admin panel page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered admin panel page.
    """
    projects = Project.objects.all()

    # Fetch currently signed-in users
    clocked_in_users = SignInOutRegister.objects.filter(
        sign_out_time__isnull=True)

    return render(request, 'register_app/admin_panel.html', {'projects': projects, 'clocked_in_users': clocked_in_users})


# Handle signing in and out of a location.
@login_required
def sign_in_out_view(request, location_id):
    """
    Handle signing in and out of a location for a user.

    Args:
        request (HttpRequest): The HTTP request object.
        location_id (int): The ID of the location.

    Returns:
        HttpResponse: The HTTP response object.
    """
    location = get_object_or_404(Location, id=location_id)
    current_signin = SignInOutRegister.objects.filter(
        user=request.user, location_id=location_id, sign_out_time__isnull=True).first()

    if request.method == "POST":
        if not current_signin:
            SignInOutRegister.objects.create(
                user=request.user, location=location, sign_in_time=timezone.now())
            current_signin = SignInOutRegister.objects.filter(
                user=request.user, location_id=location_id, sign_out_time__isnull=True).first()
        else:
            current_signin.sign_out_time = timezone.now()
            current_signin.save()
            current_signin = None

    today_min = datetime.combine(datetime.today(), time.min)
    today_max = datetime.combine(datetime.today(), time.max)
    todays_signins = SignInOutRegister.objects.filter(
        user=request.user, sign_in_time__range=(today_min, today_max))

    context = {
        'location': location,
        'current_signin': current_signin,
        'todays_signins': todays_signins
    }

    if 'HTTP_HX_REQUEST' in request.META:
        return render(request, 'register_app/sign_in_out_content.html', context)
    else:
        return render(request, 'register_app/sign_in_out.html', context)


# Display a form to select a location.
@login_required
def select_location_view(request):
    """
    Display a form to select a location for sign in/out.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML template or a redirect to the sign in/out page.
    """
    form = SelectLocationSignInOut()
    if request.method == "POST":
        form = SelectLocationSignInOut(request.POST)
        if form.is_valid():
            location_id = form.cleaned_data['location'].id
            redirect_url = reverse('sign_in_out', args=[location_id])
            return HttpResponseRedirect(redirect_url)

    return render(request, 'register_app/select_location.html', {'form': form})

# Return a JSON response containing a list of locations.


class GetLocationsView(View):
    """
    Return a JSON list of locations for a given project ID.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A list of locations.
    """

    def get(self, request, *args, **kwargs):
        project_id = request.GET.get('project_id')
        locations = Location.objects.filter(
            project_id=project_id).values('id', 'name')
        return JsonResponse(list(locations), safe=False)

# Render the admin dashboard page.


@login_required
@user_passes_test(is_admin, login_url='/no_access/')
def admin_dashboard(request):
    """
    Render the admin dashboard page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered admin dashboard page.
    """
    return render(request, 'register_app/admin_dashboard.html')


# Render the user dashboard page.
@login_required
def user_dashboard(request):
    """
    Render the user dashboard page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered user dashboard page.
    """
    current_signin = SignInOutRegister.objects.filter(
        user=request.user, sign_out_time__isnull=True).first()
    past_signins = SignInOutRegister.objects.filter(
        user=request.user, sign_out_time__isnull=False).order_by('-sign_in_time')

    context = {
        'current_signin': current_signin,
        'past_signins': past_signins,
    }
    return render(request, 'register_app/user_dashboard.html', context)

# Render the profile view page.


@login_required
def view_profile(request):
    """
    Render the profile view page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered profile view page.
    """
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'register_app/view_profile.html', context)

# Handle profile editing.


@login_required
def edit_profile(request):
    """
    Handle profile editing.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered profile edit page or a redirect to the profile view.
    """
    try:
        # Assuming 'profile' is the related name for the UserProfile
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'register_app/edit_profile.html', {'form': form})


# Create a new project.
@user_passes_test(is_admin, login_url='/no_access/')
@login_required
def create_project(request):
    """
    Handle the creation of a new project.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered project creation page or a redirect to the edit project page.
    """
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = form.save()

            return redirect(reverse('edit_project', kwargs={'project_id': project.id}))
    else:
        form = CreateProjectForm()

    return render(request, 'register_app/create_project.html', {'form': form})

# Display the project selection form.


@login_required
def select_project_view(request):
    """
    Display the project selection form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered project selection form.
    """
    form = ProjectSelectionForm()
    if request.method == "POST":
        form = SelectLocationSignInOut(request.POST)
        if form.is_valid():
            location_id = form.cleaned_data['location'].id
            redirect_url = reverse('sign_in_out', args=[location_id])
            return HttpResponseRedirect(redirect_url)

    return render(request, 'register_app/select_project.html', {'form': form})

# Handle project editing.


@user_passes_test(is_admin, login_url='/no_access/')
@login_required
def edit_project(request, project_id):
    """
    Handle editing project details.

    Args:
        request (HttpRequest): The HTTP request object.
        project_id (int): The ID of the project to edit.

    Returns:
        HttpResponse: The rendered project editing page.
    """
    project = get_object_or_404(Project, id=project_id)

    # Create a form for project details
    if request.method == 'POST':
        form = CreateProjectForm(request.POST, instance=project)
        formset = LocationFormSet(request.POST, instance=project)
        if form.is_valid() and formset.is_valid():
            # Save project details
            form.save()
            messages.success(request, "Project details updated successfully.")

            # Check if a new location is being added
            new_location_name = request.POST.get('new_location_name')
            new_location_address = request.POST.get('new_location_address')
            new_location_description = request.POST.get(
                'new_location_description')

            if new_location_name and new_location_address and new_location_description:
                # Create a new location and associate it with the project
                new_location = Location(
                    name=new_location_name,
                    address=new_location_address,
                    description=new_location_description,
                    project=project,
                    is_active=True
                )
                new_location.save()
                messages.success(request, "New location added successfully.")

            formset.save()
            # Reinitialize form and formset with updated project data
            form = CreateProjectForm(instance=project)
            formset = LocationFormSet(instance=project)
        else:
            messages.error(
                request, "There was a problem updating the project.")
    else:
        form = CreateProjectForm(instance=project)
        formset = LocationFormSet(instance=project)

    return render(request, 'register_app/edit_project.html', {'form': form, 'formset': formset, 'project': project})

# Handle project deletion.


@user_passes_test(is_admin, login_url='/no_access/')
@login_required
def delete_project(request, project_id):
    """
    Handle the deletion of a project.

    Args:
        request (HttpRequest): The HTTP request object.
        project_id (int): The ID of the project to delete.

    Returns:
        HttpResponse: A redirect to the admin panel page.
    """
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return redirect('admin_panel')


# Handle the creation of location forms.
@user_passes_test(is_admin, login_url='/no_access/')
@login_required
def location_form(request, project_id):
    """
    Handle the creation of location forms.

    Args:
        request (HttpRequest): The HTTP request object.
        project_id (int): The ID of the project.

    Returns:
        HttpResponse: The rendered location form or a redirect.
    """
    project = Project.objects.get(pk=project_id)
    if request.method == 'POST':
        formset = LocationFormSet(
            request.POST, instance=project, prefix='locations')
        if formset.is_valid():
            formset.save()
            return redirect('register_app/location_list.html')
    else:
        formset = LocationFormSet(instance=project, prefix='locations')
    return render(request, 'register_app/create_location.html', {'formset': formset, 'project': project})


# QR code generation
@receiver(post_save, sender=Location)
def generate_qr_code(sender, instance, created, **kwargs):
    """
    Generate a QR code when a new location is created.

    Args:
        sender (Model Class): The model class sending the signal.
        instance (Location): The instance of the Location.
        created (bool): Flag indicating if the location was created.
        kwargs (dict): Additional keyword arguments.

    Side-effects:
        Generates and saves a QR code image for the location.
    """
    if created:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        url = f"https://qrsigninoutapp-c6f4e2915b2d.herokuapp.com/sign_in_out/{instance.id}/"
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        # Save the image to a BytesIO object
        img_byte_arr = BytesIO()
        img.save(img_byte_arr)

        # Create a name for the file
        filename = f"{instance.name}.png".replace(" ", "_")

        # Create the File object and save it to the model
        img_file = File(img_byte_arr, name=filename)
        instance.qr_code.save(filename, img_file)
        instance.save()


# QR code view
def view_qr_code(request, location_id):
    """
    Render the QR code view.

    Args:
        request (HttpRequest): The HTTP request object.
        location_id (int): The ID of the location.

    Returns:
        HttpResponse: A PNG image response of the QR code.
    """
    location = Location.objects.get(id=location_id)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    url = f"https://qrsigninoutapp-c6f4e2915b2d.herokuapp.com/sign_in_out/{location.id}/"
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


# QR code download
def download_qr(request, location_id):
    """
    Handle the download of a QR code.

    Args:
        request (HttpRequest): The HTTP request object.
        location_id (int): The ID of the location.

    Returns:
        HttpResponse: A response with the QR code image as an attachment.
    """
    location = Location.objects.get(id=location_id)

    with location.qr_code.open("rb") as qr_file:
        response = HttpResponse(qr_file.read(), content_type="image/png")

        # Set filename based on the saved QR code's name
        filename = location.qr_code.name.split('/')[-1]
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response
