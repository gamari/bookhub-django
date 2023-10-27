document.addEventListener('DOMContentLoaded', function() {
    const getMemoListButton = document.querySelector('#get-memo-list-btn');
    const memoList = document.querySelector('#memo-list');
    const loading = document.querySelector('.loading');
    let oldestDate = undefined;

    function initialize() {
        // memoListの一番古い日付を残す
        console.log(memoList.lastElementChild)
        oldestDate = memoList.lastElementChild.dataset.date;
    }

    getMemoListButton.addEventListener('click', function() {
        let csrfToken = getCsrfToken();
        let apiUrl = '/api/memos/';
        getMemoListButton.style.display = 'none';

        console.log(oldestDate);

        if (oldestDate) {
            apiUrl += `?previous_date=${oldestDate}`;
        }


        fetch(apiUrl, {
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
            // TODO エラー出るので修正する
            const created_at  = data[data.length - 1]['created_at']
            if (created_at) {
                oldestDate = created_at
            }
        })
    });

    initialize();
});