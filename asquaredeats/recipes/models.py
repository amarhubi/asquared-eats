from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, StructuredRel, FloatProperty, DateTimeProperty, JSONProperty, RelationshipFrom)
from collections import defaultdict

class IngredientToObjectRelation(StructuredRel):
    quantity = FloatProperty(required=True)
    unit = StringProperty(required=True)
    description = StringProperty(required=False)

class Ingredient(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    recipe = RelationshipTo('Recipe', 'in_recipe', model=IngredientToObjectRelation)
    units = JSONProperty()

    def convert_to_grams(self, unit, amount):      
        return float(self.units.get(unit)) * amount

class Recipe(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    ingredients = RelationshipTo('Ingredient', 'has_ingredient', model=IngredientToObjectRelation)

    def get_absolute_url(self):
        return reverse('recipes:recipe_details', kwargs={"recipe_id" : self.uid })
    
    def get_add_ingredient_url(self):
        return(reverse('recipes:add_ingredient', kwargs={'recipe_id' : self.uid}))

class RecipeToMenuRelation(StructuredRel):
    uid = UniqueIdProperty()

class ShoppingList(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty()
    items = JSONProperty()
    menu = RelationshipFrom('Menu', 'has_shopping_list')

    def get_absolute_url(self):
        return reverse('recipes:shopping_list_details', kwargs={'shopping_list_id' : self.uid})
    
    def get_add_item_url(self):
        return reverse('recipes:add_item_to_shopping_list', kwargs={'shopping_list_id' : self.uid})

class Menu(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    date_created = DateTimeProperty()
    recipes = RelationshipTo(Recipe, 'has_recipe', model=RecipeToMenuRelation)
    
    def get_absolute_url(self):
        # return reverse('recipes:index')
        return reverse('recipes:menu_details', kwargs={"menu_id" : self.uid })
    
    def get_create_shopping_list_url(self):
        return reverse('recipes:create_shopping_list', kwargs={"menu_id" : self.uid})