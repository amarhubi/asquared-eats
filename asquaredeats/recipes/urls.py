from django.urls import path

from . import views

app_name = "recipes"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:recipe_id>/", views.recipe_details, name="recipe_details"),
    path("menus/<str:menu_id>/", views.menu_details, name="menu_details"),
    path("menus/<str:menu_id>/create_shopping_list", views.create_shopping_list, name="create_shopping_list"),
    path("shopping_lists/<str:shopping_list_id>", views.shopping_list_details, name="shopping_list_details")
    #  path("", views.IndexView.as_view(), name="index"),
]