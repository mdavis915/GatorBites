import React, { useEffect, useState } from 'react';
import axios from 'axios';

const RecipeDetails = ({ recipeName, onBack }) => {
  const [recipe, setRecipe] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchRecipeDetails = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/recipe/${recipeName}`);
        setRecipe(response.data);
        setError('');
      } catch (err) {
        setError(err.response?.data?.error || 'An error occurred.');
      }
    };

    fetchRecipeDetails();
  }, [recipeName]);

  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  if (!recipe) return <p>Loading...</p>;

  return (
    <div>
      <button onClick={onBack}>Back</button>
      <h2>{recipe.name}</h2>
      <p>{recipe.description}</p>
      <p>Total time: {recipe.minutes} minutes</p>
      <p>Steps: {recipe.n_steps}</p>
      <ol>
        {recipe.steps.map((step, index) => (
          <li key={index}>{step}</li>
        ))}
      </ol>
      <h3>Ingredients:</h3>
      <ul>
        {recipe.ingredients.map((ingredient, index) => (
          <li key={index}>{ingredient}</li>
        ))}
      </ul>
    </div>
  );
};

export default RecipeDetails;
