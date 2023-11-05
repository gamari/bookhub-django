document.addEventListener('DOMContentLoaded', function() {
    initializeSidebar();
});

function initializeSidebar() {
    const aiBtn = document.getElementById('ai-btn');
    const bookId = document.getElementById('book-id').value;
    const noteContent = document.getElementById('note-content');

    aiBtn.addEventListener('click', function () {
        console.log("click");
        fetch(`/api/ai/books/${bookId}/notes/`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            }
            // body: JSON.stringify({
            //     "title": "ai",
            //     "content": "ai"
            // })
        }).then(function (response) {
            return response.json();
        }).then(function (json) {
            console.log(json);
            console.log(noteContent)
            const content = json.content;
            if (content) {
                noteContent.value = noteContent.value + content;
            }
        });
    });
}