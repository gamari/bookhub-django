async function createMemo(url, body_data, csrf_token) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token
        },
        body: body_data
    });
    
    const data = await response.json();

    if (data.result === 'success') {
        return data;
    } else {
        alert("メモ作成に失敗しました。");
        throw new Error("メモ作成に失敗しました。");
    }
}

