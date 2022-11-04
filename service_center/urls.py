from django.urls import path
from . import views

app_name="service_center"

urlpatterns = [
    path('index/', views.index, name="index"),
    path('question/', views.question, name="question"),
    path('<int:service_pk>/', views.detail, name="detail"),
    path('<int:service_pk>/comments/',views.comment_create, name="comment_create"),
]
