from django.urls import path
from . import views 

urlpatterns = [
    path('locations/', views.location_list, name='location_list'),
    path('sign_in/<int:location_id>/', views.sign_in, name='sign_in'),
    path('sign_out/<int:register_id>/', views.sign_out, name='sign_out'),
    path('create_location/', views.create_location, name='create_location'),

]
