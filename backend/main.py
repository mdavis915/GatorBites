from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import ast
import json

app = Flask(__name__)
CORS(app)
MAX_INGREDIENTS = 10
MAX_RESULTS = 30
PREDEFINED_TAGS = {
    "vegan", "vegetarian", "gluten-free", "low-carb", "high-protein", "dairy-free",
    "nut-free", "low-fat", "italian", "mexican", "indian", "chinese", "mediterranean",
    "american", "thai", "japanese", "breakfast", "lunch", "dinner", "snack", "dessert", 
    "grilled", "baked", "fried", "roasted", "slow-cooked", "raw", "spicy", "sweet", "savory", 
    "sour", "salty"
}

# Trie Data Structure for Ingredient-Based Lookup
class TrieNode:
    def __init__(self):
        self.children = {}
        self.recipes = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, ingredient, recipe):
        node = self.root
        for char in ingredient:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.recipes.append(recipe)

    def search(self, ingredient):
        node = self.root
        for char in ingredient:
            if char not in node.children:
                return []
            node = node.children[char]
        return node.recipes

# Trie Data Structure for Name-Based Lookup
class NameTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, name, recipe):
        if not isinstance(name, str):
            name = str(name)  
        if not name.strip():
            raise ValueError("Recipe name cannot be empty")
        node = self.root
        for char in name.lower():  
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.recipes.append(recipe)

    def search(self, name):
        node = self.root
        for char in name.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        return node.recipes


def load_trie(data_file, trie):
    # Load the dataset
    recipes_df = pd.read_csv(data_file)

    recipes = []
    for _, row in recipes_df.iterrows():
        recipe_name = str(row["name"]) if pd.notna(row["name"]) else "Unnamed Recipe"
        recipe_name = recipe_name.title()
        description = row["description"] if pd.notna(row["description"]) and row["description"] != "#NAME?" else "Description not available"

        tags = row["tags"]
        try:
            tags = ast.literal_eval(tags) if pd.notna(tags) else []
            if not isinstance(tags, list):
                tags = []
        except (ValueError, SyntaxError):
            tags = []

        # Ensure 'ingredients' is always a list, even if it's malformed
        ingredients = row["ingredients"]
        try:
            ingredients = ast.literal_eval(ingredients) if pd.notna(ingredients) else []
            if not isinstance(ingredients, list):
                ingredients = []
        except (ValueError, SyntaxError):
            ingredients = []

        instructions = row["steps"]
        try:
            instructions = ast.literal_eval(instructions) if pd.notna(instructions) else []
            if not isinstance(instructions, list):
                instructions = []
        except (ValueError, SyntaxError):
            instructions = []

        instructions = [sentence.strip().capitalize() if sentence else "" for sentence in instructions]

        # Append the cleaned recipe
        recipes.append({
            "name": recipe_name,
            "total_time": row["minutes"] if pd.notna(row["minutes"]) else "Time not available",
            "num_steps": row["n_steps"] if pd.notna(row["n_steps"]) else 0,
            "tags": tags,
            "description": description,
            "ingredients": ingredients,
            "instructions": instructions
        })

    # Populate the Trie with recipes based on ingredients
    for recipe in recipes:
        for ingredient in recipe['ingredients']:
            trie.insert(ingredient, recipe)

    return recipes


def load_nameTrie(data_file, trie):
    # Read the CSV file into a DataFrame
    recipes_df = pd.read_csv(data_file)

    name_trie = trie

    for _, row in recipes_df.iterrows():
        name = str(row["name"]).strip() if pd.notna(row["name"]) else "Unnamed Recipe"
        name = name.title()
        
        if not name:
            continue
        
        tags = row["tags"]
        try:
            tags = ast.literal_eval(tags) if pd.notna(tags) else []
            if not isinstance(tags, list):
                tags = []
        except (ValueError, SyntaxError):
            tags = []  

        ingredients = row["ingredients"]
        try:
            ingredients = ast.literal_eval(ingredients) if pd.notna(ingredients) else []
            if not isinstance(ingredients, list):
                ingredients = []
        except (ValueError, SyntaxError):
            ingredients = []  

        instructions = row["steps"]
        try:
            instructions = ast.literal_eval(instructions) if pd.notna(instructions) else []
            if not isinstance(instructions, list):
                instructions = []
        except (ValueError, SyntaxError):
            instructions = []  

        description = row["description"] if pd.notna(row["description"]) and row["description"] != "#NAME?" else "Description not available"
        
        description = '. '.join([sentence.strip().capitalize() if sentence else "" for sentence in description.split('. ')])


        instructions = [sentence.strip().capitalize() if sentence else "" for sentence in instructions]

        recipe = {
            "name": name,
            "total_time": row["minutes"] if pd.notna(row["minutes"]) else "Time not available",
            "num_steps": row["n_steps"] if pd.notna(row["n_steps"]) else 0,
            "tags": tags,
            "description": description,
            "ingredients": ingredients,
            "instructions": instructions
        }


        name_trie.insert(name.lower(), recipe)

    # Return the populated name_trie
    return name_trie

# HashMap Data Structure 
class HashMap:
    def __init__(self, size=1000):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        return sum(ord(char) for char in str(key)) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value  
                return
        self.table[index].append([key, value])  

    def get(self, key):
        index = self.hash_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        return None  

    def delete(self, key):
        index = self.hash_function(key)
        for i, pair in enumerate(self.table[index]):
            if pair[0] == key:
                del self.table[index][i]
                return True 
        return False 

    def get_all_items(self):
        items = []
        for bucket in self.table:
            for pair in bucket:
                items.append(pair)
        return items

def format_title(title):
    return ' '.join(word.capitalize() for word in title.split())

def format_description(description):
    if description:
        return description[0].capitalize() + description[1:] if len(description) > 1 else description.capitalize()
    return None

def capitalize_steps(steps):
    return [f"{step.strip().capitalize()}" for i, step in enumerate(steps)]

def capitalize_ingredients(ingredients):
    return [ingredient.strip().capitalize() for ingredient in ingredients]

# Function to load recipes into the HashMap
def load_hashmap():
    file_path = 'RAW_recipes.csv'  
    try:
        df = pd.read_csv(file_path, low_memory=False)
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: The file {file_path} is empty.")
        return

    recipe_map = HashMap(size=1000)

    for index, row in df.iterrows():
        try:
            # Extract recipe details
            recipe_name = str(row['name']).strip() if pd.notnull(row['name']) else "Unnamed Recipe"
            recipe_name = format_title(recipe_name)  

            total_time = int(row['minutes']) if pd.notnull(row['minutes']) else 0
            date_submitted = str(row['submitted']).strip() if pd.notnull(row['submitted']) else "Unknown"
            description = str(row['description']).strip() if pd.notnull(row['description']) else None
            description = format_description(description)  
            tags = []
            if pd.notnull(row['tags']):
                try:
                    tags = json.loads(row['tags'].replace("'", "\""))
                except json.JSONDecodeError:
                    tags = []  

            ingredients = []
            if pd.notnull(row['ingredients']):
                try:
                    ingredients = json.loads(row['ingredients'].replace("'", "\""))
                    ingredients = capitalize_ingredients(ingredients)  
                except json.JSONDecodeError:
                    ingredients = []  

            instructions = []
            if pd.notnull(row['steps']):
                try:
                    instructions = json.loads(row['steps'].replace("'", "\""))
                    instructions = capitalize_steps(instructions)  
                except json.JSONDecodeError:
                    instructions = []  

            # Number of steps and ingredients
            num_steps = int(row['n_steps']) if pd.notnull(row['n_steps']) else len(instructions)
            num_ingredients = int(row['n_ingredients']) if pd.notnull(row['n_ingredients']) else len(ingredients)

            recipe_map.insert(index, {
                "name": recipe_name,
                "total_time": total_time,
                "date_submitted": date_submitted,
                "description": description,
                "tags": tags,
                "ingredients": ingredients,
                "instructions": instructions,
                "num_steps": num_steps,
                "num_ingredients": num_ingredients
            })

        except Exception as e:
            continue

    return recipe_map


# Search recipes based on user input
@app.route('/search', methods=['POST'])
def search_recipes():
    data = request.get_json()

    if not data or 'ingredients' not in data:
        return jsonify({"error": "Ingredients are required"}), 400

    
    user_ingredients = set(ing.lower().strip() for ing in data.get('ingredients', [])[:MAX_INGREDIENTS])

    if not user_ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    user_tags = set(tag.lower().strip() for tag in data.get('tags', []))
    invalid_tags = user_tags - PREDEFINED_TAGS
    if invalid_tags:
        return jsonify({"error": f"Invalid tags provided: {', '.join(invalid_tags)}"}), 400

    sort_by = data.get('sort_by', 'matched_ingredients')
    data_structure = data.get('data_structure', 'hashmap').lower()

    matching_recipes = []

    if data_structure == 'trie':
        trie = Trie()

        # Load recipes into the Trie
        data_file = "RAW_recipes.csv"
        recipes = load_trie(data_file, trie)

        # Aggregate matches for all ingredients
        matched_recipes = {}
        for ingredient in user_ingredients:
            for recipe in trie.search(ingredient):
                if recipe['name'] not in matched_recipes:
                    matched_recipes[recipe['name']] = {
                        'name': recipe['name'],
                        'description': recipe.get('description', 'Description not available') if recipe.get('description') != "#NAME?" else "Description not available",
                        'minutes': recipe['total_time'],
                        'ingredients': recipe['ingredients'],
                        'num_steps': recipe['num_steps'],
                        'tags': recipe.get('tags', []), 
                        'instructions': recipe['instructions'],
                        'matched_ingredients': set(),
                    }
                matched_recipes[recipe['name']]['matched_ingredients'].add(ingredient)

        # Prepare results after filtering
        results = []
        for recipe in matched_recipes.values():
            matched_ingredients = list(recipe['matched_ingredients'])
            missing_ingredients = [ing for ing in recipe['ingredients'] if ing not in user_ingredients]

            recipe_tags = recipe.get('tags', [])

            matched_tags = [tag for tag in user_tags if tag in recipe_tags]

            # Exclude recipes with no total time or missing tag matches
            if recipe['minutes'] == 0:
                continue
            if user_tags and not matched_tags:
                continue

            results.append({
                'name': recipe['name'],
                'description': recipe['description'],
                'minutes': recipe['minutes'],
                'matched_ingredients': matched_ingredients,
                'missing_ingredients': missing_ingredients,
                'n_steps': recipe['num_steps'],
                'matched_tags': matched_tags,
                'instructions': recipe['instructions'],
            })

        # Sorting logic
        if sort_by == "matched_ingredients":
            results.sort(key=lambda x: len(x["matched_ingredients"]), reverse=True)
        elif sort_by == "missing_ingredients":
            results.sort(key=lambda x: len(x["missing_ingredients"]))
        elif sort_by == "total_time":
            results.sort(key=lambda x: x["minutes"])
        elif sort_by == "num_steps":
            results.sort(key=lambda x: x["n_steps"])

        results = results[:MAX_RESULTS]

        if not results:
            return jsonify({"message": "No recipes found for the given ingredients."}), 404

        return jsonify({
            "total_matches": len(results),
            "recipes": results
        })


    if data_structure == 'hashmap':
        matching_recipes = []

        recipe_map = load_hashmap()

        # Gather all matching recipes
        for recipe_id, recipe_data in recipe_map.get_all_items():  # Getting all items from HashMap
            recipe_ingredients = set(ing.strip().lower() for ing in recipe_data.get('ingredients', []))
            matched_ingredients = user_ingredients.intersection(recipe_ingredients)
            matched_tags = user_tags.intersection(set(recipe_data.get('tags', [])))

            # Exclude recipes with zero total_time
            if recipe_data['total_time'] == 0:
                continue

            # Check if there are matched ingredients and, if necessary, matched tags
            if matched_ingredients and (not user_tags or matched_tags):
                matching_recipes.append({
                    "name": recipe_data['name'],
                    "description": recipe_data.get('description', 'Description not available'),
                    "minutes": recipe_data['total_time'],
                    "matched_ingredients": list(matched_ingredients),
                    "missing_ingredients": list(recipe_ingredients - matched_ingredients),
                    "n_steps": recipe_data['num_steps'],
                    "matched_tags": list(matched_tags),
                    "instructions": recipe_data['instructions'],
                })

        # Sorting logic
        if sort_by == "matched_ingredients":
            matching_recipes.sort(key=lambda x: len(x["matched_ingredients"]), reverse=True)
        elif sort_by == "missing_ingredients":
            matching_recipes.sort(key=lambda x: len(x["missing_ingredients"]))
        elif sort_by == "total_time":
            matching_recipes.sort(key=lambda x: x["minutes"])
        elif sort_by == "num_steps":
            matching_recipes.sort(key=lambda x: x["n_steps"])

        matching_recipes = matching_recipes[:MAX_RESULTS]

        if not matching_recipes:
            return jsonify({"message": "No recipes found for the given ingredients."}), 404

        return jsonify({
            "total_matches": len(matching_recipes),
            "recipes": matching_recipes
        })

# Route for Trie-based recipe search
@app.route('/recipe/trie/<recipe_name>', methods=['GET'])
def get_recipe_from_trie(recipe_name):
    print(f"Full URL: {request.url}")
    
    name_trie = NameTrie()
    data_file = "RAW_recipes.csv"  
    recipes = load_nameTrie(data_file, name_trie)

    # Search for the recipe in the Trie
    recipes = name_trie.search(recipe_name.lower())

    if not recipes:
        return jsonify({"error": "Recipe not found"}), 404

    recipe = recipes[0]
    description = recipe.get('description', 'Description not available')

    return jsonify({
        "name": recipe['name'],
        "description": description,
        "minutes": recipe['total_time'],
        "tags": recipe['tags'],
        "n_steps": recipe['num_steps'],
        "steps": recipe.get('instructions', []),
        "ingredients": recipe['ingredients'],
        "n_ingredients": len(recipe['ingredients'])
    })

# Route for HashMap-based recipe search
@app.route('/recipe/hashmap/<recipe_name>', methods=['GET'])
def get_recipe_from_hashmap(recipe_name):
    print(f"Full URL: {request.url}")

    recipe_map = load_hashmap()
    
    # Search for the recipe in the hashmap
    recipe = None
    for recipe_id, recipe_data in recipe_map.get_all_items():
        if recipe_data['name'].lower() == recipe_name.lower():
            recipe = recipe_data
            break

    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    description = recipe.get('description', 'Description not available')

    return jsonify({
        "name": recipe['name'],
        "description": description,
        "minutes": recipe['total_time'],
        "tags": recipe['tags'],
        "n_steps": recipe['num_steps'],
        "steps": recipe.get('instructions', []),
        "ingredients": recipe['ingredients'],
        "n_ingredients": recipe['num_ingredients']
    })

# Default route for invalid data structure
@app.route('/recipe/<recipe_name>', methods=['GET'])
def handle_invalid_data_structure(recipe_name):
    return jsonify({"error": "Invalid data structure"}), 400

if __name__ == '__main__':
    app.run(debug=True)