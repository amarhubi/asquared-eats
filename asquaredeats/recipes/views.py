from typing import Any
from neomodel import config, db
from django.shortcuts import render
from django.http import Http404
# from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F
from django.shortcuts import render
from .models import Recipe, Menu


# def index(request):
#     recipes = Recipe.nodes.all()
#     return HttpResponse(config.DATABASE_URL)

def index(request):
    recipes = Recipe.nodes.all()
    menus = Menu.nodes.all()
    context = { 
        "recipe_list": recipes,
         "menu_list" : menus
         }
    return render(request, "recipes/index.html", context)

def recipe_details(request, recipe_id):
    recipe = Recipe.nodes.get_or_none(uid=recipe_id)

    if recipe is None:
        raise Http404
    
    ingredient_list = []

    for ingredient in recipe.ingredients.all():
        relation = recipe.ingredients.relationship(ingredient)
        ingredient_list.append({
            'name' : ingredient.name,
            'quantity' : relation.quantity,
            'unit' : relation.unit
        })
   
    context = {
        'recipe' : recipe,
        'ingredient_list' : ingredient_list
    }

    return render(request, "recipes/recipe_details.html", context)

def menu_details(request, menu_id):
    menu = Menu.nodes.get_or_none(uid=menu_id)

    if menu is None:
        raise Http404
    
    context = {
        'menu' : menu,
        'recipe_list' : menu.recipes.all()
    }

    return render(request, "recipes/menu_details.html", context)

# class IndexView(generic.ListView):
#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Recipe.nodes.all