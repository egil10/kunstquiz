let streak = 0;
let paintings = [];

fetch('./data/paintings.json')
    .then(response => {
        if (!response.ok) throw new Error('Failed to load paintings.json: ' + response.status);
        return response.json();
    })
    .then(data => {
        paintings = data;
        console.log('Paintings loaded:', paintings);
        if (!paintings.length) throw new Error('No paintings in JSON');
        loadQuiz(); // Force execution
    })
    .catch(error => {
        console.error('Fetch error:', error);
        alert('Error loading paintings: ' + error.message);
    });

function loadQuiz() {
    console.log('Loading quiz with paintings:', paintings); // Debug start
    if (!paintings.length) {
        console.error('No paintings to display');
        return;
    }
    const randomIndex = Math.floor(Math.random() * paintings.length);
    const correctPainting = paintings[randomIndex];
    const img = document.getElementById('painting');
    img.src = correctPainting.url;
    img.alt = correctPainting.title;
    console.log('Setting image src to:', img.src); // Debug image set
    img.onload = () => console.log('Image loaded:', correctPainting.url);
    img.onerror = () => console.error('Image load failed:', correctPainting.url);

    const artists = [correctPainting.artist];
    while (artists.length < 4) {
        const randomArtist = paintings[Math.floor(Math.random() * paintings.length)].artist;
        if (!artists.includes(randomArtist)) artists.push(randomArtist);
    }
    artists.sort(() => Math.random() - 0.5);

    const optionsDiv = document.getElementById('options');
    optionsDiv.innerHTML = '';
    console.log('Generating buttons for artists:', artists); // Debug buttons
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