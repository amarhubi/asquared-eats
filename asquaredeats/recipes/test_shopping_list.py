from re import M
from django.test import TestCase
from .models import ShoppingList
from copy import deepcopy

def is_greater_by_amount(value1, value2, amount):
    """Checks if value1 is greater than value2 by the specified amount."""
    difference = value1 - value2
    return difference == amount

class ShoppingListModelTests(TestCase):
    def test_add_item_with_already_existing_item(self):
        """
        Adding an item that is already on the shopping list should update the item
        and should not append a new item to the list
        """
        starting_items = [{
            'name' : 'Tomato',
            'quantity' : 100,
            'unit' : 'g'
        }]
        new_item = {
            'name' : 'Tomato',
            'quantity' : 10,
            'unit' : 'g'
        }
        shopping_list = ShoppingList(items=starting_items).save()
        items_before = deepcopy(shopping_list.items)
        
        shopping_list.add_item(new_item.get('name'), new_item.get('quantity')).save()
        items_after = shopping_list.items
        self.assertEqual(len(items_before), len(items_after))

    def test_add_item_with_already_existing_item_correctly_increments(self):
        """
        Shopping list item amount should increment when given an item
        that is already on the list
        """
        starting_items = [{
            'name' : 'Tomato',
            'quantity' : 100,
            'unit' : 'g'
        }]
        new_item = {
            'name' : 'Tomato',
            'quantity' : 10,
            'unit' : 'g'
        }
        shopping_list = ShoppingList(items=starting_items).save()
        items_before = deepcopy(shopping_list.items)
        
        shopping_list.add_item(new_item.get('name'), new_item.get('quantity')).save()
        items_after = shopping_list.items
        
        shopping_list_item_quantity = items_after[0].get('quantity')

        starting_item_quantity = items_before[0].get('quantity')
        new_item_quantity = new_item.get('quantity')

        self.assertTrue(is_greater_by_amount(shopping_list_item_quantity, starting_item_quantity, new_item_quantity))
