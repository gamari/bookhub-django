document.addEventListener('DOMContentLoaded', function() {
    let buttons = document.querySelectorAll('.book-shelf-toggle');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            let bookId = button.getAttribute('data-book-id');
            let isRegistered = button.getAttribute('data-is-registered') === 'true';
            let url = `/api/bookshelf/books/${bookId}/`;
            let method = isRegistered ? 'DELETE' : 'POST';

            let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`${response.status} ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                isRegistered = !isRegistered;
                updateButton(button, isRegistered);
                button.setAttribute('data-is-registered', isRegistered);
            })
            .catch(error => {
                alert('本棚の登録に失敗しました。');
            });
        });
    });

    function updateButton(button, isRegistered) {
        if (isRegistered) {
            button.textContent = "本棚から削除";
            button.classList.remove('btn-primary');
        } else {
            button.textContent = "本棚に登録";
            button.classList.add('btn-primary');
        }
    }
});
