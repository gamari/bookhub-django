document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.memo-item-delete-button').forEach(function (button) {
        button.addEventListener('click', function () {
            const memoId = this.dataset.memoId;
            const actionUrl = this.dataset.action; // data-action属性からURLを取得

            fetch(actionUrl, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.result === 'success') {
                        // 削除に成功した場合、DOMから該当メモを削除する
                        button.closest('.memo-item').remove();
                    } else {
                        // エラーハンドリング
                        console.error('Failed to delete memo');
                    }
                })
                .catch(error => {
                    // ネットワークエラーやサーバーエラーのハンドリング
                    console.error('Error:', error);
                });
        });
    });
});

// DjangoのCSRFトークンを取得する関数
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
