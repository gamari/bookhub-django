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


function createMemoElement(data) {
    let memoList = document.querySelector("#memoList");
    let newMemo = document.createElement('li');
    newMemo.classList.add('memo-item');
    newMemo.innerHTML = `<p>${data.created_at}</p><p>${data.content}</p>`;
    memoList.prepend(newMemo);

    // 削除ボタンの追加
    let deleteButton = document.createElement('button');
    deleteButton.classList.add('memo-item-delete-button');
    deleteButton.dataset.memoId = data.id;
    deleteButton.dataset.action = `/api/memos/${data.id}/`;
    let deleteIcon = document.createElement('i');
    deleteIcon.classList.add('fa-regular', 'fa-trash-can');
    deleteIcon.style.color = '#160160160';
    deleteButton.appendChild(deleteIcon);
    newMemo.appendChild(deleteButton);
    deleteButton.addEventListener('click', function (event) {
        deleteListener(deleteButton);
    });
}


// リスナー設定
document.addEventListener('DOMContentLoaded', function () {
    // メモフォームを設定
    let memoForm = document.querySelector("#memoForm");
    let createMemoButton = document.querySelector("#createMemoButton");

    createMemoButton.addEventListener("click", function (event) {
        event.preventDefault();
        let formData = new FormData(memoForm);

        if (formData.get('content') === '') {
            alert("メモの内容を入力してください。");
            return;
        }

        for (let [key, value] of formData.entries()) {
            console.log(key, value);
        }

        let postUrl = memoForm.dataset.action;

        createMemo(
            postUrl,
            formData,
            document.querySelector("[name=csrfmiddlewaretoken]").value
        ).then(data => {
            createMemoElement(data);

            let memoContent = document.querySelector("#id_content");
            memoContent.value = '';

            let noMemoTitle = document.querySelector("#no-memo-title");
            if (noMemoTitle) {
                noMemoTitle.remove();
            }
        });
    });


    // 削除ボタンのイベントリスナーを登録
    document.querySelectorAll('.memo-item-delete-button').forEach(function (button) {
        button.addEventListener('click', function (event) {
            deleteListener(button);
        });
    });
});