
from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('school', views.get_school, name='school'),
    path('school/search', views.get_school, name='search_school'),
    path('person/<type>', views.get_person, name='person'),
]
