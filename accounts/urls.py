from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.userlist, name='userlist'),
    path('<int:id>/', views.userpage, name="userpage"),
    path('<int:id>/follow/', views.follow, name='follow'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]
