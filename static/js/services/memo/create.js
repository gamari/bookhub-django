async function createMemo(url, body_data, csrf_token) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token
        },
        body: body_data
    });

    const data = await response.json();

    if (data.result === 'success') {
        return data;
    } else {
        alert("メモ作成に失敗しました。");
        throw new Error("メモ作成に失敗しました。");
    }
}

function createDeleteButton(data) {
    let deleteButton = document.createElement('button');
    deleteButton.classList.add('memo-item-delete-button');
    deleteButton.dataset.memoId = data.id;
    deleteButton.dataset.action = `/api/memos/${data.id}/`;
    let deleteIcon = document.createElement('i');
    deleteIcon.classList.add('fa-regular', 'fa-trash-can', 'fa-xl');
    deleteIcon.style.color = '#666';
    deleteButton.appendChild(deleteIcon);
    deleteButton.addEventListener('click', function () {
        deleteListener(deleteButton);
    });
    return deleteButton;
}


function createUserIcon(user) {
    let userIcon = document.createElement('a');
    userIcon.href = `/user/${user.username}/`;
    userIcon.classList.add('user-icon-sm', 'user-icon');
    if (user.profile_image) {
        let img = document.createElement('img');
        img.src = user.profile_image;
        img.alt = user.username;
        userIcon.appendChild(img);
    } else {
        let icon = document.createElement('i');
        icon.classList.add('fa-regular', 'fa-face-smile', 'fa-xl');
        icon.style.color = '#888';
        userIcon.appendChild(icon);
    }

    return userIcon;
}

function createBookIcon(book) {
    let bookIcon = document.createElement('a');
    bookIcon.href = `/book/${book.id}/`;
    bookIcon.classList.add('book-icon-sm', 'book-icon');
    if (book.thumbnail) {
        let img = document.createElement('img');
        img.classList.add('book-image-sm', 'book-image');
        img.src = book.thumbnail;
        img.alt = book.title;
        bookIcon.appendChild(img);
    } else {
        let img = document.createElement('img');
        img.classList.add('book-image-sm', 'book-image');
        img.src = 'https://via.placeholder.com/60x80';
        img.alt = book.title;
        bookIcon.appendChild(img);
    }

    return bookIcon;
}

function createMemoElement(data) {
    // ユーザーサイド
    let memoUser = document.createElement("div");
    memoUser.classList.add('memo-user');
    let userIcon = createUserIcon(data.user);
    memoUser.appendChild(userIcon);
    let bookIcon = createBookIcon(data.book);
    memoUser.appendChild(bookIcon);
    
    // 情報サイド
    let memoInfo = document.createElement("div");
    memoInfo.classList.add('memo-info');
    let memoCreatedAt = document.createElement('p');
    memoCreatedAt.classList.add('memo-created-at');
    memoCreatedAt.textContent = data.created_at;
    memoInfo.appendChild(memoCreatedAt);
    let memoContent = document.createElement('p');
    memoContent.classList.add('memo-content');
    memoContent.textContent = data.content;
    memoInfo.appendChild(memoContent);

    // ツールサイド
    let memoTool = document.createElement("div");
    memoTool.classList.add('memo-tools');
    memoTool.appendChild(createDeleteButton(data));

    let newMemo = document.createElement('li');
    newMemo.classList.add('memo-item');
    newMemo.dataset.memoId = data.id;
    newMemo.appendChild(memoUser);
    newMemo.appendChild(memoInfo);
    newMemo.appendChild(memoTool);

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
});