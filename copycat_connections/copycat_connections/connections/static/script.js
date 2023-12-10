selected = new Set();

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('submit-button').disabled = true;
    document.body.addEventListener('click', event => {
        const element = event.target;

        // Check if the user clicked on a shuffle button
        if (element.id === 'shuffle-button') {
            shuffleGrid();
        } else if (element.className === 'col-sm word-box') {   // check if user clicked on a word box
            select(element);
        } else if (element.className === 'col-sm word-box selected') {
            deselect(element);
        } else if (element.id === 'deselect-button') {
            deselectAll();
        } else if (element.id === 'deselect-button') {
            checkSubmission();
        }
    });
});

function shuffleGrid() {
    const container = document.getElementById('grid-container');
    const wordBoxes = Array.from(container.getElementsByClassName('word-box'));

    // Fisher-Yates shuffle algorithm
    for (let i = wordBoxes.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));  // Convert the 0 <= x < 1 return value to i's range
        const tmp = wordBoxes[i].innerHTML;
        wordBoxes[i].innerHTML = wordBoxes[j].innerHTML;
        wordBoxes[j].innerHTML = tmp;
    }
}


function select(element) {
    const MAX_WORDS_SELECTED = 4;

    if (selected.size < MAX_WORDS_SELECTED) {
        // Apply the selected class
        element.classList.add('selected');
        selected.add(element)
    }

    if (selected.size === MAX_WORDS_SELECTED) {
        // set submit button to active
        document.getElementById('submit-button').disabled = false;
    }
    // Do nothing if there are already four words selected
}

function deselect(element) {
    // If the word is currently selected
    if (selected.has(element)) {
        // Un-select the word and return
        element.classList.remove('selected');
        selected.delete(element);
    }
}

function deselectAll() {
    selected.forEach(function (element) {
        element.classList.remove('selected');
    })
    selected.clear();
}


function checkSubmission() {

}