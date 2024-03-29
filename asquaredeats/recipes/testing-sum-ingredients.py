import os

from neo4j import GraphDatabase, RoutingControl

from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      UniqueIdProperty, RelationshipTo)
from dotenv import load_dotenv
from neomodel import db
from models import Menu, Recipe, Ingredient, IngredientToObjectRelation
from datetime import datetime
from asquaredeats.recipes import utils


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

    # Change the db conenction
    driver = GraphDatabase().driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    db.set_connection(driver=driver)

    menu = Menu.nodes.get_or_none(name='Feet don\'t fail me now')

    if menu is not None:
        # recipes = menu.recipes.all()
        # all_ingredients = []
        # for r in recipes:
        #     [all_ingredients.append((i, r)) for i in r.ingredients]
        print(utils.sum_ingredients(menu))
    else:
        print(f"Menu does not exist")

    db.close_connection()
    
    # jim = Person(name='Jim', age=3).save()  # Create
    # jim.age = 4
    # jim.save()  # Update, (with validation)
