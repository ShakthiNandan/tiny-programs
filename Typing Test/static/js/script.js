// Initialize variables
let typedWord = '';
let currentWord = getRandomWord(); // Get the first random word
let score = 0;
let scoreDisplay = document.getElementById('score');
let pointsDisplay = document.getElementById('points-awarded'); // New element to show points

// Set the initial word
document.getElementById('word').textContent = currentWord;

// Function to get a random word from a list
function getRandomWord() {
    const words = [
        // Technology
        "algorithm", "hardware", "software", "internet", "debugging", "encryption", "network", "virtual", "coding", "framework",
    
        // Nature
        "butterfly", "rainforest", "volcano", "savanna", "tsunami", "wildlife", "ecosystem", "sunlight", "photosynthesis", "hurricane",
    
        // Space
        "galaxy", "asteroid", "meteor", "telescope", "nebula", "planetary", "cosmos", "orbit", "blackhole", "satellite",
    
        // Everyday
        "breakfast", "laptop", "backpack", "umbrella", "grocery", "calendar", "pencil", "notebook", "headphones", "keyboard",
    
        // Fantasy
        "wizard", "dragon", "sorcery", "castle", "unicorn", "spellbound", "elf", "dungeon", "quest", "mythical",
    
        // Science
        "molecule", "gravity", "nucleus", "bacteria", "chemistry", "biotechnology", "evolution", "physics", "microscope", "theorem",
    
        // Food
        "spaghetti", "sandwich", "pancake", "chocolate", "avocado", "sushi", "lasagna", "barbecue", "cuisine", "smoothie",
    
        // Sports
        "basketball", "cricket", "marathon", "tournament", "stadium", "fitness", "athlete", "swimming", "badminton", "victory",
    
        // Emotions
        "happiness", "sadness", "anxiety", "enthusiasm", "courage", "confusion", "relief", "joyful", "hopeful", "loneliness"
    ];
     return words[Math.floor(Math.random() * words.length)];
}

// Function to highlight typed letters on the word
function highlightTypedLetters() {
    let highlightedWord = '';
    for (let i = 0; i < currentWord.length; i++) {
        if (i < typedWord.length) {
            if (currentWord[i] === typedWord[i]) {
                highlightedWord += `<span class="highlighted">${currentWord[i]}</span>`; // Correct letter
            } else {
                highlightedWord += `<span class="wrong">${currentWord[i]}</span>`; // Incorrect letter
            }
        } else {
            highlightedWord += currentWord[i];
        }
    }
    document.getElementById('word').innerHTML = highlightedWord;
}

// Function to highlight the pressed key on the on-screen keyboard
function highlightKey(key, isCorrect) {
    const keyButton = document.querySelector(`button[data-key='${key}']`);
    if (keyButton) {
        if (isCorrect) {
            keyButton.classList.add('highlighted');
            setTimeout(() => {
                keyButton.classList.remove('highlighted');
            }, 150); // Highlight duration (150ms)
        } else {
            keyButton.classList.add('highlighted-key');
            setTimeout(() => {
                keyButton.classList.remove('highlighted-key');
            }, 150); // Highlight incorrect key for a short time
        }
    }
}

// Function to handle key press events
document.addEventListener('keydown', function(event) {
    let key = event.key.toLowerCase();

    // If the key matches the first letter of the current word, update the typedWord
    if (key === currentWord[typedWord.length]) {
        typedWord += key;
        highlightTypedLetters();
        highlightKey(key, true); // Correct key press
    } else {
        // If there is a mistake, highlight the letter and key in red
        typedWord += key; // Proceed with the wrong letter
        highlightTypedLetters();
        highlightKey(key, false); // Incorrect key press

        // After a mistake, reset the word for the next try
        setTimeout(() => {
            typedWord = '';
            currentWord = getRandomWord();
            document.getElementById('word').textContent = currentWord;
            highlightTypedLetters();
        }, 1000); // Delay for 1 second before moving to the next word
    }

    // Check if the word is completely typed and correct
    if (typedWord === currentWord) {
        // Points based on the size of the word (e.g., 2 points per letter)
        let pointsForWord = currentWord.length * 2;
        pointsDisplay.textContent = `+${pointsForWord} points!`; // Show points awarded

        // Display points for a brief time before updating score
        setTimeout(() => {
            score += pointsForWord; // Add points for correctly typed word
            scoreDisplay.textContent = `Score: ${score}`; // Update the score
            typedWord = ''; // Reset typed word for the next word
            currentWord = getRandomWord(); // Get a new word
            document.getElementById('word').textContent = currentWord; // Update displayed word
            highlightTypedLetters(); // Update the word with highlighted letters
            pointsDisplay.textContent = ''; // Hide the points display
        }, 1000); // Delay for 1 second to show the points before resetting
    }
});

// Function to handle the on-screen keyboard clicks
document.querySelectorAll('.key').forEach(button => {
    button.addEventListener('click', function() {
        let key = this.textContent.toLowerCase();
        // Trigger the same logic as when a physical key is pressed
        if (key === currentWord[typedWord.length]) {
            typedWord += key;
            highlightTypedLetters();
            highlightKey(key, true); // Correct key press
        } else {
            typedWord += key; // Proceed with the wrong letter
            highlightTypedLetters();
            highlightKey(key, false); // Incorrect key press

            // After a mistake, reset the word for the next try
            setTimeout(() => {
                typedWord = '';
                currentWord = getRandomWord();
                document.getElementById('word').textContent = currentWord;
                highlightTypedLetters();
            }, 1000); // Delay for 1 second before moving to the next word
        }

        // Check if the word is completely typed and correct
        if (typedWord === currentWord) {
            // Points based on the size of the word (e.g., 2 points per letter)
            let pointsForWord = currentWord.length * 2;
            pointsDisplay.textContent = `+${pointsForWord} points!`; // Show points awarded

            // Display points for a brief time before updating score
            setTimeout(() => {
                score += pointsForWord; // Add points for correctly typed word
                scoreDisplay.textContent = `Score: ${score}`; // Update the score
                typedWord = ''; // Reset typed word for the next word
                currentWord = getRandomWord(); // Get a new word
                document.getElementById('word').textContent = currentWord; // Update displayed word
                highlightTypedLetters(); // Update the word with highlighted letters
                pointsDisplay.textContent = ''; // Hide the points display
            }, 100); // Delay for 1 second to show the points before resetting
        }
    });
});
