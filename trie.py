class recipe_nodes:
    def __init__(self):
        self.children = {}
        self.recipes = set()
        
class Trie:
    def __init__(self):
        self.root = recipe_nodes()
        self.stored_ingredient = {}
        
    #insertion into trie
    def insert(self, recipe_name, ingredients, recipe_details):
        #add ingredients
        node = self.root
        for recipe in recipe_name:
            if recipe not in node.children:
                node.children[recipe] = recipe_nodes()
            node = node.children[recipe]
        node.recipes.add(recipe_name)
        
        # add recipe details to stored_ingredient
        if recipe_name not in self.stored_ingredient:
            recipe_details['ingredients'] = set(ingredients)
            self.stored_ingredient[recipe_name] = {'details': recipe_details}
            
        #add recipe names
        for ingredient in ingredients:
            if ingredient not in self.stored_ingredient:
                self.stored_ingredient[ingredient] = {'recipes': set()}
            self.stored_ingredient[ingredient].setdefault('recipes', set()).add(recipe_name)

    #search for recipes based on ingedients
    def search_ingredients(self, ingredients, restrictions):
        matching_recipes = []
        #if exact match wanted
        if restrictions == 'yes':
            for recipe_name, recipe_data in self.stored_ingredient.items():
                if recipe_name != 'recipes' and recipe_data.get('details'): 
                    if set(ingredients) == recipe_data['details'].get('ingredients', set()):
                        matching_recipes.append(recipe_name)
            return list(set(matching_recipes))
        #items with at least one ingredient
        else:
            for ingredient in ingredients:
                if ingredient in self.stored_ingredient:
                    matching_recipes.extend(self.stored_ingredient[ingredient]['recipes'])
            return list(set(matching_recipes))

#read csv file
df = pd.read_csv('RAW_recipes.csv').dropna(subset=['name', 'ingredients'])
df['ingredients'] = df['ingredients'].apply(eval)
row_names = ['name', 'id', 'minutes', 'contributor_id', 'submitted', 'tags', 'nutrition', 'n_steps', 'steps', 'description', 'ingredients', 'n_ingredients']
recipes = df[row_names].to_dict(orient='records')

# create trie
recipe_trie = Trie()
for recipe in recipes:
    recipe_name = recipe['name']
    ingredients = recipe['ingredients']
    recipe_details = {'id': recipe['id'],'minutes': recipe['minutes'],'submitted': recipe['submitted'],
                      'tags': recipe['tags'],'nutrition': recipe['nutrition'],
                      'n_steps': recipe['n_steps'],'steps': recipe['steps'],'description': recipe['description'],'n_ingredients': recipe['n_ingredients']}
    recipe_trie.insert(recipe_name, ingredients, recipe_details)
