class recipe_nodes:
    def __init__(self):
        self.children = {}
        self.recipes = set()

class Trie:
    def __init__(self):
        self.root = recipe_nodes()
        self.stored_ingredient = {}

    #insertion into trie
    def insert(self, recipe_name, ingredients):
        #add ingredients
        node = self.root
        for recipe in recipe_name:
            if recipe not in node.children:
                node.children[recipe] = recipe_nodes()
            node = node.children[recipe]
        node.recipes.add(tuple(ingredients))
        #add recipe names
        for ingredient in ingredients:
            if ingredient not in self.stored_ingredient:
                self.stored_ingredient[ingredient] = set()
            self.stored_ingredient[ingredient].add(recipe_name)

    #search for recipes based on ingedients
    def search_ingredients(self, ingredients, restrictions):
        matching_recipes = []
        #if exact match wanted
        if restrictions == 'yes':
            for recipe_name, recipe_ingredients in self.stored_ingredient.items():
                if set(ingredients) == recipe_ingredients:
                    matching_recipes.add(recipe_name)
                    return list(set(matching_recipes))  
            return 
        #items with at least one ingredient
        else:
            for ingredient in ingredients:
                if ingredient in self.stored_ingredient:
                    matching_recipes.extend(self.stored_ingredient[ingredient])
            return list(set(matching_recipes))  
