document.addEventListener('DOMContentLoaded', function() {
    const btnReviews = document.getElementById('btn-reviews');
    const btnTimeline = document.getElementById('btn-timeline');
    const btnBookDetail = document.getElementById('btn-book-detail');
    
    const sectionReviews = document.getElementById('reviews-section');
    const sectionTimeline = document.getElementById('timeline-section');
    const sectionBookDetail = document.getElementById('book-detail-section');

    let timelinePage = 1;

    btnReviews.addEventListener('click', function () {
        reset();
        sectionReviews.style.display = 'block';
        btnReviews.classList.add('badge-info');
    });

    btnTimeline.addEventListener('click', function () {
        reset();
        sectionTimeline.style.display = 'block';
        btnTimeline.classList.add('badge-info');
    });

    btnBookDetail.addEventListener('click', function () {
        reset();
        sectionBookDetail.style.display = 'block';
        btnBookDetail.classList.add('badge-info');
    });

    function reset() {
        sectionReviews.style.display = 'none';
        sectionTimeline.style.display = 'none';
        sectionBookDetail.style.display = 'none';
        btnReviews.classList.remove('badge-info');
        btnTimeline.classList.remove('badge-info');
        btnBookDetail.classList.remove('badge-info');
    }
});