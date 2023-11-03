document.addEventListener('DOMContentLoaded', function() {
    var filterInput = document.getElementById('book-filter');
    var books = document.querySelectorAll('.book');

  
    function filterBooks() {
      var searchText = filterInput.value;
  
      books.forEach(function(book) {
        var title = book.getAttribute('data-title');
        var status = book.getAttribute('data-status');

        if (!title) return;

        const matched = title.includes(searchText);
  
        if (searchText === '' || matched) {
          book.style.display = '';
        } else {
          book.style.display = 'none';
        }
      });
    }
  
    filterInput.addEventListener('input', filterBooks);
  });