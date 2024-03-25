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
        for i in r.ingredients:
            menu_ingredients.append((i, r))
    summed_ingredients = []
    quantities = defaultdict(int)
    units = {}

    for i, r in menu_ingredients:
        # print(f"{r} {i}")
        ingredient_name = i.name
        relation = i.recipe.relationship(r)
        quantity = relation.quantity
        unit = relation.unit
        amount_in_grams = i.convert_to_grams(unit, quantity)
        # print(f"{ingredient_name} {quantity} {unit} {amount_in_grams}")
        quantities[ingredient_name] += amount_in_grams
        

    for ingredient_name, quantity in quantities.items():
        summed_ingredients.append({
            'name' : ingredient_name,
            'quantity' : quantity,
            'unit' : 'g'
        })
        
    return summed_ingredients

