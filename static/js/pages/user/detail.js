document.addEventListener('DOMContentLoaded', function() {
    initializeContentToggle();
    initializeOutput();
});

// 初期化処理
function initializeContentToggle() {
    const btnBookshelf = document.getElementById('btn-bookshelf');
    const btnOutput = document.getElementById('btn-output');

    const sectionBookshelf = document.getElementById('bookshelf-section');
    const sectionOutput = document.getElementById('output-section');

    btnBookshelf.addEventListener('click', function () {
        reset();
        sectionBookshelf.style.display = 'block';
        btnBookshelf.classList.add('badge-info');
    });

    btnOutput.addEventListener('click', function () {
        reset();
        sectionOutput.style.display = 'block';
        btnOutput.classList.add('badge-info');
    });


    function reset() {
        sectionBookshelf.style.display = 'none';
        btnBookshelf.classList.remove('badge-info');

        sectionOutput.style.display = 'none';
        btnOutput.classList.remove('badge-info');
    }
}

async function initializeOutput() {
    const getMemoListButton = document.querySelector('#get-memo-list-btn');
    const memoList = document.querySelector('#memo-list');
    let oldestDate = memoList.lastElementChild.dataset.date;
    const user_id = document.querySelector('#user_id').value;

    getMemoListButton.addEventListener('click', function () {
        getMemosByUserAndDate(user_id, oldestDate).then(json => {
            getMemoListButton.style.display = 'block';

            if (json.length === 0) {
                getMemoListButton.style.display = 'none';
                return;
            }

            json.forEach(data => {
                memoList.appendChild(createMemoElement(data));
            })

            const created_at = json[json.length - 1]['created_at']
            if (created_at) {
                oldestDate = created_at
            }
        })
    });
}