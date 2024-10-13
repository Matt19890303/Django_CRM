from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),

    # have an integer as a private key
    path('record/<int:pk>/', views.customer_record, name='record'),
    path('delete_record/<int:pk>/', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>/', views.update_record, name='update_record'),

    path('staff_members ', views.staff_members, name='staff_members'),
    path('add_owner/', views.add_owner, name='add_owner'),
    path('user/<int:user_id>/', views.owner_record, name='owner_record'),
    path('update_owner/<int:user_id>/', views.update_owner, name='update_owner'),
]
