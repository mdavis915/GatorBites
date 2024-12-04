const RecipeCard = ({ recipe, onClick, selectedTags = [] }) => {
    const matchedIngredients = recipe.matched_ingredients || [];
    const missingIngredients = recipe.missing_ingredients || [];
    const matchingTags = recipe.matched_tags || [];

    const filteredTags = selectedTags.length > 0
        ? matchingTags.filter(tag => selectedTags.includes(tag))
        : matchingTags;

    const formatTime = (minutes) => {
        const hours = Math.floor(minutes / 60);
        const remainingMinutes = minutes % 60;
        let formattedTime = '';

        if (hours > 0) {
            formattedTime += `${hours} hour${hours > 1 ? 's' : ''}`;
        }

        if (remainingMinutes > 0) {
            if (formattedTime) {
                formattedTime += ' ';
            }
            formattedTime += `${remainingMinutes} minute${remainingMinutes > 1 ? 's' : ''}`;
        }

        return formattedTime || 'N/A';
    };

    return (
        <div
            className="recipe-card"
            onClick={() => onClick(recipe.name)}
            style={{
                width: '350px', 
                height: '400px', 
                border: '1px solid #1400c4',
                borderRadius: '12px',
                padding: '15px',
                margin: '10px',
                cursor: 'pointer',
                backgroundColor: '#fff',
                transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                textAlign: 'left',
                boxShadow: '2px 2px 6px rgba(0, 0, 0, 0.1)',
                overflow: 'hidden',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
            }}
        >
            <div>
                <h3 style={{ margin: '5px 0', fontSize: '18px', color: '#333', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {recipe.name}
                </h3>
                <div style={{ fontSize: '14px', color: '#555', lineHeight: '1.6' }}>
                    <p>
                        <strong style={{ color: '#4CAF50' }}>Matching Ingredients:</strong>{' '}
                        {matchedIngredients.length > 0 ? matchedIngredients.join(', ') : 'None'}
                    </p>
                    <p>
                        <strong style={{ color: '#F44336' }}>Missing Ingredients:</strong>{' '}
                        {missingIngredients.length > 0 ? missingIngredients.join(', ') : 'None'}
                    </p>
                    <p>
                        <strong>Total Time:</strong> {formatTime(recipe.minutes || 0)}
                    </p>
                </div>
            </div>

            {filteredTags.length > 0 && (
                <div
                    className="recipe-tags-container"
                    style={{
                        display: 'flex', 
                        flexWrap: 'wrap', 
                        gap: '6px', 
                        marginTop: '10px', 
                    }}
                >
                    {filteredTags.map((tag, index) => (
                        <span
                            key={index}
                            className={`recipe-tag color-${(index % 6) + 1}`}
                            style={{
                                display: 'inline-block',
                                padding: '4px 8px',
                                fontSize: '12px',
                                borderRadius: '12px',
                                color: 'black', 
                                maxWidth: '100px',
                                textOverflow: 'ellipsis',
                                overflow: 'hidden',
                                whiteSpace: 'nowrap',
                            }}
                        >
                            {tag.charAt(0).toUpperCase() + tag.slice(1)}
                        </span>
                    ))}
                </div>
            )}
        </div>
    );
};

export default RecipeCard;
