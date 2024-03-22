import os, csv, sys
from os import path
sys.path.append( f"{path.dirname(path.abspath(__file__))}\helpers" )

from neo4j import GraphDatabase, RoutingControl
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      UniqueIdProperty, RelationshipTo)
from dotenv import load_dotenv
from neomodel import db
from models import Menu, Recipe, Ingredient, IngredientToObjectRelation
from datetime import datetime
from helpers.utils import connect_ingredient_list_to_recipe, connect_ingredient_to_recipe, create_ingredient

if __name__ == '__main__':
    load_dotenv()

    user = os.environ['NEO4J_USERNAME']
    psw = os.environ['NEO4J_PASSWORD']
    uri = os.environ['NEO4J_URI']
 
    load_dotenv()
    NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
    NEO4J_URI = os.getenv('NEO4J_URI')
    url = 'neo4j+s://{}:{}@{}'.format(NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_URI)

    # # Change the db conenction
    driver = GraphDatabase().driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    db.set_connection(driver=driver)
    [m.delete() for m in Menu.nodes.all()]
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
                conversion = row.pop(0)
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

    menu = Menu(name='Feet don\'t fail me now', date_created=datetime.now()).save()
    menu.recipes.connect(dal)
    menu.recipes.connect(salad)

    db.close_connection()
