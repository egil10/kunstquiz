let streak = 0;
let paintings = [];
let lastPaintingIndex = -1;

fetch('./data/paintings.json')
    .then(res => res.json())
    .then(data => {
        paintings = data;
        loadQuiz();
    });

function loadQuiz() {
    const painting = getRandomPainting();
    if (!painting) return;

    // Set painting image
    const img = document.getElementById('painting');
    img.src = painting.url;
    img.alt = painting.title;

    // Generate options
    const optionsDiv = document.getElementById('options');
    optionsDiv.innerHTML = '';

    const artists = generateOptions(painting.artist);
    artists.forEach(artist => {
        const btn = document.createElement('button');
        btn.textContent = artist;
        btn.className = '';
        btn.onclick = () => {
            // Disable all buttons
            Array.from(optionsDiv.children).forEach(b => b.disabled = true);
            // Find correct and selected buttons
            let correctBtn, selectedBtn;
            Array.from(optionsDiv.children).forEach(b => {
                if (b.textContent === painting.artist) correctBtn = b;
                if (b.textContent === artist) selectedBtn = b;
            });
            if (artist === painting.artist) {
                streak++;
                if (streak >= 10) {
                    updateStreakBar();
                    setTimeout(() => {
                        showCongratsModal();
                    }, 500);
                    return;
                }
                selectedBtn.classList.add('correct');
                showMessage('Riktig!', '#388e3c');
            } else {
                streak = 0;
                selectedBtn.classList.add('wrong');
                correctBtn.classList.add('correct');
                showMessage('Feil!', '#e53935');
            }
            updateStreakBar();
            setTimeout(() => {
                hideMessage();
                loadQuiz();
            }, 1000);
        };
        optionsDiv.appendChild(btn);
    });
    updateStreakBar();
}

function getRandomPainting() {
    if (paintings.length <= 1) return paintings[0];
    let idx;
    do {
        idx = Math.floor(Math.random() * paintings.length);
    } while (idx === lastPaintingIndex);
    lastPaintingIndex = idx;
    return paintings[idx];
}

function generateOptions(correct) {
    const set = new Set([correct]);
    while (set.size < 4) {
        const random = paintings[Math.floor(Math.random() * paintings.length)].artist;
        set.add(random);
    }
    return Array.from(set).sort(() => Math.random() - 0.5);
}

function updateStreakBar() {
    const streakBar = document.getElementById('streak-bar');
    streakBar.innerHTML = '';
    for (let i = 0; i < 10; i++) {
        const circle = document.createElement('div');
        circle.className = 'streak-circle' + (i < streak ? ' filled' : '');
        streakBar.appendChild(circle);
    }
}

function showMessage(text, color) {
    const msg = document.getElementById('message');
    msg.textContent = text;
    msg.style.color = color;
    msg.classList.add('visible');
}

function hideMessage() {
    const msg = document.getElementById('message');
    msg.classList.remove('visible');
}

function showCongratsModal() {
    document.getElementById('congrats-modal').style.display = 'flex';
}
function hideCongratsModal() {
    document.getElementById('congrats-modal').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    const resetBtn = document.getElementById('reset-btn');
    if (resetBtn) {
        resetBtn.onclick = function() {
            streak = 0;
            updateStreakBar();
            hideCongratsModal();
            loadQuiz();
        };
    }
});
