import os

from neo4j import GraphDatabase, RoutingControl

from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      UniqueIdProperty, RelationshipTo)
from dotenv import load_dotenv
from neomodel import db
from models import Menu, Recipe, Ingredient, IngredientToObjectRelation
from datetime import datetime
from helpers.utils import connect_ingredient_list_to_recipe, connect_ingredient_to_recipe, create_ingredient


# def add_friend(driver, name, friend_name):
#     driver.execute_query(
#         "MERGE (a:Person {name: $name}) "
#         "MERGE (friend:Person {name: $friend_name}) "
#         "MERGE (a)-[:KNOWS]->(friend)",
#         name=name, friend_name=friend_name, database_="neo4j",
#     )


# def print_friends(driver, name):
#     records, _, _ = driver.execute_query(
#         "MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
#         "RETURN friend.name ORDER BY friend.name",
#         name=name, database_="neo4j", routing_=RoutingControl.READ,
#     )
#     for record in records:
#         print(record["friend.name"])

if __name__ == '__main__':
    load_dotenv()

    user = os.environ['NEO4J_USERNAME']
    psw = os.environ['NEO4J_PASSWORD']
    uri = os.environ['NEO4J_URI']

    # with GraphDatabase.driver(uri, auth=(user, psw)) as driver:
    #     add_friend(driver, "Arthur", "Guinevere")
    #     add_friend(driver, "Arthur", "Lancelot")
    #     add_friend(driver, "Arthur", "Merlin")
    #     print_friends(driver, "Arthur")
    #     # config.DATABASE_URL = 'neo4j+s://{}:{}@{}'.format(user, psw, uri)
# 
    load_dotenv()
    NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
    NEO4J_URI = os.getenv('NEO4J_URI')
    url = 'neo4j+s://{}:{}@{}'.format(NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_URI)

    print(f"This is the stuff {NEO4J_URI}")

    # Change the db conenction
    driver = GraphDatabase().driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    db.set_connection(driver=driver)
    [m.delete() for m in Menu.nodes.all()]
    [i.delete() for i in Ingredient.nodes.all()]
    [r.delete() for r in Recipe.nodes.all()]
    # config.DRIVER = driver
    
    ingredients = [
        {
            'name' : 'Kalamata olives',
            'units' : {
                'g' : 1,
            }
        },
        {
            'name' : 'Tomato',
            'units' : {
                'g' : 1,
                'whole' : 100
            }
        },
        {
            'name' : 'Capers',
            'units' : {
                'tablespoon' : 7.5
            }
        },
        {
            'name' : 'Yellow onion',
            'units' : {
                'whole' : 110    
            }
        },
        {
            'name' : 'Ginger',
            'units' : {
                'g' : 1
            }
        },
        {
            'name' : 'Cumin Seeds',
            'units' : {
                'teaspoon' : 2.1
            }
        }
    ]

    salad_ingredients = [
        { 
            'name' : 'Kalamata olives',
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
