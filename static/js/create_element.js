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
