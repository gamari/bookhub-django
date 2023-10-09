document.addEventListener('DOMContentLoaded', function () {
    const btnBookshelf = document.getElementById('btn-bookshelf');
    const btnReviews = document.getElementById('btn-reviews');
    const sectionBookshelf = document.getElementById('bookshelf-section');
    const sectionReviews = document.getElementById('reviews-section');

    btnBookshelf.addEventListener('click', function () {
        sectionBookshelf.style.display = 'block';
        sectionReviews.style.display = 'none';
        btnBookshelf.classList.add('badge-info');
        btnReviews.classList.remove('badge-info');
    });

    btnReviews.addEventListener('click', function () {
        sectionBookshelf.style.display = 'none';
        sectionReviews.style.display = 'block';
        btnBookshelf.classList.remove('badge-info');
        btnReviews.classList.add('badge-info');
    });
});