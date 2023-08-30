from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Location, SignInOutRegister
from django.utils import timezone
# Create your views here.


@login_required
def location_list(request):
    locations = Location.objects.all()
    return render(request, 'register_app/location_list.html', {'locations': locations})

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
