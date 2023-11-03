async function deleteMemo(id, url) {
    const response = await fetch(url, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    });
    const data = await response.json();

    if (data.result === 'success') {
        return data;
    } else {
        throw new Error("メモの削除に失敗しました。");
    }

}
