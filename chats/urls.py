from django.urls import path
from . import views

app_name = 'chats'

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/send/", views.send, name="send"),
    path("test/", views.test, name="test"),
    path("<int:room_pk>/", views.detail, name="detail"),
    path("<int:pk>/first_send/", views.first_send, name="first_send"),
]