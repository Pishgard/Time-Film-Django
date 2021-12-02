from django.urls import path
from . import views

app_name = 'actors'

urlpatterns = [
    path('', views.ActorsView.as_view(), name="actors"),
    path('<id>', views.ActorsDetailView.as_view(), name='actors_detail'),
    path('create/', views.ActorsCreateView.as_view(), name="actors_create"),
    path('search/', views.SearchData.as_view(), name="search_data"),
]