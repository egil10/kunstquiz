let streak = 0;
let paintings = [];
let lastPaintingIndex = -1;
let selectedCategory = 'all';

fetch('./data/paintings.json')
    .then(res => res.json())
    .then(data => {
        paintings = data;
        loadQuiz();
    });

function getValidPaintings() {
    // Only paintings with a valid artist and url, and matching the selected category
    let filtered = paintings.filter(p => p.artist && p.url);
    if (selectedCategory && selectedCategory !== 'all') {
        filtered = filtered.filter(p => Array.isArray(p.categories) && p.categories.includes(selectedCategory));
    }
    return filtered;
}

function loadQuiz() {
    const validPaintings = getValidPaintings();
    if (!validPaintings.length) {
        document.getElementById('options').innerHTML = '<p>Ingen gyldige malerier funnet.</p>';
        return;
    }
    let painting;
    // Try up to 10 times to get a valid painting
    for (let i = 0; i < 10; i++) {
        painting = getRandomPainting(validPaintings);
        if (painting && painting.artist && painting.url) break;
    }
    if (!painting || !painting.artist || !painting.url) return;

    // Set painting image
    const img = document.getElementById('painting');
    img.src = painting.url;
    img.alt = stripHtml(painting.title);

    // Generate options
    const optionsDiv = document.getElementById('options');
    optionsDiv.innerHTML = '';

    const artists = generateOptions(painting.artist, validPaintings);
    if (artists.length < 2) {
        optionsDiv.innerHTML = '<p>Ikke nok kunstnere for quiz.</p>';
        return;
    }
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
                    showArtistPopup(painting);
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
            showArtistPopup(painting);
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

function getRandomPainting(validPaintings) {
    if (!validPaintings || validPaintings.length <= 1) return validPaintings[0];
    let idx;
    do {
        idx = Math.floor(Math.random() * validPaintings.length);
    } while (idx === lastPaintingIndex);
    lastPaintingIndex = idx;
    return validPaintings[idx];
}

function generateOptions(correct, validPaintings) {
    // Get all unique artists in the dataset
    const uniqueArtists = Array.from(new Set(validPaintings.map(p => p.artist)));
    // If less than 4 unique artists, just use all of them
    if (uniqueArtists.length <= 4) {
        return uniqueArtists.sort(() => Math.random() - 0.5);
    }
    // Otherwise, pick 3 random others + correct
    const set = new Set([correct]);
    let safety = 0;
    while (set.size < 4 && safety < 20) {
        const random = uniqueArtists[Math.floor(Math.random() * uniqueArtists.length)];
        set.add(random);
        safety++;
    }
    return Array.from(set).sort(() => Math.random() - 0.5);
}

function stripHtml(html) {
    const div = document.createElement('div');
    div.innerHTML = html;
    return div.textContent || div.innerText || '';
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

// Artist info pop-up
function showArtistPopup(painting) {
    let popup = document.getElementById('artist-popup');
    if (!popup) {
        popup = document.createElement('div');
        popup.id = 'artist-popup';
        popup.className = 'artist-popup';
        document.body.appendChild(popup);
    }
    let imgHtml = '';
    if (painting.artist_image) {
        imgHtml = `<img src="${painting.artist_image}" alt="${painting.artist}" class="artist-portrait">`;
    }
    let bio = painting.artist_bio || '';
    let shortBio = bio.split('.').slice(0,2).join('.') + '.';
    popup.innerHTML = `
        <div class="artist-popup-content">
            ${imgHtml}
            <div class="artist-popup-text">
                <strong>${painting.artist}</strong><br>
                <span>${shortBio}</span>
            </div>
        </div>
    `;
    popup.style.display = 'block';
    setTimeout(() => { popup.style.opacity = 1; }, 10);
    setTimeout(() => {
        popup.style.opacity = 0;
        setTimeout(() => { popup.style.display = 'none'; }, 400);
    }, 2200);
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
    const catSelect = document.getElementById('category-select');
    if (catSelect) {
        catSelect.onchange = function() {
            selectedCategory = catSelect.value;
            streak = 0;
            updateStreakBar();
            loadQuiz();
        };
    }
});
