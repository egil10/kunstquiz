'use strict';

let streak = 0;
let paintings = [];
let lastPaintingIndex = -1;
let selectedCategory = 'all';
let artistBios = [];

// List of categories with consistent labels
const CATEGORY_DEFS = [
  { value: 'all', label: 'Full Collection' },
  { value: 'popular', label: 'Popular Painters' },
  { value: 'landscape', label: 'Landscapes' },
  { value: 'portraits', label: 'Portraits' },
  { value: 'romanticism', label: 'Romanticism' },
  { value: 'expressionism', label: 'Expressionism' },
  { value: 'mountains_nature', label: 'Mountains & Nature' },
  { value: 'historical_nationalism', label: 'Historical / Nationalism' },
  { value: '1800s', label: '1800s' },
  { value: 'national_museum', label: 'National Museum of Norway' },
  { value: 'women_painters', label: 'Women Painters' },
];

function getYearOnly(dateStr) {
  if (!dateStr) return '';
  const match = dateStr.match(/\b(17|18|19|20|21)\d{2}\b/);
  return match ? match[0] : '';
}

function getCategoryCounts(categoryValue) {
  let filtered = paintings.filter(p => p.artist && p.url);
  if (categoryValue && categoryValue !== 'all') {
    const prev = selectedCategory;
    selectedCategory = categoryValue;
    filtered = getValidPaintings();
    selectedCategory = prev;
  }
  const count = filtered.length;
  const painterCount = new Set(filtered.map(p => p.artist)).size;
  return { count, painterCount };
}

function updateCollectionInfo() {
  const catSelect = document.getElementById('category-select');
  const infoBar = document.getElementById('collection-info');
  if (!catSelect || !infoBar) return;
  const selected = catSelect.value || 'all';
  const { count, painterCount } = getCategoryCounts(selected);
  infoBar.textContent = `${count} paintings, ${painterCount} painters`;
}

function updateCategoryDropdown() {
  const catSelect = document.getElementById('category-select');
  if (!catSelect) return;
  const options = CATEGORY_DEFS.filter(cat => {
    const { count } = getCategoryCounts(cat.value);
    return cat.value === 'all' || count > 0;
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

function setupCategoryChangeInfoBar() {
  const catSelect = document.getElementById('category-select');
  if (catSelect) {
    catSelect.addEventListener('change', () => {
      selectedCategory = catSelect.value;
      streak = 0;
      updateStreakBar();
      updateCollectionInfo();
      loadQuiz();
    });
  }
}

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
  const options = CATEGORY_DEFS.filter(cat => {
    if (cat.value === 'all') return true;
    const { count } = getCategoryCounts(cat.value);
    return count > 0;
  });
  const current = catSelect.value || 'all';
  custom.textContent = options.find(o => o.value === current)?.label || 'Full Collection';
  custom.onclick = e => {
    e.stopPropagation();
    let menu = document.getElementById('custom-category-menu');
    if (menu) return;
    menu = document.createElement('div');
    menu.id = 'custom-category-menu';
    menu.className = 'custom-category-menu';
    options.forEach(opt => {
      const item = document.createElement('div');
      item.className = 'custom-category-item';
      item.textContent = opt.label;
      item.onclick = ev => {
        ev.stopPropagation();
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
    document.addEventListener('click', () => {
      if (menu) menu.remove();
    }, { once: true });
  };
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

function showGalleryModal() {
  const modal = document.getElementById('gallery-modal');
  const collage = document.getElementById('gallery-collage');
  if (!modal || !collage) return;
  collage.innerHTML = '';
  const shuffled = [...paintings];
  shuffleArray(shuffled);
  const grid = document.createElement('div');
  grid.className = 'gallery-collage-grid';
  shuffled.forEach(p => {
    const img = document.createElement('img');
    img.src = p.url;
    img.alt = p.title || '';
    img.className = 'gallery-collage-img';
    img.loading = 'lazy';
    grid.appendChild(img);
  });
  collage.appendChild(grid);
  modal.style.display = 'flex';
  modal.focus();
}

function hideGalleryModal() {
  const modal = document.getElementById('gallery-modal');
  if (modal) modal.style.display = 'none';
}

function setupGalleryModal() {
  const showLink = document.getElementById('show-gallery-link');
  const closeBtn = document.getElementById('close-gallery-modal');
  if (showLink) showLink.addEventListener('click', e => {
    e.preventDefault();
    showGalleryModal();
  });
  if (closeBtn) closeBtn.addEventListener('click', hideGalleryModal);
}

function getArtistBioMap() {
  if (!Array.isArray(artistBios)) return {};
  return artistBios.reduce((map, b) => {
    map[b.name] = b;
    return map;
  }, {});
}

const categoryFilters = {
  popular: validPaintings => {
    const artistCounts = validPaintings.reduce((counts, p) => {
      if (p.artist) counts[p.artist] = (counts[p.artist] || 0) + 1;
      return counts;
    }, {});
    const topArtists = Object.entries(artistCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([name]) => name);
    return validPaintings.filter(p => topArtists.includes(p.artist));
  },
  landscape: p => [...(p.artist_genre || []), ...(p.genre || [])].some(g => g?.toLowerCase().includes('landscape')),
  portraits: p => [...(p.artist_genre || []), ...(p.genre || [])].some(g => g?.toLowerCase().includes('portrait')),
  impressionism: p => [...(p.artist_movement || []), ...(p.movement || [])].some(m => m?.toLowerCase().includes('impressionism')),
  expressionism: p => [...(p.artist_movement || []), ...(p.movement || [])].some(m => m?.toLowerCase().includes('expressionism')),
  abstract: p => [...(p.artist_genre || []), ...(p.genre || [])].some(g => g?.toLowerCase().includes('abstract')),
  '19thcentury': (p, artistMap) => {
    const bio = artistMap[p.artist];
    const y = bio?.birth_year ? parseInt(bio.birth_year) : null;
    return y && y >= 1800 && y < 1900;
  },
  '20thcentury': (p, artistMap) => {
    const bio = artistMap[p.artist];
    let y = bio?.birth_year ? parseInt(bio.birth_year) : (bio?.death_year ? parseInt(bio.death_year) : null);
    const isModern = bio && (
      (bio.movement || []).some(m => m?.toLowerCase().includes('modern')) ||
      (bio.genre || []).some(g => g?.toLowerCase().includes('modern'))
    );
    return (y && y >= 1900 && y < 2000) || isModern;
  },
  historical: p => [...(p.artist_genre || []), ...(p.genre || []), ...(p.artist_movement || []), ...(p.movement || [])].some(g => g?.toLowerCase().includes('historical') || g?.toLowerCase().includes('nationalism') || g?.toLowerCase().includes('mythology')),
  // Add more for other categories like 'romanticism', 'mountains_nature', etc., following similar patterns
};

function getValidPaintings() {
  let filtered = paintings.filter(p => p.artist && p.url);
  if (!selectedCategory || selectedCategory === 'all') return filtered;
  const artistMap = getArtistBioMap();
  const filterFn = categoryFilters[selectedCategory];
  if (filterFn) {
    if (selectedCategory.endsWith('century')) {
      filtered = filtered.filter(p => filterFn(p, artistMap));
    } else if (selectedCategory === 'popular') {
      filtered = filterFn(filtered);
    } else {
      filtered = filtered.filter(filterFn);
    }
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
  for (let i = 0; i < 10; i++) {
    painting = getRandomPainting(validPaintings);
    if (painting && painting.artist && painting.url) break;
  }
  if (!painting || !painting.artist || !painting.url) return;
  const img = document.getElementById('painting');
  img.src = painting.url;
  img.alt = stripHtml(painting.title) || 'Painting';
  img.loading = 'lazy';
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
    btn.onclick = () => {
      Array.from(optionsDiv.children).forEach(b => b.disabled = true);
      const correctBtn = Array.from(optionsDiv.children).find(b => b.textContent === painting.artist);
      const selectedBtn = btn;
      if (artist === painting.artist) {
        streak++;
        selectedBtn.classList.add('correct');
        showMessage('Correct!', '#388e3c');
        if (streak >= 10) {
          updateStreakBar();
          setTimeout(showCongratsModal, 500);
          setTimeout(() => showArtistPopup(painting, null), 900);
          return;
        }
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
  if (validPaintings.length <= 1) return validPaintings[0];
  let idx;
  do {
    idx = Math.floor(Math.random() * validPaintings.length);
  } while (idx === lastPaintingIndex);
  lastPaintingIndex = idx;
  return validPaintings[idx];
}

function generateOptions(correct, validPaintings) {
  const uniqueArtists = [...new Set(validPaintings.map(p => p.artist))];
  if (uniqueArtists.length <= 4) return uniqueArtists.sort(() => Math.random() - 0.5);
  const set = new Set([correct]);
  while (set.size < 4) {
    const random = uniqueArtists[Math.floor(Math.random() * uniqueArtists.length)];
    set.add(random);
  }
  return [...set].sort(() => Math.random() - 0.5);
}

function stripHtml(html) {
  const div = document.createElement('div');
  div.innerHTML = html || '';
  return div.textContent || div.innerText || '';
}

function updateStreakBar() {
  const streakBar = document.getElementById('streak-bar');
  streakBar.innerHTML = '';
  for (let i = 0; i < 10; i++) {
    const circle = document.createElement('div');
    circle.className = `streak-circle${i < streak ? ' filled' : ''}`;
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
  const modal = document.getElementById('congrats-modal');
  modal.style.display = 'flex';
  modal.focus();
}

function hideCongratsModal() {
  document.getElementById('congrats-modal').style.display = 'none';
}

function cleanWorkTitle(title) {
  if (!title) return '';
  return title.replace(/label QS:[^\s,]+,[^\n"]+"/g, '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
}

async function loadArtistBios() {
  try {
    const res = await fetch('./data/artist_bios.json');
    if (!res.ok) throw new Error('Failed to load artist bios');
    artistBios = await res.json();
  } catch (err) {
    console.error(err);
    artistBios = [];
  }
}

function getArtistBioInfo(name) {
  return artistBios.find(b => b.name === name) || null;
}

function ensureArtistPopupOverlay() {
  let overlay = document.getElementById('artist-popup-overlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'artist-popup-overlay';
    document.body.appendChild(overlay);
  }
  return overlay;
}

function createPopupTemplate({ name, bioInfo, artistPaintings, persistent, imgHtml, yearsHtml, bioHtml, tagsHtml, closeBtnHtml, paintingsHtml }) {
  return `
    <div class="artist-popup-content toast-content">
      ${imgHtml}
      <div class="artist-popup-text toast-text">
        <span class="artist-name">${name}</span>
        ${yearsHtml}
        ${bioHtml}
        ${tagsHtml}
      </div>
    </div>
    ${paintingsHtml}
    ${closeBtnHtml}
  `;
}

function showArtistPopup(paintingOrName, onDone, persistent = false) {
  let popup = document.getElementById('artist-popup');
  if (!popup) {
    popup = document.createElement('div');
    popup.id = 'artist-popup';
    document.body.appendChild(popup);
  }
  const name = typeof paintingOrName === 'string' ? paintingOrName : paintingOrName.artist || '';
  const bioInfo = getArtistBioInfo(name);
  const artistPaintings = paintings.filter(p => p.artist === name);
  const numPaintings = artistPaintings.length;
  let yearsHtml = '';
  let imgHtml = '';
  let bioHtml = '';
  let tagsHtml = '';
  if (bioInfo) {
    yearsHtml = `<span class="artist-years">${bioInfo.birth_year}–${bioInfo.death_year}</span>`;
    imgHtml = bioInfo.self_portrait_url ? `<img src="${bioInfo.self_portrait_url}" alt="${name}" class="artist-portrait toast-portrait" loading="lazy">` : '';
    bioHtml = `<span class="artist-bio">${bioInfo.bio}</span>`;
    let tagList = [...(bioInfo.awards || []), ...(bioInfo.movement || []), ...(bioInfo.genre || [])];
    if (tagList.length) {
      tagsHtml = `<div class="artist-tags">${tagList.map(tag => `<span class="artist-tag">${tag}</span>`).join('')}</div>`;
    }
    bioHtml += ` <span class="artist-painting-count">(${numPaintings} painting${numPaintings === 1 ? '' : 's'})</span>`;
  } else if (typeof paintingOrName !== 'string') {
    const birth = getYearOnly(paintingOrName.artist_birth);
    const death = getYearOnly(paintingOrName.artist_death);
    const lifeSpan = (birth && death) ? `${birth}–${death}` : (birth ? `${birth}–` : (death ? `–${death}` : ''));
    yearsHtml = lifeSpan ? `<span class="artist-years">${lifeSpan}</span>` : '';
    imgHtml = paintingOrName.artist_image ? `<img src="${paintingOrName.artist_image}" alt="${name}" class="artist-portrait toast-portrait" loading="lazy">` : '';
  }
  let closeBtnHtml = persistent ? `<button class="artist-popup-close" aria-label="Close">×</button>` : '';
  let paintingsHtml = '';
  if (persistent && artistPaintings.length > 0) {
    paintingsHtml = `<div class="artist-paintings-grid only-images">${artistPaintings.map(p => `
      <div class="artist-painting-thumb">
        <img src="${p.url}" alt="${p.title}" title="${p.title}" loading="lazy" />
      </div>`).join('')}</div>`;
  }
  popup.innerHTML = createPopupTemplate({ name, bioInfo, artistPaintings, persistent, imgHtml, yearsHtml, bioHtml, tagsHtml, closeBtnHtml, paintingsHtml });
  popup.style.opacity = '0';
  popup.style.display = 'flex';
  popup.classList.add('visible');
  setTimeout(() => popup.style.opacity = '1', 10);
  if (persistent) {
    popup.className = 'artist-popup persistent';
    const overlay = ensureArtistPopupOverlay();
    overlay.classList.add('visible');
    const closeBtn = popup.querySelector('.artist-popup-close');
    if (closeBtn) closeBtn.addEventListener('click', () => hidePopup(popup, onDone));
    document.addEventListener('mousedown', e => {
      if (!popup.contains(e.target)) hidePopup(popup, onDone);
    }, { once: true });
  } else {
    popup.className = 'artist-popup toast';
    setTimeout(() => hidePopup(popup, onDone), 3500);
  }
}

function hidePopup(popup, onDone) {
  popup.classList.remove('visible');
  popup.style.opacity = '0';
  setTimeout(() => {
    if (popup.parentNode) popup.parentNode.removeChild(popup);
    const overlay = document.getElementById('artist-popup-overlay');
    if (overlay) overlay.classList.remove('visible');
    if (onDone) onDone();
  }, 400);
}

function setupLogoReset() {
  const logo = document.querySelector('.title');
  if (logo) {
    logo.onclick = () => {
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
  const artistSet = new Set(paintings.map(p => p.artist).filter(Boolean));
  const artists = [...artistSet].sort((a, b) => a.localeCompare(b));
  const numCols = 3;
  const perCol = Math.ceil(artists.length / numCols);
  const columns = [];
  for (let i = 0; i < numCols; i++) {
    columns.push(artists.slice(i * perCol, (i + 1) * perCol));
  }
  const container = document.getElementById('artist-list-columns');
  container.innerHTML = '';
  columns.forEach(col => {
    const div = document.createElement('div');
    div.className = 'artist-list-col';
    const ul = document.createElement('ul');
    col.forEach(name => {
      const li = document.createElement('li');
      const numPaintings = paintings.filter(p => p.artist === name).length;
      const a = document.createElement('a');
      a.href = '#';
      a.textContent = `${name} (${numPaintings})`;
      a.onclick = e => {
        e.preventDefault();
        showArtistPopup(name, null, true);
      };
      li.appendChild(a);
      ul.appendChild(li);
    });
    div.appendChild(ul);
    container.appendChild(div);
  });
  const modal = document.getElementById('artists-modal');
  modal.style.display = 'flex';
  modal.focus();
}

function setupArtistModal() {
  const showLink = document.getElementById('show-artists-link');
  const closeBtn = document.getElementById('close-artists-modal');
  if (showLink) showLink.addEventListener('click', e => {
    e.preventDefault();
    showArtistsModal();
  });
  if (closeBtn) closeBtn.addEventListener('click', () => {
    document.getElementById('artists-modal').style.display = 'none';
  });
}

document.addEventListener('DOMContentLoaded', async () => {
  try {
    const res = await fetch('./data/paintings_merged.json');
    if (!res.ok) throw new Error('Failed to load paintings');
    paintings = await res.json();
    await loadArtistBios();
    updateCategoryDropdown();
    updateCollectionInfo();
    renderCategorySelector();
    loadQuiz();
    setupArtistModal();
    setupGalleryModal();
    setupLogoReset();
    setupCategoryChangeInfoBar();
    const resetBtn = document.getElementById('reset-btn');
    if (resetBtn) resetBtn.addEventListener('click', () => {
      streak = 0;
      updateStreakBar();
      hideCongratsModal();
      loadQuiz();
    });
    // Add Esc key to close modals
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') {
        hideCongratsModal();
        hideGalleryModal();
        document.getElementById('artists-modal').style.display = 'none';
      }
    });
  } catch (err) {
    console.error('Error loading data:', err);
    document.getElementById('options').innerHTML = '<p>Error loading quiz data. Please try again later.</p>';
  }
});