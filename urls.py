from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('registration/',views.registration,name='registration'),
    path('userdetails/',views.userdetails,name='userdetails'),
    path('goal/',views.goal,name='goal'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('trainerdashboard/',views.trainerdashboard,name='trainerdashboard'),
    path('trainerdashboard2/',views.trainerdashboard2,name='trainerdashboard2'),
    path('trainerdashboard3/',views.trainerdashboard3,name='trainerdashboard3'),

]
