function updateActionURL() {
    const searchType = document.getElementById("searchType").value;
    const form = document.querySelector(".search-container");
    const bookUrl = form.getAttribute('data-book-url');
    const authorUrl = form.getAttribute('data-author-url');

    console.log(searchType)
    console.log(bookUrl)
    
    if (searchType === "book_name") {
        form.action = bookUrl;
    } else if (searchType === "author_name") {
        form.action = authorUrl;
    }
}
