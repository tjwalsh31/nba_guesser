const startButton = document.querySelector('#start-game');
const gameForm = document.querySelector('#game-form');
const playerInput = document.querySelector("#player");
const submitButton = document.querySelector("button[type='submit']");

async function startGame() {
    playerInput.disabled = false;
    submitButton.disabled = false;

    const response = await fetch('/start_game', {
        method: 'POST'
    });

    const data = await response.json();
    console.log('Game started:', data);
}

startButton.addEventListener('click', startGame);

async function getGameData() {
    const response = await fetch ("/get_game_data");

    const guess = await response.json();
    console.log(guess)
    displayGuess(guess);
}

function resultClass(value) {
    if (value.startsWith('✓')) return 'match';
    if (value.startsWith('~')) return 'close-match';
    return 'no-match';
}

function addResultCell(row, value) {
    const cell = row.insertCell();
    cell.textContent = value;
    cell.className = resultClass(value);
}

function displayGuess(guess) {
    const tableBody = document.getElementById('results').getElementsByTagName('tbody')[0];
    const newRow = tableBody.insertRow(-1);
    newRow.insertCell(0).textContent = guess.name;
    addResultCell(newRow, guess.team);
    addResultCell(newRow, guess.division);
    addResultCell(newRow, guess.conference);
    addResultCell(newRow, guess.position);
    addResultCell(newRow, guess.height);
    addResultCell(newRow, guess.age);
    addResultCell(newRow, guess.jersey);

}

gameForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    await fetch('/guess', {
        method: 'POST',
        body: new URLSearchParams({player: playerInput.value})
    });
    await getGameData();
    playerInput.value = '';
});

// submitButton.addEventListener('click', async (event) => {
//     event.preventDefault();

//     const guess = playerInput.value;

//     const response = await fetch("/process_guess", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify({
//             player: guess 
//         })
//     });


//     const data = await response.json();
//     console.log()

//     result.textContent = data.result;
// });