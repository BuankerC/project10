from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.detail, name='detail'),
    path('<int:id>/reviews', views.review, name='review'),
    path('<int:id>/reviews/<int:review_id>/delete',
         views.review_delete, name='review_delete'),
    path('<int:id>/like/', views.like, name="like"),



]
