document.addEventListener('DOMContentLoaded', function () {
    initializeContentToggle();
    initializeDeleteButtons();
    initalizeSelectionModal();
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

function initializeDeleteButtons() {
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach((deleteButton) => {
        deleteButton.addEventListener('click', async function (event) {
            const id = deleteButton.dataset.id;
            const confirmation = confirm("削除しますか？");
            if (!confirmation) {
                event.preventDefault();
            }

            try {
                await deleteSelection(id);
                
                // selectionの削除処理
                const panelId = deleteButton.dataset.panelId;
                const panel = document.getElementById(panelId);
                panel.remove();
            } catch (e) {
                alert("削除に失敗しました。")
            }
        });
    });
}

function initalizeSelectionModal() {
    console.log('initalizeSelectionModal')
    const aiSelectionOpenBtn = document.getElementById('ai-selection-open');
    const aiSelectionCloseBtn = document.getElementById('ai-selection-close');
    const aiSelectionModal = document.getElementById('ai-selection-modal');
    const selectionCreateBtn = document.getElementById('selection-create-btn');

    aiSelectionOpenBtn.addEventListener('click', function () {
        aiSelectionModal.style.display = 'block';
    });
    
    aiSelectionCloseBtn.addEventListener('click', function () {
        aiSelectionModal.style.display = 'none';
    });

    selectionCreateBtn.addEventListener('click', async function () {
        // disable buttonの場合は処理を中断
        if (selectionCreateBtn.disabled) {
            console.log("disabled")
            return;
        }

        const demandInput = document.getElementById('selection-demand');

        try {
            const demand = demandInput.value;

            if (demand === '' || demand.length < 10) {
                alert('要望は10文字以上入力してください。');
                return;
            }

            selectionCreateBtn.disabled = true;

            const result = await createSelectionByAi(demand);

            location.replace(`/selection/${result.id}/`)
        } catch (e) {
            alert('オススメの書籍が見つかりませんでした。');
        } finally {
            selectionCreateBtn.disabled = false;
        }
    });
}