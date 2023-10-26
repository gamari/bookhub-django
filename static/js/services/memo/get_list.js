document.addEventListener('DOMContentLoaded', function() {
    const getMemoListButton = document.querySelector('#get-memo-list-btn');
    const memoList = document.querySelector('#memo-list');
    const loading = document.querySelector('.loading');

    getMemoListButton.addEventListener('click', function() {
        let csrfToken = getCsrfToken()

        fetch('/api/memos/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        }).then(response => response.json())
        .then(data => {
            data.forEach(data => {
                memoList.appendChild(createMemoElement(data));
            })
        })
    });
});