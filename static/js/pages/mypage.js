document.addEventListener('DOMContentLoaded', function () {
    const btnBookshelf = document.getElementById('btn-bookshelf');
    const btnReviews = document.getElementById('btn-reviews');
    const sectionBookshelf = document.getElementById('bookshelf-section');
    const sectionReviews = document.getElementById('reviews-section');
    const btnSelection = document.getElementById('btn-selection');
    const sectionSelection = document.getElementById('selection-section');

    btnSelection.addEventListener('click', function () {
        reset();
        sectionSelection.style.display = 'block';
        btnSelection.classList.add('badge-info');
    });

    btnBookshelf.addEventListener('click', function () {
        reset();
        sectionBookshelf.style.display = 'block';
        btnBookshelf.classList.add('badge-info');
    });

    btnReviews.addEventListener('click', function () {
        reset();
        sectionReviews.style.display = 'block';
        btnReviews.classList.add('badge-info');
    });

    function reset() {
        sectionBookshelf.style.display = 'none';
        sectionReviews.style.display = 'none';
        sectionSelection.style.display = 'none';
        btnBookshelf.classList.remove('badge-info');
        btnReviews.classList.remove('badge-info');
        btnSelection.classList.remove('badge-info');
    }
});