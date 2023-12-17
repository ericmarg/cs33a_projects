const WORDS_PER_ROW = 4;
const ROWS_PER_PUZZLE = 4;
let selected = new Set();
let rowsCompleted = new Set();
let usedWordBoxes = new Set();
let puzzle = undefined;
let puzzleNumber = undefined;


loadPuzzle();
document.addEventListener('DOMContentLoaded', function () {
    shuffleGrid();
    if (document.getElementById('submit-button')) document.getElementById('submit-button').disabled = true;
    document.body.addEventListener('click', event => {

        const element = event.target;
        // Add functionality to user clicks
        if (element.id === 'shuffle-button') {
            shuffleGrid();
        } else if (element.className === 'col-sm word-box') {
            select(element);
        } else if (element.className === 'col-sm word-box selected') {
            deselect(element);
        } else if (element.id === 'deselect-button') {
            deselectAll();
        } else if (element.id === 'submit-button') {
            checkSubmission();
        }
    });
});

function shuffleGrid() {
    const rows = document.querySelectorAll('.grid-row');
    let wordBoxes = Array.from(document.querySelectorAll('.word-box'));
    // Take the set difference (source: https://stackoverflow.com/questions/1723168/what-is-the-fastest-or-most-elegant-way-to-compute-a-set-difference-using-javasc)
    let remainingWordBoxes = [...wordBoxes].filter(x => !usedWordBoxes.has(x));

    // Shuffle remaining words
    fisherYatesShuffle(remainingWordBoxes);

    // Order the word boxes in the rows
    // Completed rows are filled with their words and the remaining rows are filled with shuffled words
    let arr = undefined
    let arrayUsedWordBoxes = [...usedWordBoxes]
    for (let i = 0; i < rows.length; ++i) {
        if (i < rowsCompleted.size) {
            arr = arrayUsedWordBoxes.slice(0, WORDS_PER_ROW);
            arrayUsedWordBoxes = arrayUsedWordBoxes.slice(WORDS_PER_ROW);
        } else {
            arr = remainingWordBoxes.slice(0, WORDS_PER_ROW);
            remainingWordBoxes = remainingWordBoxes.slice(WORDS_PER_ROW);
        }

        rows[i].replaceChildren('')
        arr.forEach(word => {
            rows[i].appendChild(word);
        })
    }
}

// Fisher-Yates shuffle algorithm
function fisherYatesShuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

function select(element) {
    const MAX_WORDS_SELECTED = 4;

    if (selected.size < MAX_WORDS_SELECTED) {
        // Apply the selected class
        element.classList.add('selected');
        selected.add(element);
    }

    if (selected.size === MAX_WORDS_SELECTED) {
        // set submit button to active
        document.getElementById('submit-button').disabled = false;
        document.getElementById('submit-button').style.color = 'white';
        document.getElementById('submit-button').style.backgroundColor = 'black';
    }
    // Do nothing if there are already four words selected
}

function deselect(element) {
    // If the word is currently selected
    if (selected.has(element)) {
        // De-select the word
        element.classList.remove('selected');
        selected.delete(element);
        // Disable the submit button
        document.getElementById('submit-button').disabled = true;
    }
}

function deselectAll() {
    selected.forEach(function (element) {
        // Remove class selected from each selected item's class list
        element.classList.remove('selected');
    })
    selected.clear();
    document.getElementById('submit-button').disabled = true;
}


function revealPuzzle() {
    for (let [rowNumber, rowContent] of Object.entries(puzzle)) {
        // Iterate through the puzzle entries and reveal each row
        revealRow(rowNumber, rowContent);
        rowsCompleted.add(rowNumber);
    }
}

// Function to check if two sets are equal
function isEqualSets(set1, set2) {
    if (set1.size !== set2.size) {
        return false;
    }

    for (const element of set1) {
        if (!set2.has(element)) {
            return false;
        }
    }

    return true;
}

function checkSubmission() {
    // Get the words from the selected wordBoxes and put them into a set for checking equality
    const guessedWords = new Set([...selected].map(element => element.innerHTML.trim()));
    let isEqual = false;

    for (let [rowNumber, rowContent] of Object.entries(puzzle)) {
        // Convert the only value in the rowContent object to a set for easy comparison
        const rowWords = new Set(Object.values(rowContent)[0]);
        // Check if the sets of words are the same
        if (isEqualSets(rowWords, guessedWords)) {
            isEqual = true;
            // Copy set values over
            selected.forEach(word => {
                usedWordBoxes.add(word);
            });
            // Reveal the row, deselect all boxes, and shuffle the grid so only non-used words appear
            revealRow(rowNumber, rowContent);
            deselectAll();
            rowsCompleted.add(rowNumber);
            shuffleGrid();
        }
    }

    if (!isEqual) {
        // The submission was not correct
        deselectAll();
        // Remove one of the 'mistakes remaining' bullets
        let bullets = document.getElementById('mistakes-bullet');
        bullets.innerHTML = bullets.innerHTML.slice(0, -2); // Remove bullet and whitespace character

        if (bullets.innerHTML.length === 0) {
            // Game over
            revealPuzzle();
        }
    }

    if (rowsCompleted.size === ROWS_PER_PUZZLE) {
        markPuzzleSolved(puzzleNumber);
    }
}

function revealRow(rowNumber, content) {
    // Remove non-digit characters from the string and convert to an int
    rowNumber = parseInt(rowNumber.replace(/\D/g, ''));
    const gridContainer = document.getElementById('grid-container');
    const rows = document.querySelectorAll('.grid-row');

    // Get the row element to apply the overlay to
    const targetRow = rows[rowsCompleted.size];
    // Get the position of the target word boxes relative to the viewport
    const wordBoxLeft = targetRow.children[0].getBoundingClientRect();
    const wordBoxRight = targetRow.children[WORDS_PER_ROW - 1].getBoundingClientRect();

    // Create the overlay banner and apply classes for style
    const revealBanner = document.createElement('div');
    revealBanner.className = 'row grid-overlay';
    revealBanner.id = `row-${rowNumber}-revealed`;

    // Set the position and size of the overlay based on the target position
    revealBanner.style.top = `${wordBoxLeft.top}px`;
    revealBanner.style.left = `${wordBoxLeft.left}px`;
    revealBanner.style.height = `${wordBoxLeft.height}px`;
    revealBanner.style.width = `${wordBoxRight.right - wordBoxLeft.left}px`;

    // Create elements for connection text
    const key = Object.keys(content)[0];
    const words = content[key];
    const overlayP = document.createElement('p');
    const span = document.createElement('span');

    // Display the connection and the related words, create a paragraph element, adjust style
    span.innerHTML = key;
    overlayP.appendChild(span);
    overlayP.appendChild(document.createElement('br'));
    overlayP.innerHTML += words;
    overlayP.style.textTransform = 'uppercase';
    overlayP.style.fontWeight = 'bold';

    revealBanner.appendChild(overlayP);

    // Append the overlay banner to the grid container
    gridContainer.appendChild(revealBanner);
}


function markPuzzleSolved(number) {
    fetch('/mark_puzzle_solved', {
        method: 'POST', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify({number: number}),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function loadPuzzle() {
    if (window.location.href.includes('/play')) {
        fetch(window.location.href, {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                puzzle = data[0];
                puzzleNumber = data[1];
            }).catch(error => {
            console.log('Error:', error);
        });
    }
}