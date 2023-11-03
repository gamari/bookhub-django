async function deleteMemo(id, url) {
    const response = await fetch(url, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    });

    if (!response.ok) {
        throw new Error("メモの削除に失敗しました。");
    }

    const data = await response.json();
    return data;
}
