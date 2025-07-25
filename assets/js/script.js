let streak = 0;
let paintings = [];
let lastPaintingIndex = -1;
let selectedCategory = 'all';
let artistBios = [];

function getYearOnly(dateStr) {
    if (!dateStr) return '';
    // Try to find the first 4-digit year in the string
    const match = dateStr.match(/\b(17|18|19|20|21)\d{2}\b/);
    return match ? match[0] : '';
}

function getCenturyFromYear(yearStr) {
    const year = parseInt(getYearOnly(yearStr), 10);
    if (!year || isNaN(year)) return null;
    return Math.floor((year - 1) / 100) + 1;
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
    // Get top 9 categories (excluding 'all'), sorted by number of paintings
    const sortedCats = Object.keys(counts)
        .filter(cat => cat !== 'all')
        .sort((a, b) => counts[b] - counts[a])
        .slice(0, 9);
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

// Custom category selector as clickable text
function renderCategorySelector() {
    const catSelect = document.getElementById('category-select');
    const selectorDiv = document.querySelector('.category-selector');
    if (!catSelect || !selectorDiv) return;
    catSelect.style.display = 'none';
    let custom = document.getElementById('custom-category-link');
    if (!custom) {
        custom = document.createElement('span');
        custom.id = 'custom-category-link';
        custom.className = 'custom-category-link';
        selectorDiv.appendChild(custom);
    }
    // Only show these categories
    const CATEGORY_ORDER = [
        { value: 'all', label: 'Full collection' },
        { value: 'Popular painters', label: 'Popular painters' },
        { value: 'National Museum of Norway', label: 'National Museum of Norway' },
        { value: 'Landscapes', label: 'Landscapes' }
    ];
    // Filter to only those that exist in the data
    const { counts } = getCategoryCounts();
    const options = CATEGORY_ORDER.filter(opt => opt.value === 'all' || counts[opt.value]);
    // Set current
    const current = catSelect.value || 'all';
    custom.textContent = options.find(o => o.value === current)?.label || 'Full collection';
    custom.style.textDecoration = 'underline';
    custom.style.cursor = 'pointer';
    let menu = document.getElementById('custom-category-menu');
    if (menu) menu.remove();
    custom.onclick = function(e) {
        e.stopPropagation();
        if (document.getElementById('custom-category-menu')) return;
        menu = document.createElement('div');
        menu.id = 'custom-category-menu';
        menu.className = 'custom-category-menu';
        options.forEach(opt => {
            const item = document.createElement('div');
            item.className = 'custom-category-item';
            item.textContent = opt.label;
            item.onclick = function(ev) {
                catSelect.value = opt.value;
                selectedCategory = opt.value;
                streak = 0;
                updateStreakBar();
                updateCollectionInfo();
                loadQuiz();
                renderCategorySelector();
                menu.remove();
            };
            menu.appendChild(item);
        });
        custom.appendChild(menu);
        document.addEventListener('click', function handler() {
            if (menu) menu.remove();
            document.removeEventListener('click', handler);
        });
    };
}

// Call renderCategorySelector after paintings are loaded and on category change
// After paintings are loaded:
fetch('./data/paintings_merged.json')
    .then(res => res.json())
    .then(data => {
        paintings = data;
        updateCategoryDropdown();
        updateCollectionInfo();
        renderCategorySelector();
        loadQuiz();
        setupArtistModal();
        return loadArtistBios();
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
                    showArtistPopup(painting, null);
                    return;
                }
                selectedBtn.classList.add('correct');
                showMessage('Correct!', '#388e3c');
            } else {
                streak = 0;
                selectedBtn.classList.add('wrong');
                correctBtn.classList.add('correct');
                showMessage('Not correct!', '#e53935');
            }
            updateStreakBar();
            showArtistPopup(painting, () => {
                hideMessage();
                loadQuiz();
            });
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

function loadArtistBios() {
    return fetch('./data/artist_bios.json')
        .then(res => res.json())
        .then(data => { artistBios = data; });
}

function getArtistBioInfo(name) {
    if (!artistBios || !artistBios.length) return null;
    return artistBios.find(b => b.name === name) || null;
}

function showArtistPopup(painting, onDone) {
    let popup = document.getElementById('artist-popup');
    if (!popup) {
        popup = document.createElement('div');
        popup.id = 'artist-popup';
        popup.className = 'artist-popup toast';
        document.body.appendChild(popup);
    }
    const name = painting.artist || '';
    const bioInfo = getArtistBioInfo(name);
    // Count paintings for this artist
    const numPaintings = paintings.filter(p => p.artist === name).length;
    let nameHtml = '';
    let yearsHtml = '';
    let bioHtml = '';
    let imgHtml = '';
    if (bioInfo) {
        nameHtml = `<span class='artist-name'>${bioInfo.name}</span>`;
        yearsHtml = `<span class='artist-years'>${bioInfo.birth_year}–${bioInfo.death_year}</span>`;
        bioHtml = `<span class='artist-bio'>${bioInfo.bio}</span>`;
        if (bioInfo.self_portrait_url) {
            imgHtml = `<img src="${bioInfo.self_portrait_url}" alt="${bioInfo.name}" class="artist-portrait toast-portrait">`;
        }
        // Add number of paintings at the end of the bio
        bioHtml += ` <span class='artist-painting-count'>(${numPaintings} painting${numPaintings === 1 ? '' : 's'})</span>`;
    } else {
        const birth = getYearOnly(painting.artist_birth);
        const death = getYearOnly(painting.artist_death);
        let lifeSpan = (birth && death) ? `${birth}–${death}` : (birth ? `${birth}–` : (death ? `–${death}` : ''));
        nameHtml = `<span class='artist-name'>${name}</span>`;
        yearsHtml = lifeSpan ? `<span class='artist-years'>${lifeSpan}</span>` : '';
        imgHtml = painting.artist_image ? `<img src="${painting.artist_image}" alt="${name}" class="artist-portrait toast-portrait">` : '';
        bioHtml = '';
    }
    // Remove the number of paintings from the nameHtml
    nameHtml = nameHtml.replace(/ \(.*painting.*\)$/, '');
    popup.innerHTML = `
        <div class="artist-popup-content toast-content">
            ${imgHtml}
            <div class="artist-popup-text toast-text">
                ${nameHtml}
                ${yearsHtml}
                ${bioHtml}
            </div>
        </div>
    `;
    popup.classList.add('visible');
    setTimeout(() => {
        popup.classList.remove('visible');
        setTimeout(() => { popup.style.display = 'none'; if (onDone) onDone(); }, 400);
    }, 3000);
    popup.style.display = 'flex';
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

function showArtistsModal() {
    // Only artists with paintings in the dataset
    const artistSet = new Set(paintings.map(p => p.artist).filter(Boolean));
    const artists = Array.from(artistSet).sort((a, b) => a.localeCompare(b));
    // Split into columns (3 columns)
    const numCols = 3;
    const perCol = Math.ceil(artists.length / numCols);
    const columns = [];
    for (let i = 0; i < numCols; i++) {
        columns.push(artists.slice(i * perCol, (i + 1) * perCol));
    }
    // Build HTML
    const container = document.getElementById('artist-list-columns');
    container.innerHTML = '';
    columns.forEach(col => {
        const div = document.createElement('div');
        div.className = 'artist-list-col';
        const ul = document.createElement('ul');
        col.forEach(name => {
            const li = document.createElement('li');
            // Count paintings for this artist
            const numPaintings = paintings.filter(p => p.artist === name).length;
            li.textContent = `${name} (${numPaintings})`;
            ul.appendChild(li);
        });
        div.appendChild(ul);
        container.appendChild(div);
    });
    document.getElementById('artists-modal').style.display = 'flex';
}

// Modal open/close logic
function setupArtistModal() {
    const showLink = document.getElementById('show-artists-link');
    const closeBtn = document.getElementById('close-artists-modal');
    if (showLink) {
        showLink.onclick = function(e) {
            e.preventDefault();
            showArtistsModal();
        };
    }
    if (closeBtn) {
        closeBtn.onclick = function() {
            document.getElementById('artists-modal').style.display = 'none';
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
    renderCategorySelector();
});
