function createElement(tag, options = {}) {
    const el = document.createElement(tag);
    if (options.classes) el.classList.add(...options.classes);
    if (options.content) el.textContent = options.content;
    if (options.attributes) {
        for (const [key, value] of Object.entries(options.attributes)) {
            el.setAttribute(key, value);
        }
    }
    return el;
}

function createDeleteButton(data, classes = "") {
    const deleteIcon = createElement('i', {
        classes: ['fa-regular', 'fa-trash-can', 'fa-xl'],
        attributes: { style: 'color: #666' }
    });

    const deleteButton = createElement('button', {
        classes: [classes],
        attributes: {
            dataset: {
                memoId: data.id,
                action: `/api/memos/${data.id}/`
            }
        }
    });
    deleteButton.appendChild(deleteIcon);
    deleteButton.addEventListener('click', function () {
        deleteListener(deleteButton);
    });
    return deleteButton;
}

function createIconOrImage(source, alt, classes, isIcon = false) {
    if (isIcon) {
        return createElement('i', {
            classes: [...classes, 'fa-xl'],
            attributes: { style: `color: ${alt}` }
        });
    } else {
        return createElement('img', {
            classes,
            attributes: { src: source, alt: alt }
        });
    }
}

function createUserIcon(user) {
    const iconOrImage = user.profile_image ?
        createIconOrImage(user.profile_image, user.username, ['user-icon-sm', 'user-icon']) :
        createIconOrImage(null, '#888', ['fa-regular', 'fa-face-smile'], true);
    const userIcon = createElement('a', {
        classes: ['user-icon-sm', 'user-icon'],
        attributes: { href: `/user/${user.username}/` }
    })
    userIcon.appendChild(iconOrImage);
    return userIcon;
}

function createBookIcon(book) {
    const imgSource = book.thumbnail || 'https://via.placeholder.com/60x80';
    const bookImage = createIconOrImage(imgSource, book.title, ['book-image-sm', 'book-image']);
    return createElement('a', {
        classes: ['book-icon-sm', 'book-icon'],
        attributes: { href: `/book/${book.id}/` }
    }).appendChild(bookImage);
}

function createMemoElement(data) {
    
    const memoHeader = createElement('div', { classes: ['memo-item__header'] });
    const memoImage = createElement('div', { classes: ['memo-item__image'] });
    const memoInfo = createElement('div', { classes: ['memo-item__info'] });
    const memoTool = createElement('div', { classes: ['memo-item__tool'] });
    memoTool.appendChild(createDeleteButton(data, "memo-item__delete"));
    
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
    const timeData = data.created_at
    const formattedTime = timeData.replace(/年|月/g, '/').replace('日', ' ');
    const time = createElement("p", {classes: ['time'], content: formattedTime})
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