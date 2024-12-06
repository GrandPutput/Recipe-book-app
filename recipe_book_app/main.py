from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens import MainMenuScreen, NewRecipeScreen, RecipeBookScreen, FoodMenuScreen, ShoppingCartScreen
import json
import os

class RecipeBookApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(NewRecipeScreen(name='new_recipe'))
        sm.add_widget(RecipeBookScreen(name='recipe_book'))
        sm.add_widget(FoodMenuScreen(name='food_menu'))
        sm.add_widget(ShoppingCartScreen(name='shopping_cart'))

        # Initialize the data structures
        sm.recipe_book = self.load_data('data/recipes.json')
        sm.food_menu = self.load_data('data/food_menu.json')
        sm.shopping_cart = self.load_data('data/shopping_cart.json')

        return sm

    def load_data(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return json.load(file)
        return []

    def save_data(self, filename, data):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def on_stop(self):
        self.save_data('data/recipes.json', self.root.recipe_book)
        self.save_data('data/food_menu.json', self.root.food_menu)
        self.save_data('data/shopping_cart.json', self.root.shopping_cart)

if __name__ == '__main__':
    RecipeBookApp().run()
