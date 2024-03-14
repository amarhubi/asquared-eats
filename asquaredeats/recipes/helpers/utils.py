from models import Menu, Recipe, Ingredient, IngredientToObjectRelation


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
    return recipe
