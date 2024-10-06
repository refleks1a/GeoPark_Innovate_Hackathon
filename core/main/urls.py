from django.urls import path
from .views import contact, home


app_name = 'main'

urlpatterns = [
    path("contact/", contact, name="contact"),
    path("", home, name="home")
]
