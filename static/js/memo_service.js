async function deleteMemo(id, url) {
    const response = await fetch(url, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    });
    const data = await response.json();

    if (data.result === 'success') {
        // TODO 成功
    } else {
        // TODO 失敗
        console.error('Failed to delete memo');
    }

}