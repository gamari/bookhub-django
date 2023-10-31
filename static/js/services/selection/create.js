async function createSelectionByAi(demand) {
    const response = await fetch('/api/ai/selection/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCsrfToken()
        },
        body: JSON.stringify({ "demand": demand})
    });
    
    if (!response.ok) {
        throw new Error('作成に失敗しました。');
    }

    const result = await response.json();
    return result;   
}