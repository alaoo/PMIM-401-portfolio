from django.urls import path
from . import views

app_name = 'waitlist'

urlpatterns = [
    path("", views.home, name='home'),
    path("table/", views.table, name='table'),
    path("contact/", views.contact, name='contact'),
    path("doctors/", views.doctors, name='doctors')
]
