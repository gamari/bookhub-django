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

document.addEventListener('DOMContentLoaded', function () {
    // 削除ボタンのイベントリスナーを登録
    document.querySelectorAll('.memo-item-delete-button').forEach(function (button) {
        button.addEventListener('click', function () {
            const isOk = confirm('メモを削除しますか？');

            if (!isOk) return;

            const memoId = this.dataset.memoId;
            const actionUrl = this.dataset.action;

            deleteMemo(memoId, actionUrl).then(data => {
                button.closest('.memo-item').remove();
            });
        });
    });
});