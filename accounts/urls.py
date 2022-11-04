from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.index, name='index'),
    path("signup/", views.signup, name="signup"),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('edit/', views.edit, name='edit'),
    path('editpw/', views.editpw, name='editpw'),
    path('delete/', views.delete, name='delete'),
    path('block_user/', views.block_user, name='block_user'),
    path('question/',views.question,name='question'),
    path('<str:username>/', views.profile, name='profile'),
    path('<int:pk>/follow/', views.follow, name='follow'),
    path('<int:pk>/block', views.block, name='block'),
    path('<int:pk>/block_user_block', views.block_user_block, name='block_user_block'),
]