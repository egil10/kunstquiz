let streak = 0;
let paintings = [];

fetch('./data/paintings.json')
    .then(response => {
        if (!response.ok) throw new Error('Failed to load paintings.json: ' + response.status);
        return response.json();
    })
    .then(data => {
        paintings = data;
        if (!paintings.length) throw new Error('No paintings in JSON');
        loadQuiz();
    })
    .catch(error => {
        console.error('Fetch error:', error);
        alert('Error loading paintings: ' + error.message);
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
        btn.onclick = () => {
            if (artist === painting.artist) {
                streak++;
                alert(`✅ Correct!\n"${painting.title}" is by ${artist}.`);
            } else {
                streak = 0;
                alert(`❌ Wrong!\nIt was "${painting.title}" by ${painting.artist}.`);
            }
            document.getElementById('streak').textContent = 'Streak: ' + streak;
            loadQuiz(); // loop continues
        };
        optionsDiv.appendChild(btn);
    });
}

function getRandomPainting() {
    if (!paintings.length) return null;
    return paintings[Math.floor(Math.random() * paintings.length)];
}

function generateOptions(correctArtist) {
    const artistSet = new Set();
    artistSet.add(correctArtist);

    while (artistSet.size < 4) {
        const randomArtist = paintings[Math.floor(Math.random() * paintings.length)].artist;
        artistSet.add(randomArtist);
    }

    // Shuffle the options
    return Array.from(artistSet).sort(() => Math.random() - 0.5);
}
