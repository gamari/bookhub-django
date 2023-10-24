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

function createDeleteButton(data, classes="") {
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
    console.log(data);
    const memoImage = createElement('div', { classes: ['memo-item__image'] });
    memoImage.append(createBookIcon(data.book));

    const memoInfo = createElement('div', { classes: ['memo-item__info'] });
    const memoInfoHeader = createElement('div', { classes: ['memo-item__info-header'] });
    const headerInfo = createElement('div', { classes: ['memo-item__header-info'] });
    headerInfo.append(
        createElement('p', { classes: ['memo-item__info-username'], content: data.user.username }),
        createElement('p', { classes: ['memo-item__info-time'], content: data.created_at })
    );
    const userIcon = createUserIcon(data.user);
    console.log(userIcon);
    memoInfoHeader.append(
        userIcon, 
        headerInfo
    );

    memoInfo.append(
        memoInfoHeader,
        createElement('p', { classes: ['memo-item__content'], content: data.content })
    );

    const memoTool = createElement('div', { classes: ['memo-item__tool'] });
    memoTool.appendChild(createDeleteButton(data, "memo-item__delete"));

    const newMemo = createElement('li', { classes: ['memo-item'], attributes: { dataset: { memoId: data.id } } });
    newMemo.append(memoImage, memoInfo, memoTool);

    return newMemo;
}