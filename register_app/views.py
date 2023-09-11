from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Location, SignInOutRegister
from django.utils import timezone
from django.http import JsonResponse
from .forms import LocationForm
from django.contrib.auth.decorators import user_passes_test
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group

# Create your views here.

def add_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser or instance.is_staff:
            instance.groups.add(Group.objects.get(name='Admin'))
        else:
            instance.groups.add(Group.objects.get(name='External User'))

def is_admin(user):
    return user.is_superuser or user.is_staff

@user_passes_test(is_admin, login_url='/no_access/')
@login_required
def location_list(request):
    locations = Location.objects.filter(is_active=True)
    return render(request, 'register_app/location_list.html', {'locations': locations})

def no_access(request):
    return render(request, 'register_app/no_access.html')

@login_required
def sign_in(request, location_id):
    if request.method == "POST":
        SignInOutRegister.objects.create(user=request.user, location_id=location_id, sign_in_time=timezone.now())
        return redirect('location_list')
    return render(request, 'register_app/login.html')

@login_required
def sign_out(request, register_id):
    if request.method == "POST":
        register_entry = SignInOutRegister.objects.get(id=register_id)
        register_entry.sign_out_time = timezone.now()
        register_entry.save()
        return redirect('location_list')
    return render(request, 'register_app/sign_out.html')

def create_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error'})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('location_list')
    else:
        form = UserCreationForm()
    return render(request, 'register_app/register.html', {'form': form})
