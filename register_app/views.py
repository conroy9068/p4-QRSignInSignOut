from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Location, SignInOutRegister
from django.utils import timezone
from django.http import JsonResponse
from .forms import LocationForm
from django.contrib.auth.decorators import user_passes_test
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import UserUpdateForm
import qrcode
from django.dispatch import receiver
from django.http import HttpResponse



# Create your views here.

def add_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser or instance.is_staff:
            instance.groups.add(Group.objects.get(name='Admin'))
        else:
            instance.groups.add(Group.objects.get(name='External User'))

def is_admin(user):
    return user.is_superuser or user.is_staff

post_save.connect(add_to_group, sender=User)

@user_passes_test(is_admin, login_url='/no_access/')
@login_required
def location_list(request):
    locations = Location.objects.filter(is_active=True)
    return render(request, 'register_app/location_list.html', {'locations': locations})

def no_access(request):
    return render(request, 'register_app/no_access.html')


# Sign in and sign out views
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


# User dashboard and profile views
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
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = UserUpdateForm(instance=request.user)
        
    return render(request, 'register_app/edit_profile.html', {'form': form})


# Location views
@login_required
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

# QR code generation
@receiver(post_save, sender=Location)
def generate_qr_code(sender, instance, created, **kwargs):
    if created:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        url = f"http://127.0.0.0/sign_in/{instance.id}/"
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img_path = f"qr_codes/{instance.id}.png"
        img.save(img_path)
        instance.qr_code = img_path
        instance.save()


def generate_qr_code(request, location_id):
    location = Location.objects.get(id=location_id)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    url = f"http://127.0.0.0/sign_in/{location.id}/"
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

