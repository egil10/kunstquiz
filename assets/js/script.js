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
    CATEGORY_DEFS.forEach(cat => {
        const prev = selectedCategory;
        selectedCategory = cat.value;
        const valid = getValidPaintings();
        counts[cat.value] = valid.length;
        painterSets[cat.value] = new Set(valid.map(p => p.artist));
        selectedCategory = prev;
    });
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
    // Only show categories that have at least 1 painting
    const options = CATEGORY_DEFS.filter(cat => {
        if (cat.value === 'all') return true;
        const prev = selectedCategory;
        selectedCategory = cat.value;
        const count = getValidPaintings().length;
        selectedCategory = prev;
        return count > 0;
    });
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
    const options = CATEGORY_DEFS.filter(cat => {
        if (cat.value === 'all') return true;
        const prev = selectedCategory;
        selectedCategory = cat.value;
        const count = getValidPaintings().length;
        selectedCategory = prev;
        return count > 0;
    });
    // Set current
    const current = catSelect.value || 'all';
    custom.textContent = options.find(o => o.value === current)?.label || 'Full Collection';
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

// Helper to get artist bios by name
function getArtistBioMap() {
    if (!artistBios || !artistBios.length) return {};
    const map = {};
    artistBios.forEach(b => { map[b.name] = b; });
    return map;
}

// List of new categories
const CATEGORY_DEFS = [
    { value: 'all', label: 'Full Collection' },
    { value: 'popular', label: 'Popular Painters' },
    { value: 'landscape', label: 'Landscape Painting' },
    { value: 'romanticism', label: 'Romanticism' },
    { value: 'impressionism', label: 'Impressionism' },
    { value: 'expressionism', label: 'Expressionism' },
    { value: 'portraits', label: 'Portraits' },
    { value: 'historical', label: 'Historical/Nationalism' },
    { value: '19thcentury', label: '19th Century' },
    { value: '20thcentury', label: '20th Century' }
];

function getValidPaintings() {
    let filtered = paintings.filter(p => p.artist && p.url);
    if (!selectedCategory || selectedCategory === 'all') return filtered;
    const artistMap = getArtistBioMap();
    function arr(val) {
        if (Array.isArray(val)) return val;
        if (typeof val === 'string') return [val];
        return [];
    }
    if (selectedCategory === 'popular') {
        // Top 10 artists by number of paintings
        const artistCounts = {};
        paintings.forEach(p => { if (p.artist) artistCounts[p.artist] = (artistCounts[p.artist] || 0) + 1; });
        const topArtists = Object.entries(artistCounts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10)
            .map(([name]) => name);
        filtered = filtered.filter(p => topArtists.includes(p.artist));
    } else if (selectedCategory === 'landscape') {
        filtered = filtered.filter(p => {
            const bio = artistMap[p.artist];
            return bio && (
                arr(bio.genre).some(g => g.toLowerCase().includes('landscape')) ||
                arr(bio.movement).some(m => m.toLowerCase().includes('landscape'))
            );
        });
    } else if (selectedCategory === 'romanticism') {
        filtered = filtered.filter(p => {
            const bio = artistMap[p.artist];
            return bio && arr(bio.movement).some(m => m.toLowerCase().includes('romanticism'));
        });
    } else if (selectedCategory === 'impressionism') {
        filtered = filtered.filter(p => {
            const bio = artistMap[p.artist];
            return bio && arr(bio.movement).some(m => m.toLowerCase().includes('impressionism'));
        });
    } else if (selectedCategory === 'expressionism') {
        filtered = filtered.filter(p => {
            const bio = artistMap[p.artist];
            return bio && arr(bio.movement).some(m => m.toLowerCase().includes('expressionism'));
        });
    } else if (selectedCategory === 'portraits') {
        filtered = filtered.filter(p => {
            const bio = artistMap[p.artist];
            return bio && arr(bio.genre).some(g => g.toLowerCase().includes('portrait'));
        });
    } else if (selectedCategory === 'historical') {
        filtered = filtered.filter(p => {
            const bio = artistMap[p.artist];
            return bio && (
                arr(bio.genre).some(g => g.toLowerCase().includes('historical') || g.toLowerCase().includes('nationalism') || g.toLowerCase().includes('mythology')) ||
                arr(bio.movement).some(m => m.toLowerCase().includes('historical') || m.toLowerCase().includes('nationalism') || m.toLowerCase().includes('mythology'))
            );
        });
    } else if (selectedCategory === '19thcentury') {
        filtered = filtered.filter(p => {
            const bio = artistMap[p.artist];
            const y = bio && bio.birth_year ? parseInt(bio.birth_year) : null;
            return y && y >= 1800 && y < 1900;
        });
    } else if (selectedCategory === '20thcentury') {
        filtered = filtered.filter(p => {
            const bio = artistMap[p.artist];
            let y = bio && bio.birth_year ? parseInt(bio.birth_year) : null;
            if (!y && bio && bio.death_year) y = parseInt(bio.death_year);
            const isModern = bio && (
                arr(bio.movement).some(m => m.toLowerCase().includes('modern')) ||
                arr(bio.genre).some(g => g.toLowerCase().includes('modern'))
            );
            return (y && y >= 1900 && y < 2000) || isModern;
        });
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
                    setTimeout(() => {
                        showArtistPopup(painting, null);
                    }, 900);
                    return;
                }
                selectedBtn.classList.add('correct');
                showMessage('Correct!', '#388e3c');
            } else {
                streak = 0;
                selectedBtn.classList.add('wrong');
                correctBtn.classList.add('correct');
                showMessage('Incorrect!', '#e53935');
            }
            updateStreakBar();
            setTimeout(() => {
                showArtistPopup(painting, () => {
                    hideMessage();
                    loadQuiz();
                });
            }, 900);
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

// Add overlay for persistent popup
function ensureArtistPopupOverlay() {
    let overlay = document.getElementById('artist-popup-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'artist-popup-overlay';
        document.body.appendChild(overlay);
    }
    return overlay;
}

function showArtistPopup(paintingOrName, onDone, persistent = false) {
    let popup;
    if (persistent) {
        popup = document.getElementById('artist-popup');
        if (!popup) {
            popup = document.createElement('div');
            popup.id = 'artist-popup';
            popup.className = 'artist-popup persistent';
            document.body.appendChild(popup);
        }
    } else {
        // In-game popup: render above the answer buttons and cover them
        let optionsDiv = document.getElementById('options');
        let container = document.getElementById('artist-popup-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'artist-popup-container';
            optionsDiv.parentNode.insertBefore(container, optionsDiv);
        }
        // Remove any previous popup
        container.innerHTML = '';
        popup = document.createElement('div');
        popup.id = 'artist-popup';
        popup.className = 'artist-popup toast artist-popup-cover';
        container.appendChild(popup);
    }
    // Accept either a painting object or a string name
    let name = typeof paintingOrName === 'string' ? paintingOrName : (paintingOrName.artist || '');
    const bioInfo = getArtistBioInfo(name);
    // Count paintings for this artist
    const artistPaintings = paintings.filter(p => p.artist === name);
    const numPaintings = artistPaintings.length;
    let yearsHtml = '';
    let imgHtml = '';
    let bioHtml = '';
    let tagsHtml = '';
    if (bioInfo) {
        yearsHtml = `<span class='artist-years'>${bioInfo.birth_year}–${bioInfo.death_year}</span>`;
        imgHtml = bioInfo.self_portrait_url ? `<img src="${bioInfo.self_portrait_url}" alt="${bioInfo.name}" class="artist-portrait toast-portrait">` : '';
        bioHtml = `<span class='artist-bio'>${bioInfo.bio}</span>`;
        let tagList = [];
        if (bioInfo.awards && bioInfo.awards.length) tagList = tagList.concat(bioInfo.awards);
        if (bioInfo.movement && bioInfo.movement.length) tagList = tagList.concat(bioInfo.movement);
        if (bioInfo.genre && bioInfo.genre.length) tagList = tagList.concat(bioInfo.genre);
        if (tagList.length) {
            tagsHtml = `<div class='artist-tags'>${tagList.map(tag => `<span class='artist-tag'>${tag}</span>`).join('')}</div>`;
        }
        bioHtml += ` <span class='artist-painting-count'>(${numPaintings} painting${numPaintings === 1 ? '' : 's'})</span>`;
    } else {
        const birth = getYearOnly(paintingOrName.artist_birth);
        const death = getYearOnly(paintingOrName.artist_death);
        let lifeSpan = (birth && death) ? `${birth}–${death}` : (birth ? `${birth}–` : (death ? `–${death}` : ''));
        yearsHtml = lifeSpan ? `<span class='artist-years'>${lifeSpan}</span>` : '';
        imgHtml = paintingOrName.artist_image ? `<img src="${paintingOrName.artist_image}" alt="${name}" class="artist-portrait toast-portrait">` : '';
        bioHtml = '';
        tagsHtml = '';
    }
    let closeBtnHtml = '';
    if (persistent) {
        closeBtnHtml = `<button class='artist-popup-close' aria-label='Close'>&times;</button>`;
    }
    // Persistent: right side is only images (no titles/years)
    let paintingsHtml = '';
    if (persistent && artistPaintings.length > 0) {
        paintingsHtml = `<div class='artist-paintings-grid only-images'>` +
            artistPaintings.map(p =>
                `<div class='artist-painting-thumb'>
                    <img src="${p.url}" alt="${p.title}" title="${p.title}" />
                </div>`
            ).join('') +
            `</div>`;
    }
    // In-game: 2-column layout, image left, info right, covers answer options
    let contentHtml = '';
    if (!persistent) {
        contentHtml = `
        <div class="artist-popup-columns in-game-cover">
            <div class="artist-popup-left">
                ${imgHtml}
            </div>
            <div class="artist-popup-right">
                <div class="artist-popup-text toast-text">
                    <span class='artist-name'>${name}</span>
                    ${yearsHtml}
                    ${bioHtml}
                    ${tagsHtml}
                </div>
            </div>
        </div>
        `;
    } else {
        contentHtml = `
        <div class="artist-popup-columns persistent-modal">
            <div class="artist-popup-left">
                ${imgHtml}
                <div class="artist-popup-text toast-text">
                    <span class='artist-name'>${name}</span>
                    ${yearsHtml}
                    ${bioHtml}
                    ${tagsHtml}
                </div>
            </div>
            <div class="artist-popup-right only-images">
                ${paintingsHtml}
            </div>
            ${closeBtnHtml}
        </div>
        `;
    }
    popup.innerHTML = contentHtml;
    popup.style.opacity = 0;
    popup.classList.add('visible');
    popup.style.display = 'flex';
    setTimeout(() => { popup.style.opacity = 1; }, 10);
    if (!persistent) {
        popup.style.position = 'static';
        popup.style.top = '';
        popup.style.left = '';
        popup.style.transform = '';
        popup.style.zIndex = '';
        popup.style.maxWidth = '100%';
        popup.style.minWidth = '320px';
        let overlay = document.getElementById('artist-popup-overlay');
        if (overlay) overlay.classList.remove('visible');
    } else {
        popup.classList.remove('toast');
        popup.classList.add('persistent');
        popup.style.position = 'fixed';
        popup.style.top = '12vh';
        popup.style.left = '50%';
        popup.style.transform = 'translateX(-50%)';
        popup.style.zIndex = '2000';
        popup.style.maxWidth = '700px';
        popup.style.minWidth = '320px';
        let overlay = ensureArtistPopupOverlay();
        overlay.classList.add('visible');
    }
    if (persistent) {
        const closeBtn = popup.querySelector('.artist-popup-close');
        if (closeBtn) {
            closeBtn.onclick = function() {
                popup.classList.remove('visible');
                popup.style.opacity = 0;
                setTimeout(() => { popup.style.display = 'none'; let overlay = document.getElementById('artist-popup-overlay'); if (overlay) overlay.classList.remove('visible'); if (onDone) onDone(); }, 400);
            };
        }
        setTimeout(() => {
            function outsideClick(e) {
                if (!popup.contains(e.target)) {
                    popup.classList.remove('visible');
                    popup.style.opacity = 0;
                    setTimeout(() => { popup.style.display = 'none'; let overlay = document.getElementById('artist-popup-overlay'); if (overlay) overlay.classList.remove('visible'); if (onDone) onDone(); }, 400);
                    document.removeEventListener('mousedown', outsideClick);
                }
            }
            document.addEventListener('mousedown', outsideClick);
        }, 100);
    } else {
        setTimeout(() => {
            popup.classList.remove('visible');
            popup.style.opacity = 0;
            setTimeout(() => { if (popup.parentNode) popup.parentNode.removeChild(popup); if (onDone) onDone(); }, 400);
        }, 3500);
    }
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
            // Make artist name clickable
            const a = document.createElement('a');
            a.href = '#';
            a.textContent = `${name} (${numPaintings})`;
            a.onclick = (e) => {
                e.preventDefault();
                showArtistPopup(name, null, true);
            };
            li.appendChild(a);
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
