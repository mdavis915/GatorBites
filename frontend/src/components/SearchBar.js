import React, { useState } from 'react';

const PREDEFINED_TAGS = [
    "vegan", "vegetarian", "gluten-free", "low-carb", "high-protein", "dairy-free",
    "nut-free", "low-fat", "italian", "mexican", "indian", "chinese", "mediterranean",
    "american", "thai", "japanese", "breakfast", "lunch", "dinner", "snack", "dessert",
    "grilled", "baked", "fried", "roasted", "slow-cooked", "raw", "spicy", "sweet", "savory",
    "sour", "salty"
];

const SearchBar = ({ onSearch }) => {
    const [tags, setTags] = useState([]);
    const [ingredients, setIngredients] = useState('');

    const handleTagClick = (tag) => {
        if (tags.includes(tag)) {
            setTags(tags.filter(t => t !== tag)); 
        } else {
            setTags([...tags, tag]); 
        }
    };

    const handleSearch = () => {
        onSearch(ingredients, tags);
    };

    return (
        <div className="search-bar" style={{ margin: '20px 0' }}>
            <label
                htmlFor="ingredientsInput"
                style={{
                    fontWeight: 'bold',
                    textAlign: 'left', 
                    display: 'block', 
                    marginBottom: '5px' 
                }}
            >
                Enter up to 10 ingredients (separated by commas):
            </label>
            <input
                type="text"
                id="ingredientsInput"
                placeholder="Enter ingredients..."
                value={ingredients}
                onChange={(e) => setIngredients(e.target.value)}
                style={{
                    padding: '8px',
                    fontSize: '14px',
                    width: '60%',
                    margin: '10px 0',
                    borderRadius: '4px',
                    border: '1px solid #ccc'
                }}
            />
            <button
                onClick={handleSearch}
                style={{
                    padding: '8px 16px',
                    fontSize: '14px',
                    marginLeft: '10px',
                    borderRadius: '4px',
                    backgroundColor: '#FF7F50',
                    color: '#fff',
                    border: 'none',
                    cursor: 'pointer'
                }}
            >
                Search
            </button>
        </div>
    );
};

export default SearchBar;
