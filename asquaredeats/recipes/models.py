from http.server import HTTPServer
from django.db import models
from django.http import HttpResponseRedirect, HttpResponseServerError
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
    
    def get_add_to_menu_url(self):
        return(reverse('recipes:add_to_menu', kwargs={'recipe_id' : self.uid}))
    
class RecipeToMenuRelation(StructuredRel):
    uid = UniqueIdProperty()
    count = IntegerProperty(default=1)

class ShoppingList(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty()
    items = JSONProperty()
    menu = RelationshipFrom('Menu', 'has_shopping_list')

    def get_absolute_url(self):
        return reverse('recipes:shopping_list_details', kwargs={'shopping_list_id' : self.uid})
    
    def get_add_item_url(self):
        return reverse('recipes:add_item_to_shopping_list', kwargs={'shopping_list_id' : self.uid})
    
    def add_item(self, new_item_name, new_item_amount):
        item_index = next((i for i, item in enumerate(self.items) if item.get('name') == new_item_name), None)
        if item_index is None:
            item = {
                'name' : new_item_name,
                'quantity' : new_item_amount,
                'unit' : 'g'
            }
            self.items.append(item)
            print(f"Item wasn't on the list and added {item}")
            return self
        item = self.items[item_index]
        item_quantity = item.get('quantity')
        item['quantity'] = item_quantity + new_item_amount
        self.items[item_index] = item
        
        return self

class Menu(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    date_created = DateTimeProperty()
    recipes = RelationshipTo(Recipe, 'has_recipe', model=RecipeToMenuRelation)

    # TODO Check if the menu and recipe are already connected. If yes, increment the relation count
    def add_recipe(self, recipe):
        if self.recipes.is_connected(recipe):
            menu_to_recipe_relationship = self.recipes.relationship(recipe)
            menu_to_recipe_relationship.count += 1 
            menu_to_recipe_relationship.save()
            return self
        self.recipes.connect(recipe)
        return self

    def remove_recipe(self, recipe):
        if not self.recipes.is_connected(recipe):
            return HttpResponseServerError("Recipe is not part of the menu")

        menu_to_recipe_relationship = self.recipes.relationship(recipe)

        if menu_to_recipe_relationship.count > 1:
            menu_to_recipe_relationship.count -= 1 
            menu_to_recipe_relationship.save()
            return self

        self.recipes.disconnect(recipe)
        return self

    def get_absolute_url(self):
        # return reverse('recipes:index')
        return reverse('recipes:menu_details', kwargs={"menu_id" : self.uid })
    
    def get_create_shopping_list_url(self):
        return reverse('recipes:create_shopping_list', kwargs={"menu_id" : self.uid})
    
    def get_delete_url(self):
        return reverse('recipes:menu_delete', kwargs={"menu_id" : self.uid})
    
    def get_add_recipe_url(self):
        return reverse('recipes:menu_add_recipe', kwargs={"menu_id": self.uid})

    def get_remove_recipe_url(self):
        return reverse('recipes:menu_remove_recipe', kwargs={"menu_id" : self.uid})