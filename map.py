import pandas as pd
import json

class HashMap:
    def __init__(self, size=1000):
        self.size = size
        self.table = [[] for _ in range(size)]  # Initialize with empty lists for chaining

    def hash_function(self, key):
        return sum(ord(char) for char in str(key)) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value  # Update value if key exists
                return
        self.table[index].append([key, value])  # Add new key-value pair

    def get(self, key):
        index = self.hash_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        return None  # Key not found

    def delete(self, key):
        index = self.hash_function(key)
        for i, pair in enumerate(self.table[index]):
            if pair[0] == key:
                del self.table[index][i]
                return True  # Key deleted
        return False  # Key not found

    def count(self):
        total_entries = 0
        for bucket in self.table:
            total_entries += len(bucket)  # Count entries in each bucket
        return total_entries

def create_hashmap():
    file_path = 'RAW_recipes.csv'  # Path to your CSV file
    try:
        df = pd.read_csv(file_path, low_memory=False)
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: The file {file_path} is empty.")
        return

    # Custom hash map to store recipes by their IDs
    recipe_map = HashMap(size=1000)

    for index, row in df.iterrows():
        try:
            # Extract recipe details
            recipe_name = str(row['name']).strip() if pd.notnull(row['name']) else "Unnamed Recipe"
            total_time = int(row['minutes']) if pd.notnull(row['minutes']) else 0
            date_submitted = str(row['submitted']).strip() if pd.notnull(row['submitted']) else "Unknown"
            description = str(row['description']).strip() if pd.notnull(row['description']) else None

            # Tags (parse safely)
            tags = []
            if pd.notnull(row['tags']):
                try:
                    tags = json.loads(row['tags'].replace("'", "\""))
                except json.JSONDecodeError:
                    tags = []  # Set default value if parsing fails

            # Ingredients (parse safely)
            ingredients = []
            if pd.notnull(row['ingredients']):
                try:
                    ingredients = json.loads(row['ingredients'].replace("'", "\""))
                except json.JSONDecodeError:
                    ingredients = []  # Set default value if parsing fails

            # Instructions (parse safely)
            instructions = []
            if pd.notnull(row['steps']):
                try:
                    instructions = json.loads(row['steps'].replace("'", "\""))
                except json.JSONDecodeError:
                    instructions = []  # Set default value if parsing fails

            # Number of steps and ingredients
            num_steps = int(row['n_steps']) if pd.notnull(row['n_steps']) else len(instructions)
            num_ingredients = int(row['n_ingredients']) if pd.notnull(row['n_ingredients']) else len(ingredients)

            # Store in custom hash map
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
            # Skip any rows with errors
            continue

    # Count the number of entries in the hash map
    total_entries = recipe_map.count()
    print(f"Total number of entries in the hash map: {total_entries}")

    # Save the hashmap to a file for later use
    output_file = 'recipe_map.json'
    with open(output_file, 'w') as json_file:
        serialized_map = {}
        for index in range(recipe_map.size):
            for key, value in recipe_map.table[index]:
                serialized_map[key] = value
        json.dump(serialized_map, json_file, indent=4)

    print(f"Hash map saved with recipes to {output_file}.")

if __name__ == "__main__":
    create_hashmap()