from typing import Any
from wsgiref.util import shift_path_info
from django.urls import reverse
from django.views import View
from neomodel import config, db
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from django.contrib import messages
from .models import Recipe, Menu, ShoppingList, Ingredient
from .helpers.utils import sum_ingredients

def index(request):
    recipes = Recipe.nodes.all()
    menus = Menu.nodes.all()
    shopping_lists = ShoppingList.nodes.all()
    context = { 
        "recipe_list": recipes,
        "menu_list" : menus,
        "shopping_lists" : shopping_lists
        }
    return render(request, "recipes/index.html", context)

# Recipe views
def recipe_details(request, recipe_id):
    recipe = Recipe.nodes.get_or_none(uid=recipe_id)

    if recipe is None:
        raise Http404
    
    menu_list = Menu.nodes.all()
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
        'ingredient_list' : ingredient_list,
        'menu_list' : menu_list
    }

    return render(request, "recipes/recipe_details.html", context)

def add_to_menu(request, recipe_id):
    recipe = Recipe.nodes.get_or_none(uid=recipe_id)
    menu_id = request.POST.get('menus')

    menu = Menu.nodes.get_or_none(uid=menu_id)
    if recipe is None:
        messages.error(request, "Recipe does not exist")
        return  HttpResponseRedirect(reverse('recipes:recipe_details', kwargs={"recipe_id" : recipe.uid }))
    
    if menu is None:
        messages.error(request, "Menu does not exist")
        return  HttpResponseRedirect(reverse('recipes:recipe_details', kwargs={"recipe_id" : recipe.uid }))
    print(request.POST)
    menu.recipes.connect(recipe)
    messages.info(request, f"{recipe.name} added to menu")
    return  HttpResponseRedirect(reverse('recipes:recipe_details', kwargs={"recipe_id" : recipe.uid }))

def add_ingredient_to_recipe(request, recipe_id):
    recipe = Recipe.nodes.get_or_none(uid=recipe_id)
    ingredients = Ingredient.nodes.all()

    if recipe is None:
        raise Http404

    context = {
        'recipe' : recipe,
        'ingredients' : ingredients
    }

    return render(request, "recipes/add_ingredient_to_recipe.html", context)

def recipes_list(request):
    recipes = Recipe.nodes.all()

    context = {
        'recipes' : recipes,
    }
    return render(request, "recipes/recipe_list.html")
#Menu views
def menu_list(request):
    menus = Menu.nodes.all()
    context = {
        'menus' : menus
    }
    return render(request, "recipes/menu_list.html", context)

class MenuView(View):
    def get(self, request):
        menus = Menu.nodes.all()
        context = {
            'menus' : menus
        }
        return render(request, "recipes/menu_list.html", context)
   
    def post(self, request):
        print(request.POST)
        menu_name = request.POST.get('menu-name')
        menu = Menu(name=menu_name).save()
        return HttpResponseRedirect(reverse('recipes:menu_details', kwargs={'menu_id' : menu.uid}))
    #
def delete_menu(request, menu_id):
    menu = Menu.nodes.get_or_none(uid=menu_id)

    if menu is None:
        raise Http404('Menu does not exit')
    
    if menu.delete():
        return HttpResponseRedirect(reverse('recipes:menus'))
    return HttpResponseServerError

def menu_details(request, menu_id):
    menu = Menu.nodes.get_or_none(uid=menu_id)

    if menu is None:
        raise Http404
    
    context = {
        'menu' : menu,
        'recipe_list' : menu.recipes.all()
    }

    return render(request, "recipes/menu_details.html", context)
def shopping_lists(request):
    shopping_lists = ShoppingList.nodes.all()
    context = {
        'shopping_lists' : shopping_lists
    }
    return render(request, 'recipes/shopping_lists.html', context )
    
def create_shopping_list(request, menu_id):
    menu = Menu.nodes.get_or_none(uid=menu_id)
    
    if menu is not None:
        name = menu.name
        items = sum_ingredients(menu)
        shopping_list = ShoppingList(name=name, items=items).save()
        shopping_list.menu.connect(menu)
    return HttpResponseRedirect(reverse('recipes:shopping_list_details', kwargs={"shopping_list_id" : shopping_list.uid }))

def shopping_list_details(request, shopping_list_id):  
    shopping_list = ShoppingList.nodes.get_or_none(uid=shopping_list_id)
    all_ingredients = Ingredient.nodes.all()
    ingredients = []
    for i in all_ingredients:
        ingredients.append((i.name, i.units.keys()))

    if shopping_list is None:
        raise Http404
    
    context = {
        'shopping_list' : shopping_list,
        'ingredients' : ingredients,
    }
    return render(request, "recipes/shopping_list_details.html", context)

def add_item_to_shopping_list(request, shopping_list_id):
    shopping_list = ShoppingList.nodes.get_or_none(uid=shopping_list_id)
    
    if shopping_list is None:
        raise Http404('Shopping list does not exist')
    
    print(request.POST)
    new_item_name = request.POST.get('ingredients')
    try:
        new_item_amount = float(request.POST.get('amount'))
        ingredient_node = Ingredient.nodes.get_or_none(name=new_item_name)
    except ValueError:
        messages.error(request, 'Amount must be a float')
        return HttpResponseRedirect(reverse('recipes:shopping_list_details', kwargs={"shopping_list_id" : shopping_list_id})) 
    if ingredient_node is None:
        messages.error(request, 'Item does not exist')

        return HttpResponseRedirect(reverse('recipes:shopping_list_details', kwargs={"shopping_list_id" : shopping_list_id}))

    shopping_list.add_item(new_item_name, new_item_amount).save()
    
    #     next(ingredient for ingredients)
    messages.info(request, "Item added to shopping list ")
    return HttpResponseRedirect(reverse('recipes:shopping_list_details', kwargs={"shopping_list_id" : shopping_list_id}))

def add_ingredient_to_recipe(request, recipe_id):
    print(request)
    return HttpResponseRedirect(reverse('recipes:recipe_details', kwargs={"recipe_id" : recipe_id }))


# class IndexView(generic.ListView):
#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Recipe.nodes.all