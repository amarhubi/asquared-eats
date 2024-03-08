import os
from typing import Any
from neomodel import config, db
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F
from django.shortcuts import render
from dotenv import load_dotenv
from neo4j import GraphDatabase
from .models import Recipe


# def index(request):
#     recipes = Recipe.nodes.all()
#     return HttpResponse(config.DATABASE_URL)

def index(request):
    recipes = Recipe.nodes.all()
    context = { "recipe_list": recipes }
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
    print(ingredient_list)
    
    context = {
        'recipe' : recipe,
        'ingredient_list' : ingredient_list
    }
    return render(request, "recipes/recipe_details.html", context)

# class IndexView(generic.ListView):
#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Recipe.nodes.all