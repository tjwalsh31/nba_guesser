const startButton = document.querySelector('#start-game');
const playerInput = document.querySelector("#player");
const submitButton = document.querySelector("button[type='submit']");
const result = document.querySelector("#result");

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