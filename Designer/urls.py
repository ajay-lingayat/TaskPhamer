from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home-page'),
    path('contact', views.contact, name='contact'),
    path('add-data', views.add_data, name='add-data'),
    path('delete-data-<int:data_index>', views.delete_data, name='delete-data'),
    path('edit-data', views.edit_data, name='edit-data'),
    path('generate-pdf', views.generate_pdf, name='generate-pdf'),
    path('about', views.about, name="about"),
]