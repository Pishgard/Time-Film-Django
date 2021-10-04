from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('', views.EditProfileView.as_view(), name='edit_profile'),
    path('profile/<user_id>', views.ProfileAPI.as_view())
]