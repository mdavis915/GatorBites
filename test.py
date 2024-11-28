from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Constants
MAX_RESULTS = 10
MAX_INGREDIENTS = 10

# Load the hash map from the saved JSON file
def load_recipe_hashmap():
    try:
        with open('recipe_map.json', 'r') as file:
            recipe_map = json.load(file)
        return recipe_map
    except FileNotFoundError:
        print("Error: The hash map file 'recipe_map.json' was not found.")
        return {}
    except json.JSONDecodeError:
        print("Error: The hash map file 'recipe_map.json' is corrupted.")
        return {}

# Load the recipes from the hash map
recipe_map = load_recipe_hashmap()

PREDEFINED_TAGS = {
    "vegan", "vegetarian", "gluten-free", "low-carb", "high-protein", "dairy-free",
    "nut-free", "low-fat", "italian", "mexican", "indian", "chinese", "mediterranean",
    "american", "thai", "japanese", "breakfast", "lunch", "dinner", "snack", "dessert", 
    "grilled", "baked", "fried", "roasted", "slow-cooked", "raw", "spicy", "sweet", "savory", 
    "sour", "salty"
}

@app.route('/search', methods=['POST'])
def search_recipes():
    data = request.get_json()

    if not data or 'ingredients' not in data:
        return jsonify({"error": "Ingredients are required"}), 400

    user_ingredients = set(ing.lower().strip() for ing in data.get('ingredients', [])[:MAX_INGREDIENTS])

    if not user_ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    # Get tags filter, if provided, and ensure they match predefined tags
    user_tags = set(tag.lower().strip() for tag in data.get('tags', []))
    
    # Check if any provided tags are invalid
    invalid_tags = user_tags - PREDEFINED_TAGS
    if invalid_tags:
        return jsonify({"error": f"Invalid tags provided: {', '.join(invalid_tags)}"}), 400

    sort_by = data.get('sort_by', 'matched_ingredients')
    matching_recipes = []

    for recipe_id, recipe_data in recipe_map.items():
        recipe_ingredients = set(ing.strip().lower() for ing in recipe_data.get('ingredients', []))
        matched_ingredients = user_ingredients.intersection(recipe_ingredients)

        # Check if recipe matches tags
        matched_tags = user_tags.intersection(set(recipe_data.get('tags', [])))

        # Skip recipes with total_time of 0
        if recipe_data['total_time'] == 0:
            continue

        if matched_ingredients and (not user_tags or matched_tags):  # If any tags match
            matching_recipes.append({
                "name": recipe_data['name'],
                "description": recipe_data.get('description', 'Description not available'),
                "minutes": recipe_data['total_time'],
                "matched_ingredients": list(matched_ingredients),
                "missing_ingredients": list(recipe_ingredients - matched_ingredients),
                "n_steps": recipe_data['num_steps'],
                "tags": recipe_data['tags'],
                "instructions": recipe_data['instructions'],  # Make sure instructions are included
            })

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


@app.route('/recipe/<recipe_name>', methods=['GET'])
def get_recipe_details(recipe_name):
    """
    Get detailed information about a specific recipe by name.
    """
    # Find the recipe by name in the hash map
    recipe = None
    for recipe_id, recipe_data in recipe_map.items():
        if recipe_data['name'].lower() == recipe_name.lower():
            recipe = recipe_data
            break

    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    # If description is null or empty, set to "Description not available"
    description = recipe.get('description', 'Description not available')

    # Return detailed information about the recipe
    return jsonify({
        "name": recipe['name'],  # Name first
        "description": description,  # Description second
        "minutes": recipe['total_time'],
        "tags": recipe['tags'],
        "n_steps": recipe['num_steps'],
        "steps": recipe.get('instructions', []),  # Include instructions
        "ingredients": recipe['ingredients'],
        "n_ingredients": recipe['num_ingredients']
    })

if __name__ == '__main__':
    app.run(debug=True)
