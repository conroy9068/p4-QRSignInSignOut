from datetime import datetime, time
import os

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.views import View
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.core.files import File
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import Location, Project, SignInOutRegister, UserProfile
from .forms import (
    CreateProjectForm, 
    LocationFormSet, 
    ProjectSelectionForm, 
    SelectLocationSignInOut, 
    UserProfileForm, 
    UserRegistrationForm, 
    UserUpdateForm, 
    UserProfileForm
)
import qrcode
from django.dispatch import receiver

def home(request):
    return render(request, 'landing_page.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()  # Save now
            
            login(request, user)

            # Update UserProfile
            company_name = request.POST.get('company_name')
            date_of_birth = request.POST.get('date_of_birth')
            phone_number = request.POST.get('phone_number')
            
            user_profile = UserProfile.objects.get(user=user)
            user_profile.company_name = company_name
            user_profile.date_of_birth = date_of_birth
            user_profile.phone_number = phone_number
            user_profile.save()

            messages.success(request, 'You are now registered and logged in.')
            return redirect('user_dashboard')
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'register_app/register.html', {'form': form})




# def register(request):
#     print("Inside register view")
#     print(request.POST)
#     print(user_form.is_valid())
#     print(profile_form.is_valid())
#     print(user_form.errors)
#     print(profile_form.errors)

#     if request.method == 'POST':

#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user_form.cleaned_data['password'])
#             user.save()

#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.save()
            
#             # Add user to a group
#             add_to_group(None, user, True)

#             # Authenticate and login (optional)
#             authenticated_user = authenticate(username=user.username, password=user_form.cleaned_data['password'])
#             if authenticated_user:
#                 login(request, authenticated_user)

#             messages.success(request, "Registration successful!")
#             return redirect('login')
#         else:
#             print("User Form Errors:", user_form.errors)
#             print("Profile Form Errors:", profile_form.errors)
#             return render(request, 'register_app/register.html', {'user_form': user_form, 'profile_form': profile_form})
        
#     else:
#         user_form = UserRegistrationForm()
#         profile_form = UserProfileForm()

#     return render(request, 'register_app/register.html', {'user_form': user_form, 'profile_form': profile_form})


def is_admin(user):
    return user.is_superuser or user.is_staff

def add_to_group(sender, user, created, **kwargs):
    if created:
        try:
            group = Group.objects.get(name='Users')
            user.groups.add(group)
        except ObjectDoesNotExist:
            print("Group 'Users' does not exist.")
        
@user_passes_test(is_admin, login_url='/no_access/')
@login_required
def location_list(request):
    locations = Location.objects.filter(is_active=True)
    return render(request, 'register_app/user_dashboard', {'locations': locations})

def no_access(request):
    return render(request, 'register_app/no_access.html')


# Sign in and sign out views
@login_required
def sign_in_out_view(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    current_signin = SignInOutRegister.objects.filter(user=request.user, location_id=location_id, sign_out_time__isnull=True).first()

    if request.method == "POST":
        if not current_signin:
            SignInOutRegister.objects.create(user=request.user, location=location, sign_in_time=timezone.now())
            current_signin = SignInOutRegister.objects.filter(user=request.user, location_id=location_id, sign_out_time__isnull=True).first()
        else:
            current_signin.sign_out_time = timezone.now()
            current_signin.save()
            current_signin = None  

    today_min = datetime.combine(datetime.today(), time.min)
    today_max = datetime.combine(datetime.today(), time.max)
    todays_signins = SignInOutRegister.objects.filter(user=request.user, sign_in_time__range=(today_min, today_max))

    context = {
        'location': location,
        'current_signin': current_signin,
        'todays_signins': todays_signins
    }
    
    if 'HTTP_HX_REQUEST' in request.META:
        return render(request, 'register_app/sign_in_out_content.html', context)
    else:
        return render(request, 'register_app/sign_in_out.html', context)
    
# LOCATION VIEWS
@login_required
def select_location_view(request):
    form = SelectLocationSignInOut()
    if request.method == "POST":
        form = SelectLocationSignInOut(request.POST)
        if form.is_valid():
            location_id = form.cleaned_data['location'].id
            redirect_url = reverse('sign_in_out', args=[location_id])
            return HttpResponseRedirect(redirect_url)

    return render(request, 'register_app/select_location.html', {'form': form})

class GetLocationsView(View):
    def get(self, request, *args, **kwargs):
        project_id = request.GET.get('project_id')
        locations = Location.objects.filter(project_id=project_id).values('id', 'name')
        return JsonResponse(list(locations), safe=False)


# PROJECT VIEWS
@login_required
def select_project_view(request):
    form = ProjectSelectionForm()
    if request.method == "POST":
        form = SelectLocationSignInOut(request.POST)
        if form.is_valid():
            location_id = form.cleaned_data['location'].id
            redirect_url = reverse('sign_in_out', args=[location_id])
            return HttpResponseRedirect(redirect_url)
        
    return render(request, 'register_app/select_project.html', {'form': form})


# ADMIN VIEWS
@login_required
@user_passes_test(is_admin, login_url='/no_access/')
def admin_dashboard(request):
    return render(request, 'register_app/admin_dashboard.html')


# USER VIEWS
@login_required
def user_dashboard(request):
    current_signin = SignInOutRegister.objects.filter(user=request.user, sign_out_time__isnull=True).first()
    past_signins = SignInOutRegister.objects.filter(user=request.user, sign_out_time__isnull=False).order_by('-sign_in_time')

    context = {
        'current_signin': current_signin,
        'past_signins': past_signins,
    }
    return render(request, 'register_app/user_dashboard.html', context)

@login_required
def view_profile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'register_app/view_profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = UserUpdateForm(instance=request.user)
        
    return render(request, 'register_app/edit_profile.html', {'form': form})

# Project & Location views
@login_required
def create_project(request):
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        formset = LocationFormSet(request.POST, prefix='locations')
        if form.is_valid() and formset.is_valid():
            project = form.save()
            formset.instance = project
            formset.save()
            return redirect('user_dashboard.html')  # Make sure 'user_dashboard.html' is the correct redirect URL
    else:
        form = CreateProjectForm()
        formset = LocationFormSet(prefix='locations')
    return render(request, 'register_app/create_project.html', {'form': form, 'formset': formset})

# @login_required
# def create_location(request):
#     if request.method == 'POST':
#         project_form = SelectProjectForm(request.POST)
#         if project_form.is_valid():
#             project_id = project_form.cleaned_data.get('project')
#             location_form = LocationForm(request.POST, project_id=project_id)
#             if location_form.is_valid():
#                 location_form.save()
#                 return JsonResponse({'status': 'success'})
#             else:
#                 return JsonResponse({'status': 'error', 'errors': location_form.errors})
#         else:
#             return JsonResponse({'status': 'error', 'errors': project_form.errors})
#     else:
#         project_form = SelectProjectForm()
#         location_form = LocationForm()
#     return render(request, 'your_template.html', {'project_form': project_form, 'location_form': location_form})



# QR code generation
@receiver(post_save, sender=Location)
def generate_qr_code(sender, instance, created, **kwargs):
    if created:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        url = f"http://127.0.0.0/sign_in/{instance.id}/"
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img_path = os.path.join(settings.BASE_DIR, f"media/qr_codes/{instance.id}.png")
        directory = os.path.dirname(img_path)
        img.save(img_path)
        instance.qr_code = img_path
        instance.save()

# QR code view
def view_qr_code(request, location_id):
    location = Location.objects.get(id=location_id)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    url = f"http://127.0.0.0/sign_in/{location.id}/"
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

