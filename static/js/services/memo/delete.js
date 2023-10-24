// TODO 移動させる


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
        return data;
    } else {
        throw new Error("メモの削除に失敗しました。");
    }

}

function deleteListener(button) {
    const isOk = confirm('削除してもよろしいですか？');

    if (!isOk) return;

    const memoId = button.dataset.memoId;
    const actionUrl = button.dataset.action;

    deleteMemo(memoId, actionUrl).then(data => {
        button.closest('.memo-item').remove();
    });
}


document.addEventListener('DOMContentLoaded', function () {
    const deleteButtonList = document.querySelectorAll('.memo-item-delete-button')
    deleteButtonList.forEach(function (button) {
        button.addEventListener('click', function (event) {
            deleteListener(button);
        });
    });
});

