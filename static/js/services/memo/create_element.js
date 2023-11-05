/** 削除ボタン */
function createDeleteButton(data, classes = "") {
    const deleteIcon = createElement('i', {
        classes: ['fa-regular', 'fa-trash-can', 'fa-xl'],
        attributes: { style: 'color: #666' }
    });

    const deleteButton = createElement('button', {
        classes: [classes],
        attributes: {
            "data-memo-id": data.id,
            "data-action": `/api/memos/${data.id}/`
        }
    });
    deleteButton.appendChild(deleteIcon);
    deleteButton.addEventListener('click', function () {
        deleteListener(deleteButton);
    });
    return deleteButton;
}


function createMemoElement(data, show_delete = true) {
    const memoHeader = createElement('div', { classes: ['memo-item__header'] });
    const memoImage = createElement('div', { classes: ['memo-item__image'] });
    const memoInfo = createElement('div', { classes: ['memo-item__info'] });
    const memoTool = createElement('div', { classes: ['memo-item__tool'] });

    if (show_delete) {
        memoTool.appendChild(createDeleteButton(data, "memo-item__delete"));
    }
    
    memoImage.append(createBookIcon(data.book));
    memoHeader.append(
        memoImage,
        memoInfo,
        memoTool
    )

    
    const tempDiv = createElement('div');
    const userName =createElement("div", {classes: ['user-name__md']})
    const userNameLink = createElement('a', {
        attributes: { href: `/user/${data.user.username}/` },
        content: data.user.username
    });
    userName.appendChild(userNameLink)
    const formattedDate = formatDateTime(data.created_at);
    const time = createElement("p", {classes: ['time'], content: formattedDate})
    tempDiv.append(userName, time)

    const userIcon = createUserIcon(data.user);
    
    const infoHeader = createElement('div', { classes: ['memo-item__info-header'] });
    infoHeader.append(userIcon, tempDiv);


    const bookTitleDiv = createElement('div');
    const bookTitleLink = createElement('a', {
        classes: ['text-sm'],
        attributes: { href: `/book/${data.book.id}/` },
        content: data.book.title
    });
    bookTitleDiv.appendChild(bookTitleLink);
    memoInfo.append(infoHeader, bookTitleDiv);


    // メモの作成
    const memoContent = createElement('p', { classes: ['memo-item__content'], content: data.content })
    const newMemo = createElement('li', { classes: ['memo-item'], attributes: { dataset: { memoId: data.id } } });
    newMemo.append(memoHeader, memoContent)

    return newMemo;
}