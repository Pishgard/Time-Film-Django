from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostView.as_view(), name="products"),
    path('<id>', views.PostDetailView.as_view(), name='products_detail'),
    path('create/', views.PostCreateView.as_view(), name="create_products"),
    path('search/', views.SearchData.as_view(), name="search_data"),
]