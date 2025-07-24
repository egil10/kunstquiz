let streak = 0;
let paintings = [];

fetch('./data/paintings.json')
    .then(res => res.json())
    .then(data => {
        paintings = data;
        loadQuiz();
    });

function loadQuiz() {
    const painting = getRandomPainting();
    const img = document.getElementById('painting');
    img.src = painting.url;
    img.alt = painting.title;

    const artists = generateOptions(painting.artist);
    const optionsDiv = document.getElementById('options');
    optionsDiv.innerHTML = '';

    artists.forEach(artist => {
        const button = document.createElement('button');
        button.textContent = artist;

        button.onclick = () => {
            const buttons = document.querySelectorAll('#options button');
            buttons.forEach(btn => {
                if (btn.textContent === painting.artist) {
                    btn.classList.add('correct');
                } else {
                    btn.classList.add('wrong');
                }
                btn.disabled = true;
            });

            if (artist === painting.artist) {
                streak++;
            } else {
                streak = 0;
            }

            updateStreakBar();

            setTimeout(() => {
                if (streak >= 10) {
                    alert("🏆 You're on fire! 10 in a row!");
                    streak = 0;
                    updateStreakBar();
                }
                loadQuiz();
            }, 1200);
        };

        optionsDiv.appendChild(button);
    });
}

function getRandomPainting() {
    return paintings[Math.floor(Math.random() * paintings.length)];
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
    const bar = document.getElementById('streak-bar');
    bar.innerHTML = '';
    for (let i = 0; i < 10; i++) {
        const box = document.createElement('div');
        box.className = 'streak-box' + (i < streak ? ' filled' : '');
        bar.appendChild(box);
    }
}
