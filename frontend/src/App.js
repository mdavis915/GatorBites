import React, { useState } from 'react';
import Header from './components/Header';
import RecipeList from './components/RecipeList';
import SearchBar from './components/SearchBar';
import Footer from './components/Footer';
import './styles/App.css';

const App = () => {
    const [recipes, setRecipes] = useState([]);
    const [selectedRecipe, setSelectedRecipe] = useState(null); 
    const [error, setError] = useState(null);
    const [sortBy, setSortBy] = useState('matched_ingredients'); 
    const [tags, setTags] = useState([]); 
    const [searchAttempted, setSearchAttempted] = useState(false);
    const [userDataStructure, setUserDataStructure] = useState('trie'); 

    const availableTags = [
        "vegan", "vegetarian", "gluten-free", "low-carb", "high-protein",
        "dairy-free", "nut-free", "low-fat", "italian", "mexican", "indian",
        "chinese", "mediterranean", "american", "thai", "japanese", "breakfast",
        "lunch", "dinner", "snack", "dessert", "grilled", "baked", "fried",
        "roasted", "slow-cooked", "raw", "spicy", "sweet", "savory", "sour",
        "salty"
    ].map(tag => tag.toLowerCase()); 

    const searchRecipes = () => {
        const ingredients = document.getElementById('ingredientsInput').value;
        console.log("Ingredients input:", ingredients); 
    
        const ingredientsArray = ingredients
            .split(',')
            .map(ingredient => ingredient.trim())
            .filter(ingredient => ingredient.length > 0);
        console.log("Ingredients array:", ingredientsArray); 
    
        
        console.log("User data structure choice:", userDataStructure);
    
        const query = {
            ingredients: ingredientsArray,
            sort_by: sortBy,
            tags: tags.length > 0 ? tags : [], 
            data_structure: userDataStructure 
        };
    
        
        console.log("Query sent to server:", JSON.stringify(query, null, 2));
    
        if (ingredientsArray.length === 0 && tags.length === 0) {
            alert('Please enter some ingredients or select at least one tag');
            return;
        }
    
        setSearchAttempted(true);
        setLoading(true);  
        setMessage('Loading results...');  
    
        // Fetch request 
        fetch('http://localhost:5000/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(query)
        })
        .then(response => {
            console.log("Response received:", response);  
    
            if (response.ok) {
                return response.text();  
            } else {
                throw new Error(`Network response was not ok: ${response.status}`);
            }
        })
        .then(text => {
            console.log("Raw response text:", text);  
    
            try {
                const data = JSON.parse(text);  
                console.log("Parsed API Response:", data);  
                return data;  
            } catch (error) {
                console.error("Error parsing JSON:", error);  
                throw new Error(`Failed to parse JSON response: ${error.message}`);
            }
        })
        .then(data => {
            // Handle the response data
            setLoading(false);  
            if (data.recipes) {
                console.log("Recipes retrieved:", data.recipes); 
                console.log("Number of results:", data.total_matches); 
                setRecipes(data.recipes);  
                setMessage(`${data.total_matches} recipes found!`);  
            } else {
                console.warn("No recipes found in the response.");
                setMessage('No recipes found');
            }
        })
        .catch(error => {
            setLoading(false);  
            console.error("Error fetching or parsing data:", error);  
            setMessage('Error fetching data');
        });
    };
    
    const [loading, setLoading] = useState(false);  
    const [message, setMessage] = useState('');  
    
    const handleRecipeClick = (recipeName) => {
        const dataStructure = userDataStructure.toLowerCase();  
        console.log("Data Structure:", dataStructure);  
    
        const encodedRecipeName = encodeURIComponent(recipeName);
        console.log("Encoded Recipe Name:", encodedRecipeName);  
    
        const url = `http://localhost:5000/recipe/${dataStructure}/${encodedRecipeName}`;
    
        // Fetch the detailed recipe info from Flask
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    setSelectedRecipe(data);  
                }
            })
            .catch(error => {
                setError('Error fetching recipe details');
                console.error('Error:', error);
            });
    };

    const handleSortChange = (event) => {
        setSortBy(event.target.value); 
    };

    const handleBackToHome = () => {
        setSelectedRecipe(null); 
    };

    const handleTagClick = (tag) => {
        const normalizedTag = tag.toLowerCase();
        if (tags.includes(normalizedTag)) {
            setTags(prevTags => prevTags.filter(t => t !== normalizedTag)); 
        } else {
            setTags(prevTags => [...prevTags, normalizedTag]); 
        }
    };

    const handleDataStructureChange = (event) => {
        setUserDataStructure(event.target.value); 
    };  

    
    return (
        <div className="app" style={{ fontFamily: 'Arial, sans-serif', padding: '1rem' }}>
            <Header />
            <SearchBar onSearch={searchRecipes} />
    
            {/* Data Structure Choice Dropdown */}
            <div style={{ marginBottom: '2rem' }}>
                <label htmlFor="data-structure" style={{ fontWeight: 'bold' }}>Choose Data Structure: </label>
                <select
                    id="data-structure"
                    value={userDataStructure}
                    onChange={handleDataStructureChange}
                    style={{ padding: '0.5rem', fontFamily: 'Arial, sans-serif' }}
                >
                    <option value="trie">Trie</option>
                    <option value="hashmap">HashMap</option>
                </select>
            </div>
    
            {/* Sorting Dropdown */}
            <div style={{ marginBottom: '2rem' }}>
                <label htmlFor="sort-options" style={{ fontWeight: 'bold' }}>Sort by: </label>
                <select
                    id="sort-options"
                    value={sortBy}
                    onChange={handleSortChange}
                    style={{ padding: '0.5rem', fontFamily: 'Arial, sans-serif' }}
                >
                    <option value="matched_ingredients">Matched Ingredients</option>
                    <option value="total_time">Total Time</option>
                    <option value="num_steps">Number of Steps</option>
                </select>
            </div>
    
            {/* Tags Section */}
            <div style={{ marginBottom: '2rem' }}>
                <strong>Filter by Tags: </strong>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
                    {availableTags.map(tag => (
                        <button
                            key={tag}
                            onClick={() => handleTagClick(tag)}
                            className={tags.includes(tag) ? 'selected' : ''}
                            style={{
                                margin: '4px',
                                padding: '6px 12px',
                                fontSize: '12px',
                                borderRadius: '5px',
                                border: tags.includes(tag) ? '2px solid #FF7F50' : '1px solid #FF7F50',
                                backgroundColor: tags.includes(tag) ? '#ccebff' : '#f9f9f9',
                                color: tags.includes(tag) ? 'black' : 'black',
                                cursor: 'pointer',
                                transition: 'all 0.2s ease-in-out',
                            }}
                        >
                            {tag.charAt(0).toUpperCase() + tag.slice(1)}
                        </button>
                    ))}
                </div>
            </div>
    
            {/* Display Loading Indicator or Recipe Results */}
            {loading ? (
                <p>Loading results...</p>
            ) : (
                <>
                    {searchAttempted && recipes.length === 0 && !loading && (
                        <p style={{ color: 'red', textAlign: 'center' }}>No recipes found</p>
                    )}
    
                    {recipes && recipes.length > 0 && (
                        <p>Showing {recipes.length} {recipes.length === 1 ? 'recipe' : 'recipes'}</p>
                    )}
    
                    {selectedRecipe ? (
                        <div className="recipe-details" style={{ marginBottom: '2rem' }}>
                            <button
                                onClick={handleBackToHome}
                                style={{
                                    padding: '0.5rem 1rem',
                                    backgroundColor: '#1400c4',
                                    color: 'white',
                                    border: 'none',
                                    cursor: 'pointer',
                                    marginBottom: '2rem',
                                    fontFamily: "'Poppins', sans-serif",
                                }}
                            >
                                Back to Recipes
                            </button>
                            <h2 style={{ marginBottom: '1rem' }}>{selectedRecipe.name}</h2>
                            <p style={{ marginBottom: '1rem' }}><strong>Description:</strong> {selectedRecipe.description}</p>
                            <p style={{ marginBottom: '1rem' }}><strong>Time:</strong> {selectedRecipe.minutes} minutes</p>
    
                            <h3 style={{ marginBottom: '1rem' }}>Ingredients:</h3>
                            <ul style={{ paddingLeft: '0', marginLeft: '1rem', marginBottom: '2rem' }}>
                                {selectedRecipe.ingredients.map((ingredient, index) => (
                                    <li key={index} style={{ marginBottom: '0.5rem' }}>
                                        {ingredient.charAt(0).toUpperCase() + ingredient.slice(1)}
                                    </li>
                                ))}
                            </ul>
    
                            <h3 style={{ marginBottom: '1rem' }}>Steps:</h3>
                            <div style={{ paddingLeft: '0', marginLeft: '1rem' }}>
                                {selectedRecipe.steps.map((step, index) => (
                                    <p key={index} style={{ marginBottom: '0.5rem' }}>
                                        {index + 1}. {step}
                                    </p>
                                ))}
                            </div>
                        </div>
                    ) : (
                        <RecipeList recipes={recipes} onRecipeClick={handleRecipeClick} />
                    )}
                </>
            )}
    
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <Footer />
        </div>
    );
    
    
};

export default App;
