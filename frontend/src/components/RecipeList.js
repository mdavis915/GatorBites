import React from 'react';
import RecipeCard from './RecipeCard';

const RecipeList = ({ recipes, onRecipeClick, selectedTags, searchAttempted }) => {
    console.log('Recipes passed to RecipeList:', recipes);

    const filteredRecipes = recipes.filter(recipe => recipe && typeof recipe === 'object');

    // Extract all unique tags from the filtered recipes
    const allTags = [...new Set(filteredRecipes.flatMap(recipe => recipe.matched_tags || []))];

    return (
        <div className="recipe-list" style={styles.listContainer}>
            {searchAttempted && filteredRecipes.length === 0 && (
                <p style={styles.emptyMessage}>No recipes found.</p>
            )}
            {filteredRecipes.length > 0 &&
                filteredRecipes.map((recipe, index) => {
                    console.log('Recipe Tags:', recipe.matched_tags);

                    const recipeKey = recipe.id || recipe.name || index;

                    return (
                        <RecipeCard
                            key={recipeKey}
                            recipe={recipe}
                            onClick={onRecipeClick}
                            selectedTags={selectedTags}
                            allTags={allTags}
                        />
                    );
                })}
        </div>
    );
};



const styles = {
    listContainer: {
        display: 'flex',
        flexWrap: 'wrap',
        gap: '16px',
        padding: '10px',
        justifyContent: 'center',
        alignItems: 'flex-start',
    },
    emptyMessage: {
        fontSize: '18px',
        color: '#555',
    },
};

export default RecipeList;
