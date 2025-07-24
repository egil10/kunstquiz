let streak = 0;
let paintings = [];
let lastPaintingIndex = -1;
let selectedCategory = 'all';

function getYearOnly(dateStr) {
    if (!dateStr) return '';
    const match = dateStr.match(/\d{4}/);
    return match ? match[0] : '';
}

function getCategoryCounts() {
    const counts = {};
    const painterSets = {};
    paintings.forEach(p => {
        if (Array.isArray(p.categories)) {
            p.categories.forEach(cat => {
                counts[cat] = (counts[cat] || 0) + 1;
                if (!painterSets[cat]) painterSets[cat] = new Set();
                if (p.artist) painterSets[cat].add(p.artist);
            });
        }
    });
    // For full collection
    painterSets['all'] = new Set(paintings.map(p => p.artist));
    counts['all'] = paintings.length;
    return { counts, painterSets };
}

function updateCollectionInfo() {
    const catSelect = document.getElementById('category-select');
    const infoBar = document.getElementById('collection-info');
    if (!catSelect || !infoBar) return;
    const { counts, painterSets } = getCategoryCounts();
    const selected = catSelect.value || 'all';
    const count = counts[selected] || 0;
    const painterCount = painterSets[selected] ? painterSets[selected].size : 0;
    infoBar.textContent = `${count} paintings, ${painterCount} painters`;
}

function updateCategoryDropdown() {
    const catSelect = document.getElementById('category-select');
    if (!catSelect) return;
    const { counts, painterSets } = getCategoryCounts();
    // Get all categories except 'all', sort alphabetically
    const sortedCats = Object.keys(counts)
        .filter(cat => cat !== 'all')
        .sort((a, b) => a.localeCompare(b));
    // Always include 'all' as first option
    const options = [
        { value: 'all', label: 'Full collection' },
        ...sortedCats.map(cat => ({ value: cat, label: cat }))
    ];
    // Rebuild dropdown
    catSelect.innerHTML = '';
    options.forEach(opt => {
        const option = document.createElement('option');
        option.value = opt.value;
        option.textContent = opt.label;
        catSelect.appendChild(option);
    });
    updateCollectionInfo();
}

// Update info bar on category change
function setupCategoryChangeInfoBar() {
    const catSelect = document.getElementById('category-select');
    if (catSelect) {
        catSelect.onchange = function() {
            selectedCategory = catSelect.value;
            streak = 0;
            updateStreakBar();
            updateCollectionInfo();
            loadQuiz();
        };
    }
}

// Use the merged data file
fetch('./data/paintings_merged.json')
    .then(res => res.json())
    .then(data => {
        paintings = data;
        updateCategoryDropdown();
        updateCollectionInfo();
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
            }, 2500);
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

function cleanWorkTitle(title) {
    // Remove label QS:... and HTML tags
    if (!title) return '';
    return title.replace(/label QS:[^\s,]+,[^\n"]+"/g, '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
}

function showArtistPopup(painting) {
    let popup = document.getElementById('artist-popup');
    if (!popup) {
        popup = document.createElement('div');
        popup.id = 'artist-popup';
        popup.className = 'artist-popup';
        // Insert after #message
        const msg = document.getElementById('message');
        if (msg && msg.parentNode) {
            msg.parentNode.insertBefore(popup, msg.nextSibling);
        } else {
            document.body.appendChild(popup);
        }
    }
    // Format: {Name} (YEAR–YEAR) \n {Work name} (YEAR)
    const name = painting.artist || '';
    const birth = getYearOnly(painting.artist_birth);
    const death = getYearOnly(painting.artist_death);
    const paintingTitle = cleanWorkTitle(painting.title ? stripHtml(painting.title) : '');
    const year = getYearOnly(painting.year);
    let imgHtml = '';
    if (painting.artist_image) {
        imgHtml = `<img src="${painting.artist_image}" alt="${name}" class="artist-portrait">`;
    }
    let lifeSpan = (birth && death) ? `${birth}–${death}` : (birth ? `${birth}–` : (death ? `–${death}` : ''));
    let line1 = `${name}${lifeSpan ? ` (${lifeSpan})` : ''}`;
    let line2 = paintingTitle ? `${paintingTitle}${year ? ` (${year})` : ''}` : '';
    popup.innerHTML = `
        <div class="artist-popup-content">
            ${imgHtml}
            <div class="artist-popup-text">
                <strong>${line1}</strong><br>
                ${line2 ? `<span>${line2}</span>` : ''}
            </div>
        </div>
    `;
    popup.style.display = 'block';
    setTimeout(() => { popup.style.opacity = 1; }, 10);
    setTimeout(() => {
        popup.style.opacity = 0;
        setTimeout(() => { popup.style.display = 'none'; }, 400);
    }, 2500); // 2.5 seconds
}

// Make logo/title clickable to reset
function setupLogoReset() {
    const logo = document.querySelector('.title');
    if (logo) {
        logo.style.cursor = 'pointer';
        logo.onclick = function() {
            selectedCategory = 'all';
            const catSelect = document.getElementById('category-select');
            if (catSelect) catSelect.value = 'all';
            streak = 0;
            updateStreakBar();
            loadQuiz();
        };
    }
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
    setupLogoReset();
    setupCategoryChangeInfoBar();
});
