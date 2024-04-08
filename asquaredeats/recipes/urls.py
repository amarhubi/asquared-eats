from django.urls import path

from . import views
from .views import MenuView

app_name = "recipes"
urlpatterns = [
    path("", views.index, name="index"),
    path("recipes/<str:recipe_id>/", views.recipe_details, name="recipe_details"),
    path("recipes/", views.recipes_list, name="recipes_list"),
    path("recipes/<str:recipe_id>/new-ingredient", views.add_ingredient_to_recipe, name="add_ingredient_to_recipe"),
    path("recipes/<str:recipe_id>/add-to-menu", views.add_to_menu, name="add_to_menu"),
    # Menu URLs
    path("menus/", MenuView.as_view(), name="menus"),
    path("menus/<str:menu_id>/", views.menu_details, name="menu_details"),
    path("menus/<str:menu_id>/delete", views.menu_delete, name="menu_delete"),
    path("menus/<str:menu_id>/create-shopping-list", views.create_shopping_list, name="create_shopping_list"),
    path("menus/<str:menu_id>/add-recipe", views.menu_add_recipe, name="menu_add_recipe"), 
    path("menus/<str:menu_id>/remove-recipe", views.menu_remove_recipe, name="menu_remove_recipe"),

    # Shopping list URLs
    path("shopping_lists/<str:shopping_list_id>", views.shopping_list_details, name="shopping_list_details"),
    path("shopping_lists/<str:shopping_list_id>/add-item", views.add_item_to_shopping_list, name="add_item_to_shopping_list"),
    path("shopping_lists/", views.shopping_lists, name="shopping_lists")
    #  path("", views.IndexView.as_view(), name="index"),
]