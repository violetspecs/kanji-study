from django.urls import path

from . import views

app_name = 'quiz'
urlpatterns = [
    path('', views.index, name='index'),
    path('answer', views.answer, name='answer'),
    path('result', views.result, name='result'),
    path('register', views.register, name='register'),
]