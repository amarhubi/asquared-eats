import os

from neo4j import GraphDatabase, RoutingControl

from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      UniqueIdProperty, RelationshipTo)
from dotenv import load_dotenv
from neomodel import db
from models import Recipe, Ingredient, IngredientToRecipeRelation


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
    # config.DRIVER = driver
    # results, meta = db.cypher_query("RETURN 'Hello World' as message")
    # print(results)
    
    ingredients = [
        { 
            'name' : 'Kalamata olives',
            'relations' : {
                'unit' : 'grams', 
                'quantity' : '200', 
                'description' : 'seeded'
            } 
        },
        { 
            'name' : 'Tomato',
            'relations' : {
                'unit' : '', 
                'quantity' : '1', 
                'description' : 'whole'
            } 
        },
        { 
            'name' : 'Capers',
            'relations' : {
                'unit' : 'table spoon', 
                'quantity' : '1', 
                'description' : ''
            } 
        }
    ]
    salad = Recipe(name='Tomato Pasta Salad').save()
    for i in ingredients:
        print(i)
        name = i.get('name')
        relations = i.get('relations')
        ingredient = Ingredient(name=name).save()
        salad.ingredients.connect(ingredient,
                                {
                                    'quantity' :relations.get('quantity'),
                                    'unit' : relations.get('unit'),
                                    'description' : relations.get('description')
                                    })
    db.close_connection()

    # jim = Person(name='Jim', age=3).save()  # Create
    # jim.age = 4
    # jim.save()  # Update, (with validation)
