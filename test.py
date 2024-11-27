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

@app.route('/search', methods=['POST'])
def search_recipes():
    """
    Search recipes by ingredients and other optional filters.
    Request JSON format: { "ingredients": ["ingredient1", "ingredient2", ...], "max_minutes": 45, "min_steps": 3 }
    """
    data = request.get_json()

    # Check if ingredients field is present
    if not data or 'ingredients' not in data:
        return jsonify({"error": "Ingredients are required"}), 400

    # Normalize user-provided ingredients
    user_ingredients = set(ing.lower().strip() for ing in data.get('ingredients', [])[:MAX_INGREDIENTS])

    # If no ingredients are provided, return an error
    if not user_ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    # Extract filter criteria from the request data
    max_minutes = data.get('max_minutes', float('inf'))  # Default to infinity (no limit)
    min_steps = data.get('min_steps', 0)  # Default to 0 (no minimum)
    max_steps = data.get('max_steps', float('inf'))  # Default to infinity (no limit)

    # Filter recipes by matching ingredients and the filter criteria
    matching_recipes = []
    for recipe_id, recipe_data in recipe_map.items():
        recipe_ingredients = set(ing.strip().lower() for ing in recipe_data['ingredients'])
        matched = user_ingredients.intersection(recipe_ingredients)

        # Apply the additional filters
        if matched:
            if (recipe_data['total_time'] <= max_minutes and
                recipe_data['num_steps'] >= min_steps and
                recipe_data['num_steps'] <= max_steps):
                matching_recipes.append({
                    "name": recipe_data['name'],
                    "description": recipe_data['description'],
                    "minutes": recipe_data['total_time'],
                    "matched_ingredients": list(matched),
                    "missing_ingredients": list(recipe_ingredients - matched),
                    "n_steps": recipe_data['num_steps'],
                    "tags": recipe_data['tags'],
                })

    # Sort recipes by the number of matched ingredients
    matching_recipes.sort(key=lambda x: len(x["matched_ingredients"]), reverse=True)

    # Limit the number of recipes returned
    matching_recipes = matching_recipes[:MAX_RESULTS]

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

    # Return detailed information about the recipe with name before description
    return jsonify({
        "name": recipe['name'],  # Name first
        "description": recipe['description'],  # Description second
        "minutes": recipe['total_time'],
        "tags": recipe['tags'],
        "n_steps": recipe['num_steps'],
        "steps": recipe['instructions'],
        "ingredients": recipe['ingredients'],
        "n_ingredients": recipe['num_ingredients']
    })

if __name__ == '__main__':
    app.run(debug=True)
