async function deleteSelection(id) {
    const response = await fetch(`/api/selection/${id}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCsrfToken(),
        },
    });

    if (!response.ok) {
        console.log(response.statusText);
        throw new Error("削除に失敗しました。")
    }
}