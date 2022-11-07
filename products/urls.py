from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name='create'),
    path('<int:products_pk>/', views.detail, name="detail"),
    path('<int:products_pk>/update/', views.update, name="update"),
    path('<int:products_pk>/delete/', views.delete, name="delete"),
    path('<int:products_pk>/zzim', views.zzi, name='zzi'),
    path('<int:products_pk>/sold_out/', views.sold_out, name='sold_out'),
    path('search/', views.search, name='search'),
]