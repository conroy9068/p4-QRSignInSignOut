from django.urls import path
from . import views 

urlpatterns = [
    path('locations/', views.location_list, name='location_list'),
    # path('sign_in/<int:location_id>/', views.sign_in, name='sign_in'),
    # path('sign_out/<int:register_id>/', views.sign_out, name='sign_out'),
    # path('sign_in/<int:location_id>/', views.sign_in_out_view, name='sign_in_out'),
    path('create_location/', views.create_location, name='create_location'),
    path('no_access/', views.no_access, name='no_access'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('view_qr_code/<int:location_id>/', views.view_qr_code, name='view_qr_code'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

]
