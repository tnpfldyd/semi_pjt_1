from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('index/', views.index, name="index"),
    path('create/', views.create, name='create'),
    path('<int:products_pk>/', views.detail, name="detail"),
    path('<int:products_pk>/update/', views.update, name="update"),
    path('<int:products_pk>/delete/', views.delete, name="delete"),
    # location
    path('location/',  views.location, name="location"),
]