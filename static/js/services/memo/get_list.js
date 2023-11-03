async function getMemoList() {
    let apiUrl = '/api/memos/';
    const response = fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    });

    const json = await response.json();

    return json;
}

/** 対象日より前のメモ一覧を取得する */
async function getMemoListToBookBeforeDate(book_id, date) {
    let csrfToken = getCsrfToken();
    let apiUrl = `/api/books/${book_id}/memos/`;

    if (date) {
        apiUrl += `?previous_date=${date}`;
    }

    const response = await fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    });

    const json = await response.json();

    return json;
}