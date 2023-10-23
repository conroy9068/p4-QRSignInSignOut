from django.urls import path
from . import views 

urlpatterns = [
    # path('create_location/', views.location_form, name='location_list'),
    # path('sign_in/<int:location_id>/', views.sign_in, name='sign_in'),
    # path('sign_out/<int:register_id>/', views.sign_out, name='sign_out'),
    # path('sign_in/<int:location_id>/', views.sign_in_out_view, name='sign_in_out'),
    path('create_project/', views.create_project, name='create_project'),
    path('create_location/', views.location_form, name='create_location'),
    path('no_access/', views.no_access, name='no_access'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('view_qr_code/<int:location_id>/', views.view_qr_code, name='view_qr_code'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('select_location/', views.select_location_view, name='select_location'),
    path('select_project/', views.select_project_view, name='select_project'),
    path('get_locations/', views.GetLocationsView.as_view(), name='get_locations'),
    path('register/', views.register, name='register'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),


]
