from collections import defaultdict
from ..models import Menu, Recipe, Ingredient, IngredientToObjectRelation


def create_ingredients_and_connect_to_recipe(recipe, ingredient_list):
    for i in ingredient_list:
        name = i.get('name')
        relations = i.get('relations')
        print(f"{name} {relations}")
        ingredient = Ingredient(name=name).save()
        connect_ingredient_to_recipe(recipe, ingredient, relations)
    return recipe 

def connect_ingredient_to_recipe(recipe, ingredient, relation):
    # Format of relation dict
    # {
    #     'quantity' : 1,
    #     'unit' : 'whole',
    #     'description' : 'diced'
    # }
    recipe.ingredients.connect(ingredient, relation)
    ingredient.recipe.connect(recipe, relation)
    return recipe

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