// TODO 移動させる
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

function deleteListener(button) {
    const isOk = confirm('メモを削除しますか？');

    if (!isOk) return;

    const memoId = button.dataset.memoId;
    const actionUrl = button.dataset.action;

    deleteMemo(memoId, actionUrl).then(data => {
        button.closest('.memo-item').remove();
    });
}

function createDeleteButton(data) {
    let deleteButton = document.createElement('button');
    deleteButton.classList.add('memo-item-delete-button');
    deleteButton.dataset.memoId = data.id;
    deleteButton.dataset.action = `/api/memos/${data.id}/`;
    let deleteIcon = document.createElement('i');
    deleteIcon.classList.add('fa-regular', 'fa-trash-can');
    deleteIcon.style.color = '#160160160';
    deleteButton.appendChild(deleteIcon);
    deleteButton.addEventListener('click', function () {
        deleteListener(deleteButton);
    });
    return deleteButton;
}


function createMemoElement(data) {
    let newMemo = document.createElement('li');
    newMemo.classList.add('memo-item');
    newMemo.innerHTML = `<p>${data.created_at}</p><p>${data.content}</p>`;
    newMemo.appendChild(createDeleteButton(data));
    return newMemo;
}


// リスナー設定
document.addEventListener('DOMContentLoaded', function () {
    const memoList = document.querySelector("#memoList");
    const memoForm = document.querySelector("#memoForm");
    const createMemoButton = document.querySelector("#createMemoButton");
    const memoContent = document.querySelector("#id_content");
    const noMemoTitle = document.querySelector("#no-memo-title");

    // フォーム設定
    createMemoButton.addEventListener("click", function (event) {
        event.preventDefault();
        let formData = new FormData(memoForm);

        if (formData.get('content') === '') {
            alert("メモの内容を入力してください。");
            return;
        }

        let postUrl = memoForm.dataset.action;

        createMemo(
            postUrl,
            formData,
            getCookie('csrfmiddlewaretoken')
        ).then(data => {
            memoList.prepend(createMemoElement(data));
            memoContent.value = '';
            if (noMemoTitle) noMemoTitle.remove();
        });
    });


    // 削除ボタン設定
    document.querySelectorAll('.memo-item-delete-button').forEach(function (button) {
        button.addEventListener('click', function (event) {
            deleteListener(button);
        });
    });
});