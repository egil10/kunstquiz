let streak = 0;
let paintings = [];

fetch('../data/paintings.json')
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
        console.error('Error:', error);
        alert('Error loading paintings: ' + error.message);
    });

function loadQuiz() {
    const randomIndex = Math.floor(Math.random() * paintings.length);
    const correctPainting = paintings[randomIndex];
    document.getElementById('painting').src = correctPainting.url;

    const artists = [correctPainting.artist];
    while (artists.length < 4) {
        const randomArtist = paintings[Math.floor(Math.random() * paintings.length)].artist;
        if (!artists.includes(randomArtist)) artists.push(randomArtist);
    }
    artists.sort(() => Math.random() - 0.5);

    const optionsDiv = document.getElementById('options');
    optionsDiv.innerHTML = '';
    artists.forEach(artist => {
        const button = document.createElement('button');
        button.textContent = artist;
        button.onclick = () => {
            if (artist === correctPainting.artist) {
                streak++;
                alert('Correct! It\'s ' + correctPainting.title + ' by ' + artist);
            } else {
                streak = 0;
                alert('Wrong! It\'s ' + correctPainting.title + ' by ' + correctPainting.artist);
            }
            document.getElementById('streak').textContent = 'Streak: ' + streak;
            loadQuiz();
        };
        optionsDiv.appendChild(button);
    });
}