from collections import defaultdict
import os

from django import db
from dotenv import load_dotenv
from neo4j import GraphDatabase
from neomodel import config
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
def create_dummy_data ():
    load_dotenv()
    NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
    NEO4J_URI = os.getenv('NEO4J_URI')
    # url = 'neo4j+s://{}:{}@{}'.format(NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_URI)
  
    # # Change the db conenction
    driver = GraphDatabase().driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    db.set_connection(driver=driver)
    [m.delete() for m in MenuView.nodes.all()]
    [i.delete() for i in Ingredient.nodes.all()]
    [r.delete() for r in Recipe.nodes.all()]

    config.DRIVER = driver

    ingredients = []
    with open('data\ingredients.csv', newline='') as ingredients_csv:
        reader = csv.reader(ingredients_csv)
        next(reader, None)
        for row in reader:
            ingredient = {}
            units = {}
            name = row.pop(0)
            
            while row:
                unit = row.pop(0)
                conversion = float(row.pop(0))
                units[unit] = conversion
            ingredient['name'] = name
            ingredient['units'] = units
            ingredients.append(ingredient)

    salad_ingredients = [
        { 
            'name' : 'Kalamata Olives',
            'relations' : {
                'unit' : 'g', 
                'quantity' : '200', 
                'description' : 'seeded'
            } 
        },
        { 
            'name' : 'Tomato',
            'relations' : {
                'unit' : 'whole', 
                'quantity' : '1', 
                'description' : ''
            } 
        },
        { 
            'name' : 'Capers',
            'relations' : {
                'unit' : 'tablespoon', 
                'quantity' : '1', 
                'description' : ''
            } 
        }
    ]

    dal_ingredients = [
        { 
            'name' : 'Yellow onion',
            'relations' : {
                'unit' : 'whole', 
                'quantity' : '5', 
                'description' : 'sliced'
            } 
        },
        { 
            'name' : 'Ginger',
            'relations' : {
                'unit' : 'g', 
                'quantity' : '50', 
                'description' : 'grated'
            } 
        },
        { 
            'name' : 'Cumin Seeds',
            'relations' : {
                'unit' : 'tablespoon', 
                'quantity' : '1', 
                'description' : ' toasted'
            } 
        }
    ]

    salad = Recipe(name='Tomato Pasta Salad').save()
    dal = Recipe(name='Dal').save()
    for i in ingredients:
        create_ingredient(i)
    connect_ingredient_list_to_recipe(dal, dal_ingredients)
    connect_ingredient_list_to_recipe(salad, salad_ingredients)

    dal_tomato_relation = {
        'name' : 'Tomato',
        'relations': {
            'quantity' : 1,
            'unit' : 'whole',
            'description' : 'diced'
        }
    }
    connect_ingredient_to_recipe(dal, dal_tomato_relation)

    menu = MenuView(name='Feet don\'t fail me now', date_created=datetime.now()).save()
    menu.recipes.connect(dal)
    menu.recipes.connect(salad)

    db.close_connection()
