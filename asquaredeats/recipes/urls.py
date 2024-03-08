from django.urls import path

from . import views

app_name = "recipes"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:recipe_id>/", views.recipe_details, name="recipe_details")
    # path("", views.IndexView.as_view(), name="index"),
]