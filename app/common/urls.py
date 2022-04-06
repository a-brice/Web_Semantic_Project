
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('school', views.get_school, name='school'),
    path('school/<entry>', views.get_school, name='school'),
    path('person/<type>', views.get_person, name='person'),
]
