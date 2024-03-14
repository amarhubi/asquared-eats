from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, StructuredRel, FloatProperty, DateTimeProperty)
from collections import defaultdict

class Ingredient(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)

class IngredientToObjectRelation(StructuredRel):
    quantity = FloatProperty(required=True)
    unit = StringProperty(required=True)
    description = StringProperty(required=False)

class Recipe(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    ingredients = RelationshipTo(Ingredient, 'has_ingredient', model=IngredientToObjectRelation)

    def get_absolute_url(self):
        # return reverse('recipes:index')
        return reverse('recipes:recipe_details', kwargs={"recipe_id" : self.uid })

class RecipeToMenuRelation(StructuredRel):
    uid = UniqueIdProperty()

class ShoppingList(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty()
    items = RelationshipTo(Ingredient, 'has_item', model=IngredientToObjectRelation)

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
        # shopping_list = ShoppingList(name=self.name).save()
        # recipes = self.recipes.all()
        # items = []
        # print(recipes)
        # quantities = defaultdict(int)
        # units = {}
        # # shopping_list = ShoppingList().save()
        # for r in recipes:
        #     ingredients = r.ingredients.all()
                       
        #     for i in ingredients:
        #         # print(i)
        #         name = i.name
        #         relation = r.ingredients.relationship(i)
        #         quantity = relation.quantity
        #         unit = relation.unit
        #         # print(f'{quantity} {unit} {name}')
        #         quantities[name] += quantity
        #         units[name] = unit
        # print(quantities)
        # print(units)
        # for name, quantity in quantities.items():
        #     shopping_list.items.connect({
        #         'name' : name,
        #         'relation' : {
        #             'unit' : units[name],
        #             'quantitiy' : quantity,
        #             'description' : ''
        #         }
        #     })
        

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