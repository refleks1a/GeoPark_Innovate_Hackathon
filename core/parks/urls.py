from django.urls import path
from .views import like, delete_like, favorites, create_post_comment


app_name = 'parks'

urlpatterns = [
    path("<int:pk>/like/", like, name = "like"),
    path("<int:pk>/like/delete", delete_like, name = "delete-like"),

    path("<int:pk>/comment/", create_post_comment, name = "comment"),

    path("favorites/", favorites, name="favorites"),
]
