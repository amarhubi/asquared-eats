from collections import defaultdict
from ..models import Menu, Recipe, Ingredient, IngredientToObjectRelation


def connect_ingredient_list_to_recipe(recipe, ingredient_list):
    for ingredient in ingredient_list:
        connect_ingredient_to_recipe(recipe, ingredient)
    return recipe 

def connect_ingredient_to_recipe(recipe, ingredient):
    # Format of relation dict
    # {
    #     'quantity' : 1,
    #     'unit' : 'whole',
    #     'description' : 'diced'
    # }

    name = ingredient.get('name')
    relation = ingredient.get('relations')
    # print(f"{name} {relation}")
    # print(ingredient)
    ingredient = Ingredient.nodes.get(name=name)
    recipe.ingredients.connect(ingredient, relation)
    ingredient.recipe.connect(recipe, relation)
    return recipe

def create_ingredient(i):
    name = i.get('name')
    units = i.get('units')
    ingredient = Ingredient(name=name, units=units).save()
    
    return ingredient

def sum_ingredients(menu):
    recipes = menu.recipes.all()
    menu_ingredients = []
    for r in recipes:
        [menu_ingredients.append((i, r)) for i in r.ingredients]
    summed_ingredients = []
    quantities = defaultdict(int)
    units = {}

    for i, r in menu_ingredients:
        name = i.name
        relation = i.recipe.relationship(r)
        quantity = relation.quantity
        unit = relation.unit

        quantities[name] += quantity
        units[name] = unit

    for name, quantity in quantities.items():
        summed_ingredients.append({
            'name' : name,
            'quantity' : quantity,
            'unit' : units[name]
        })
        
    return summed_ingredients