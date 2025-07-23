let streak = 0;
let paintings = []; // Will load from JSON

fetch('../data/paintings.json')
    .then(response => response.json())
    .then(data => {
        paintings = data;
        loadQuiz();
    });

function loadQuiz() {
    // Same logic as MVP, using paintings array
    // ...
}