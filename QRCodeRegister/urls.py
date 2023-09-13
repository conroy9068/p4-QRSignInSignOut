"""QRCodeRegister URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from register_app import views as register_views
from django.conf import settings
from django.urls import include, path  # For django versions from 2.0 and up
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),

    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='register_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='register_app/logout.html'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='passwordChangeForm'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='passwordChangeDone'),
    path('register/', register_views.register, name='register'),
    path('', include('register_app.urls')), 
    path('dashboard/', register_views.user_dashboard, name='user_dashboard'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
