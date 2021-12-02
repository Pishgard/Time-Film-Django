from django.urls import path
from . import views

app_name = 'movie'

urlpatterns = [
    path('', views.MovieView.as_view(), name="movies"),
    path('<id>', views.MovieDetailView.as_view(), name='movies_detail'),
    path('create/', views.MovieCreateView.as_view(), name="movies_create"),
    path('search/', views.SearchData.as_view(), name="search_data"),
]