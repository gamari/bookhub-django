document.addEventListener('DOMContentLoaded', function() {
    const getMemoListButton = document.querySelector('#get-memo-list-btn');
    const memoList = document.querySelector('#memo-list');
    const loading = document.querySelector('.loading');

    getMemoListButton.addEventListener('click', function() {
        let csrfToken = getCsrfToken()
        getMemoListButton.style.display = 'none';
        fetch('/api/memos/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        }).then(response => response.json())
        .then(data => {
            getMemoListButton.style.display = 'block';
            data.forEach(data => {
                memoList.appendChild(createMemoElement(data));
            })
        })
    });
});