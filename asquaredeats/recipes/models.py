from django.db import models
from django.urls import reverse
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, StructuredRel, FloatProperty, DateTimeProperty)

class Ingredient(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)

class IngredientToRecipeRelation(StructuredRel):
    quantity = FloatProperty(required=True)
    unit = StringProperty(required=True)
    description = StringProperty(required=False)

class Recipe(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    ingredients = RelationshipTo(Ingredient, 'HAS_INGREDIENT', model=IngredientToRecipeRelation)

    def get_absolute_url(self):
        # return reverse('recipes:index')
        return reverse('recipes:recipe_details', kwargs={"recipe_id" : self.uid })

class RecipeToMenuRelation(StructuredRel):
    uid = UniqueIdProperty()

class Menu(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    date_created = DateTimeProperty()
    recipes = RelationshipTo(Recipe, 'has_recipe', model=RecipeToMenuRelation)
    
    def get_absolute_url(self):
        # return reverse('recipes:index')
        return reverse('recipes:menu_details', kwargs={"menu_id" : self.uid })

# class Country(StructuredNode):
#     code = StringProperty(unique_index=True, required=True)

# class City(StructuredNode):
#     name = StringProperty(required=True)
#     country = RelationshipTo(Country, 'FROM_COUNTRY')

# class Person(StructuredNode):
#     uid = UniqueIdProperty()
#     name = StringProperty(unique_index=True)
#     age = IntegerProperty(index=True, default=0)

#     # traverse outgoing IS_FROM relations, inflate to Country objects
#     country = RelationshipTo(Country, 'IS_FROM')

#     # traverse outgoing LIVES_IN relations, inflate to City objects
#     city = RelationshipTo(City, 'LIVES_IN')