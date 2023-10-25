document.addEventListener('DOMContentLoaded', function () {
    initializeContentToggle();
    initializeForms();
});

function initializeContentToggle() {
    const btnBookshelf = document.getElementById('btn-bookshelf');
    const btnReviews = document.getElementById('btn-reviews');
    const btnSelection = document.getElementById('btn-selection');
    const btnTimeline = document.getElementById('btn-timeline');
    
    const sectionBookshelf = document.getElementById('bookshelf-section');
    const sectionReviews = document.getElementById('reviews-section');
    const sectionSelection = document.getElementById('selection-section');
    const sectionTimeline = document.getElementById('timeline-section');

    btnTimeline.addEventListener('click', function () {
        reset();
        sectionTimeline.style.display = 'block';
        btnTimeline.classList.add('badge-info');
    });


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
        sectionTimeline.style.display = 'none';
        btnBookshelf.classList.remove('badge-info');
        btnReviews.classList.remove('badge-info');
        btnSelection.classList.remove('badge-info');
        btnTimeline.classList.remove('badge-info');
    }
}

function initializeForms() {
    const deleteForms = document.querySelectorAll('.delete-form');
    deleteForms.forEach(deleteForm => {
        deleteForm.addEventListener('submit', function (event) {
            console.log("SUBMIT")
            const confirmation = confirm("削除しますか？");
            if (!confirmation) {
                event.preventDefault();
            }
        });
    });
}