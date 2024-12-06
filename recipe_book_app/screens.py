from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        new_recipe_button = Button(text='New Recipe')
        new_recipe_button.bind(on_press=self.go_to_new_recipe)
        recipe_book_button = Button(text='Recipe Book')
        recipe_book_button.bind(on_press=self.go_to_recipe_book)
        food_menu_button = Button(text='Food Menu')
        food_menu_button.bind(on_press=self.go_to_food_menu)
        shopping_cart_button = Button(text='Shopping Cart')
        shopping_cart_button.bind(on_press=self.go_to_shopping_cart)
        layout.add_widget(new_recipe_button)
        layout.add_widget(recipe_book_button)
        layout.add_widget(food_menu_button)
        layout.add_widget(shopping_cart_button)
        self.add_widget(layout)

    def go_to_new_recipe(self, instance):
        self.manager.current = 'new_recipe'

    def go_to_recipe_book(self, instance):
        self.manager.current = 'recipe_book'

    def go_to_food_menu(self, instance):
        self.manager.current = 'food_menu'

    def go_to_shopping_cart(self, instance):
        self.manager.current = 'shopping_cart'

class NewRecipeScreen(Screen):
    def __init__(self, **kwargs):
        super(NewRecipeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        self.recipe_name_input = TextInput(hint_text='Recipe Name')
        
        description_layout = BoxLayout(size_hint_y=None, height=40)
        self.description_input = TextInput(hint_text='Add Recipe Step')
        save_description_button = Button(text='Add', size_hint_x=None, width=80)
        save_description_button.bind(on_press=self.add_description)
        description_layout.add_widget(self.description_input)
        description_layout.add_widget(save_description_button)
        
        self.description_list = GridLayout(cols=1, size_hint_y=None)
        self.description_list.bind(minimum_height=self.description_list.setter('height'))
        description_scroll = ScrollView(size_hint=(1, None), size=(400, 200))
        description_scroll.add_widget(self.description_list)

        ingredient_layout = BoxLayout(size_hint_y=None, height=40)
        self.ingredient_input = TextInput(hint_text='Add Ingredient')
        save_ingredient_button = Button(text='Add', size_hint_x=None, width=80)
        save_ingredient_button.bind(on_press=self.add_ingredient)
        ingredient_layout.add_widget(self.ingredient_input)
        ingredient_layout.add_widget(save_ingredient_button)
        
        self.ingredients_list = GridLayout(cols=1, size_hint_y=None)
        self.ingredients_list.bind(minimum_height=self.ingredients_list.setter('height'))
        ingredients_scroll = ScrollView(size_hint=(1, None), size=(400, 200))
        ingredients_scroll.add_widget(self.ingredients_list)
        
        save_button = Button(text='Save Recipe')
        save_button.bind(on_press=self.save_recipe)
        main_menu_button = Button(text='Main Menu')
        main_menu_button.bind(on_press=self.go_to_main_menu)
        
        layout.add_widget(self.recipe_name_input)
        layout.add_widget(description_layout)
        layout.add_widget(description_scroll)
        layout.add_widget(ingredient_layout)
        layout.add_widget(ingredients_scroll)
        layout.add_widget(save_button)
        layout.add_widget(main_menu_button)
        self.add_widget(layout)

        self.description = []
        self.ingredients = []
        self.step_number = 1  # Initialize step number

    def add_description(self, instance):
        description = self.description_input.text.strip()
        if description:
            self.description.append(f"Step {self.step_number}: {description}")
            description_label = BoxLayout(size_hint_y=None, height=40)
            description_text = Label(text=self.description[-1])
            remove_button = Button(text='Remove', size_hint_x=None, width=80)
            remove_button.bind(on_press=lambda x: self.remove_description(description_label, description))
            description_label.add_widget(description_text)
            description_label.add_widget(remove_button)
            self.description_list.add_widget(description_label)
            self.description_input.text = ''
            self.step_number += 1  # Increment step number

    def remove_description(self, description_layout, description):
        if description in self.description:
            self.description.remove(description)
            self.description_list.remove_widget(description_layout)

    def add_ingredient(self, instance):
        ingredient = self.ingredient_input.text.strip()
        if ingredient:
            self.ingredients.append(ingredient)
            ingredient_label = BoxLayout(size_hint_y=None, height=40)
            ingredient_text = Label(text=ingredient)
            remove_button = Button(text='Remove', size_hint_x=None, width=80)
            remove_button.bind(on_press=lambda x: self.remove_ingredient(ingredient_label, ingredient))
            ingredient_label.add_widget(ingredient_text)
            ingredient_label.add_widget(remove_button)
            self.ingredients_list.add_widget(ingredient_label)
            self.ingredient_input.text = ''

    def remove_ingredient(self, ingredient_layout, ingredient):
        if ingredient in self.ingredients:
            self.ingredients.remove(ingredient)
            self.ingredients_list.remove_widget(ingredient_layout)

    def save_recipe(self, instance):
        recipe_name = self.recipe_name_input.text.strip()
        if recipe_name:
            self.manager.recipe_book.append({
                'name': recipe_name,
                'description': self.description,
                'ingredients': self.ingredients
            })

            self.recipe_name_input.text = ''
            self.description_input.text = ''
            self.ingredient_input.text = ''
            self.description = []
            self.ingredients = []
            self.description_list.clear_widgets()
            self.ingredients_list.clear_widgets()
            self.step_number = 1
            self.manager.current = 'recipe_book'

    def go_to_main_menu(self, instance):
        self.manager.current = 'main_menu'

class RecipeBookScreen(Screen):
    def __init__(self, **kwargs):
        super(RecipeBookScreen, self).__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical')

        self.recipe_list = GridLayout(cols=1, size_hint_y=None)
        self.recipe_list.bind(minimum_height=self.recipe_list.setter('height'))
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
        scroll_view.add_widget(self.recipe_list)
        self.main_layout.add_widget(scroll_view)

        bottom_layout = BoxLayout(size_hint_y=None, height=50)
        bottom_layout.add_widget(Label())
        self.main_menu_button = Button(text='Main Menu', size_hint=(None, None), size=(120, 50))
        self.main_menu_button.bind(on_press=self.go_to_main_menu)
        bottom_layout.add_widget(self.main_menu_button)
        self.main_layout.add_widget(bottom_layout)

        self.add_widget(self.main_layout)

    def on_enter(self):
        self.recipe_list.clear_widgets()
        for recipe in self.manager.recipe_book:
            recipe_name = recipe['name']
            btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            btn = Button(text=recipe_name, size_hint_x=0.8)
            btn.bind(on_press=lambda instance, r=recipe: self.show_recipe_description(r))
            delete_btn = Button(text='Delete', size_hint_x=0.2)
            delete_btn.bind(on_press=lambda instance, r=recipe: self.delete_recipe(r))
            btn_layout.add_widget(btn)
            btn_layout.add_widget(delete_btn)
            self.recipe_list.add_widget(btn_layout)

    def show_recipe_description(self, recipe):
        self.current_recipe = recipe
        self.clear_widgets()
        description_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        name_label = Label(text=f"Recipe: {recipe['name']}", font_size='20sp')
        description_label = Label(text="Description:")
        description_list = BoxLayout(orientation='vertical', size_hint_y=None, height=200)
        for step in recipe['description']:
            description_list.add_widget(Label(text=step))
        ingredients_label = Label(text="Ingredients:")
        ingredients_list = BoxLayout(orientation='vertical', size_hint_y=None, height=200)
        for ingredient in recipe['ingredients']:
            ingredients_list.add_widget(Label(text=ingredient))

        add_to_menu_button = Button(text='Add to Food Menu')
        add_to_menu_button.bind(on_press=self.add_to_food_menu)
        back_button = Button(text='Back to Recipe Book')
        back_button.bind(on_press=self.back_to_recipe_book)

        description_layout.add_widget(name_label)
        description_layout.add_widget(description_label)
        description_layout.add_widget(description_list)
        description_layout.add_widget(ingredients_label)
        description_layout.add_widget(ingredients_list)
        description_layout.add_widget(add_to_menu_button)
        description_layout.add_widget(back_button)
        self.add_widget(description_layout)

    def add_to_food_menu(self, instance):
        self.manager.food_menu.append(self.current_recipe)
        self.manager.current = 'food_menu'

    def delete_recipe(self, recipe):
        if recipe in self.manager.recipe_book:
            self.manager.recipe_book.remove(recipe)
        self.on_enter()

    def back_to_recipe_book(self, instance):
        self.clear_widgets()
        self.add_widget(self.main_layout)
        self.on_enter()

    def go_to_main_menu(self, instance):
        self.manager.current = 'main_menu'

class FoodMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(FoodMenuScreen, self).__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical')

        self.food_menu_list = GridLayout(cols=1, size_hint_y=None)
        self.food_menu_list.bind(minimum_height=self.food_menu_list.setter('height'))
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
        scroll_view.add_widget(self.food_menu_list)
        self.main_layout.add_widget(scroll_view)

        bottom_layout = BoxLayout(size_hint_y=None, height=50)
        bottom_layout.add_widget(Label())
        self.main_menu_button = Button(text='Main Menu', size_hint=(None, None), size=(120, 50))
        self.main_menu_button.bind(on_press=self.go_to_main_menu)
        bottom_layout.add_widget(self.main_menu_button)
        self.main_layout.add_widget(bottom_layout)

        self.add_widget(self.main_layout)

    def on_enter(self):
        self.food_menu_list.clear_widgets()
        for recipe in self.manager.food_menu:
            recipe_name = recipe['name']
            btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            btn = Button(text=recipe_name, size_hint_x=0.8)
            btn.bind(on_press=lambda instance, r=recipe: self.show_recipe_details(r))
            remove_btn = Button(text='Remove', size_hint_x=0.2)
            remove_btn.bind(on_press=lambda instance, r=recipe: self.remove_from_food_menu(r))
            btn_layout.add_widget(btn)
            btn_layout.add_widget(remove_btn)
            self.food_menu_list.add_widget(btn_layout)

    def show_recipe_details(self, recipe):
        self.current_recipe = recipe
        self.clear_widgets()
        description_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        name_label = Label(text=f"Recipe: {recipe['name']}", font_size='20sp')
        description_label = Label(text="Description:")
        description_list = BoxLayout(orientation='vertical', size_hint_y=None, height=200)
        for step in recipe['description']:
            description_list.add_widget(Label(text=step))
        ingredients_label = Label(text="Ingredients:")
        ingredients_list = BoxLayout(orientation='vertical', size_hint_y=None, height=200)
        for ingredient in recipe['ingredients']:
            ingredients_list.add_widget(Label(text=ingredient))

        add_to_cart_button = Button(text='Add Ingredients to Cart')
        add_to_cart_button.bind(on_press=self.add_ingredients_to_cart)
        back_button = Button(text='Back to Food Menu')
        back_button.bind(on_press=self.back_to_food_menu)

        description_layout.add_widget(name_label)
        description_layout.add_widget(description_label)
        description_layout.add_widget(description_list)
        description_layout.add_widget(ingredients_label)
        description_layout.add_widget(ingredients_list)
        description_layout.add_widget(add_to_cart_button)
        description_layout.add_widget(back_button)
        self.add_widget(description_layout)

    def remove_from_food_menu(self, recipe):
        if recipe in self.manager.food_menu:
            self.manager.food_menu.remove(recipe)
            # Also remove from shopping cart
            self.manager.shopping_cart = [item for item in self.manager.shopping_cart if item not in recipe['ingredients']]
        self.on_enter()

    def add_ingredients_to_cart(self, instance):
        for ingredient in self.current_recipe['ingredients']:
            self.manager.shopping_cart.append(ingredient)

    def back_to_food_menu(self, instance):
        self.clear_widgets()
        self.add_widget(self.main_layout)  # Refers to the layout added previously
        self.on_enter()  # Ensure the list is updated

    def go_to_main_menu(self, instance):
        self.manager.current = 'main_menu'

class ShoppingCartScreen(Screen):
    def __init__(self, **kwargs):
        super(ShoppingCartScreen, self).__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical')

        self.shopping_cart_list = GridLayout(cols=1, size_hint_y=None)
        self.shopping_cart_list.bind(minimum_height=self.shopping_cart_list.setter('height'))
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
        scroll_view.add_widget(self.shopping_cart_list)
        self.main_layout.add_widget(scroll_view)

        bottom_layout = BoxLayout(size_hint_y=None, height=50)
        bottom_layout.add_widget(Label())
        self.main_menu_button = Button(text='Main Menu', size_hint=(None, None), size=(120, 50))
        self.main_menu_button.bind(on_press=self.go_to_main_menu)
        bottom_layout.add_widget(self.main_menu_button)
        self.main_layout.add_widget(bottom_layout)

        self.add_widget(self.main_layout)

    def on_enter(self):
        self.shopping_cart_list.clear_widgets()
        for ingredient in self.manager.shopping_cart:
            ingredient_label = Label(text=ingredient, size_hint_x=0.8)
            remove_button = Button(text='Remove', size_hint_x=0.2)
            remove_button.bind(on_press=lambda instance, i=ingredient: self.remove_from_cart(i))
            layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            layout.add_widget(ingredient_label)
            layout.add_widget(remove_button)
            self.shopping_cart_list.add_widget(layout)

    def remove_from_cart(self, ingredient):
        if ingredient in self.manager.shopping_cart:
            self.manager.shopping_cart.remove(ingredient)
        self.on_enter()

    def go_to_main_menu(self, instance):
        self.manager.current = 'main_menu'
