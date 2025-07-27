'use strict';

// Language support
let currentLanguage = 'en'; // 'en' for English, 'no' for Norwegian
const translations = {
  en: {
    title: 'Kunstquiz',
    collectionInfo: 'paintings, painters',
    fullCollection: 'Full Collection',
    popularPainters: 'Popular Painters',
    landscapePainting: 'Landscape Painting',
    portraits: 'Portraits',
    womenPainters: 'Women Painters',
    nineteenthCentury: '19th Century',
    twentiethCentury: '20th Century',
    impressionism: 'Impressionism',
    expressionism: 'Expressionism',
    norwegianRomantic: 'Norwegian Romantic',
    correct: 'Correct!',
    incorrect: 'Incorrect!',
    congratulations: 'Congratulations!',
    streakMessage: 'You got 10 in a row!',
    playAgain: 'Play Again',
    noPaintings: 'No valid paintings found.',
    notEnoughArtists: 'Not enough artists for quiz.',
    errorLoading: 'Error loading quiz data. Please try again later.',
    close: 'Close',
    artists: 'All Artists',
    gallery: 'Gallery',
    about: 'About',
    language: 'Language',
    paintings: 'paintings',
    painting: 'painting',
    painters: 'painters',
    // About modal translations
    aboutTitle: 'About Kunstquiz',
    aboutCollection: 'The Collection',
    aboutCollectionText: 'Kunstquiz features 3,282 paintings from 81 Norwegian artists, making it one of the most comprehensive Norwegian art quizzes available. Our collection spans from the 19th century to contemporary works, covering various movements and styles.',
    aboutCategories: 'Quiz Categories',
    aboutCategoriesText: 'Full Collection: All 3,282 paintings, Popular Painters: Top 10 artists with most works, Landscape Painting: 1,745 landscape works, Portraits: 584 portrait paintings, Women Painters: 259 works by female artists, Impressionism: 392 impressionist works, Expressionism: 253 expressionist paintings, Norwegian Romantic: 765 romantic nationalist works',
    aboutHowToPlay: 'How to Play',
    aboutHowToPlayText: 'Select a category, view a painting, and choose the correct artist from four options. Build streaks and learn about Norwegian art history with each answer!',
    aboutFacts: 'Interesting Facts',
    aboutFactsText: 'Data sourced from open Wikimedia and Wikidata APIs, Features 33 different art genres including landscape, portrait, and abstract painting, Includes 7 major art movements from Impressionism to Contemporary art, Collection spans over 200 years of Norwegian art history, All images are freely available under open licenses',
    aboutTechnical: 'Technical Details',
    aboutTechnicalText: 'Built with modern web technologies, featuring responsive design for all devices. The quiz uses intelligent artist weighting to ensure fair representation regardless of collection size.',
    // Encouraging messages for correct answers
    encouragingMessages: [
      'Excellent! 🎨',
      'Perfect! ✨',
      'Brilliant! 🌟',
      'Well done! 👏',
      'Fantastic! 🎯',
      'Outstanding! 🏆',
      'Amazing! 💫',
      'Superb! 🎪',
      'Incredible! 🔥',
      'Wonderful! 🌈',
      'Spectacular! ⭐',
      'Marvelous! 🎭',
      'Splendid! 🎪',
      'Magnificent! 👑',
      'Exceptional! 🎨'
    ]
  },
  no: {
    title: 'Kunstquiz',
    collectionInfo: 'malerier, malere',
    fullCollection: 'Full Samling',
    popularPainters: 'Populære Malere',
    landscapePainting: 'Landskapsmaleri',
    portraits: 'Portretter',
    womenPainters: 'Kvinnelige Malere',
    nineteenthCentury: '19. Århundre',
    twentiethCentury: '20. Århundre',
    impressionism: 'Impressionisme',
    expressionism: 'Ekspresjonisme',
    norwegianRomantic: 'Norsk Romantikk',
    correct: 'Riktig!',
    incorrect: 'Feil!',
    congratulations: 'Gratulerer!',
    streakMessage: 'Du klarte 10 på rad!',
    playAgain: 'Spill igjen',
    noPaintings: 'Ingen gyldige malerier funnet.',
    notEnoughArtists: 'Ikke nok kunstnere for quiz.',
    errorLoading: 'Feil ved lasting av quiz-data. Vennligst prøv igjen senere.',
    close: 'Lukk',
    artists: 'Alle Kunstnere',
    gallery: 'Galleri',
    about: 'Om',
    language: 'Språk',
    paintings: 'malerier',
    painting: 'maleri',
    painters: 'malere',
    // About modal translations
    aboutTitle: 'Om Kunstquiz',
    aboutCollection: 'Samlingen',
    aboutCollectionText: 'Kunstquiz inneholder 3,282 malerier fra 81 norske kunstnere, noe som gjør det til en av de mest omfattende norske kunstquizene tilgjengelig. Vår samling spenner fra 1800-tallet til samtidsverk, og dekker ulike bevegelser og stiler.',
    aboutCategories: 'Quiz-kategorier',
    aboutCategoriesText: 'Full Samling: Alle 3,282 malerier, Populære Malere: Topp 10 kunstnere med flest verk, Landskapsmaleri: 1,745 landskapsverk, Portretter: 584 portrettmalerier, Kvinnelige Malere: 259 verk av kvinnelige kunstnere, Impressionisme: 392 impressionistiske verk, Ekspresjonisme: 253 ekspresjonistiske malerier, Norsk Romantikk: 765 romantisk nasjonalistiske verk',
    aboutHowToPlay: 'Slik spiller du',
    aboutHowToPlayText: 'Velg en kategori, se på et maleri, og velg riktig kunstner fra fire alternativer. Bygg opp streaks og lær om norsk kunsthistorie med hvert svar!',
    aboutFacts: 'Interessante fakta',
    aboutFactsText: 'Data hentet fra åpne Wikimedia og Wikidata APIer, Inneholder 33 ulike kunstgenrer inkludert landskap, portrett og abstrakt maleri, Inkluderer 7 store kunstbevegelser fra impressionisme til samtidskunst, Samlingen spenner over 200 år med norsk kunsthistorie, Alle bilder er fritt tilgjengelige under åpne lisenser',
    aboutTechnical: 'Tekniske detaljer',
    aboutTechnicalText: 'Bygget med moderne webteknologier, med responsivt design for alle enheter. Quizen bruker intelligent kunstnervektlegging for å sikre rettferdig representasjon uansett samlingsstørrelse.',
    // Encouraging messages for correct answers
    encouragingMessages: [
      'Utmerket! 🎨',
      'Perfekt! ✨',
      'Strålende! 🌟',
      'Bra gjort! 👏',
      'Fantastisk! 🎯',
      'Fremragende! 🏆',
      'Fantastisk! 💫',
      'Suverent! 🎪',
      'Utrolig! 🔥',
      'Vidunderlig! 🌈',
      'Spektakulært! ⭐',
      'Marveløst! 🎭',
      'Praktfullt! 🎪',
      'Magnifikt! 👑',
      'Exceptionelt! 🎨'
    ]
  }
};

// Artist weighting system
let artistWeights = new Map(); // Track how often each artist appears
let lastSelectedArtists = new Set(); // Track recently selected artists to avoid repetition

// Encouraging message counter
let encouragingMessageIndex = 0;

let streak = 0;
let paintings = [];
let lastPaintingIndex = -1;
let selectedCategory = 'all';
let artistBios = [];

// List of categories with consistent labels - Updated based on actual data
const CATEGORY_DEFS = [
  { value: 'all', label: 'fullCollection' },
  { value: 'popular', label: 'popularPainters' },
  { value: 'landscape', label: 'landscapePainting' },
  { value: 'portraits', label: 'portraits' },
  { value: 'women_painters', label: 'womenPainters' },
  { value: '19thcentury', label: 'nineteenthCentury' },
  { value: '20thcentury', label: 'twentiethCentury' },
  { value: 'impressionism', label: 'impressionism' },
  { value: 'expressionism', label: 'expressionism' },
  { value: 'norwegian_romantic', label: 'norwegianRomantic' }
];

function t(key) {
  return translations[currentLanguage][key] || key;
}

function updateLanguageUI() {
  // Update title
  const title = document.querySelector('.title');
  if (title) title.textContent = t('title');
  
  // Update category labels
  const customLink = document.getElementById('custom-category-link');
  if (customLink) {
    const currentValue = document.getElementById('category-select')?.value || 'all';
    const category = CATEGORY_DEFS.find(cat => cat.value === currentValue);
    if (category) {
      customLink.textContent = t(category.label);
    }
  }
  
  // Update collection info
  updateCollectionInfo();
  
  // Update language link
  const languageLink = document.getElementById('language-link');
  if (languageLink) {
    languageLink.textContent = currentLanguage === 'en' ? 'Norsk' : 'English';
  }
  
  // Update modal texts
  const congratsTitle = document.getElementById('congrats-title');
  if (congratsTitle) congratsTitle.textContent = t('congratulations');
  
  const congratsMessage = document.querySelector('#congrats-modal p');
  if (congratsMessage) congratsMessage.textContent = t('streakMessage');
  
  const resetBtn = document.getElementById('reset-btn');
  if (resetBtn) resetBtn.textContent = t('playAgain');
  
  const artistsTitle = document.getElementById('artists-title');
  if (artistsTitle) artistsTitle.textContent = t('artists');
  
  const galleryTitle = document.getElementById('gallery-title');
  if (galleryTitle) galleryTitle.textContent = t('gallery');
  
  const aboutTitle = document.getElementById('about-title');
  if (aboutTitle) aboutTitle.textContent = t('aboutTitle');
  
  const closeArtistsBtn = document.getElementById('close-artists-modal');
  if (closeArtistsBtn) closeArtistsBtn.textContent = t('close');
  
  const closeGalleryBtn = document.getElementById('close-gallery-modal');
  if (closeGalleryBtn) closeGalleryBtn.textContent = t('close');
  
  const closeAboutBtn = document.getElementById('close-about-modal');
  if (closeAboutBtn) closeAboutBtn.textContent = t('close');
}

function setupLanguageToggle() {
  const languageLink = document.getElementById('language-link');
  if (languageLink) {
    languageLink.addEventListener('click', e => {
      e.preventDefault();
      currentLanguage = currentLanguage === 'en' ? 'no' : 'en';
      updateLanguageUI();
      renderCategorySelector();
      updateStreakBar();
    });
  }
}



// Artist weighting system
function initializeArtistWeights() {
  const validPaintings = getValidPaintings();
  const artistCounts = {};
  
  validPaintings.forEach(painting => {
    if (painting.artist) {
      artistCounts[painting.artist] = (artistCounts[painting.artist] || 0) + 1;
    }
  });
  
  // Calculate weights inversely proportional to painting count
  const maxCount = Math.max(...Object.values(artistCounts));
  Object.keys(artistCounts).forEach(artist => {
    const count = artistCounts[artist];
    // Higher weight for artists with fewer paintings
    artistWeights.set(artist, maxCount / count);
  });
}

function getWeightedRandomPainting(validPaintings) {
  if (validPaintings.length <= 1) return validPaintings[0];
  
  // Filter out recently selected artists
  const availablePaintings = validPaintings.filter(p => 
    !lastSelectedArtists.has(p.artist)
  );
  
  if (availablePaintings.length === 0) {
    // If all artists were recently used, reset the set
    lastSelectedArtists.clear();
    return getWeightedRandomPainting(validPaintings);
  }
  
  // Calculate total weight
  let totalWeight = 0;
  const weightedPaintings = availablePaintings.map(painting => {
    const weight = artistWeights.get(painting.artist) || 1;
    totalWeight += weight;
    return { painting, weight, cumulativeWeight: totalWeight };
  });
  
  // Select random painting based on weights
  const random = Math.random() * totalWeight;
  const selected = weightedPaintings.find(wp => wp.cumulativeWeight >= random);
  
  if (selected) {
    // Add to recently selected set
    lastSelectedArtists.add(selected.painting.artist);
    if (lastSelectedArtists.size > 5) {
      // Keep only last 5 artists
      const artistsArray = Array.from(lastSelectedArtists);
      lastSelectedArtists = new Set(artistsArray.slice(-5));
    }
    return selected.painting;
  }
  
  return availablePaintings[0];
}

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
  infoBar.textContent = `${count} ${t('paintings')}, ${painterCount} ${t('painters')}`;
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
    option.textContent = t(opt.label);
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
  custom.textContent = t(options.find(o => o.value === current)?.label || 'fullCollection');
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
      item.textContent = t(opt.label);
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
  // Add click outside to close
  setTimeout(() => {
    function outsideClick(e) {
      if (!modal.querySelector('.gallery-modal-content').contains(e.target)) {
        hideGalleryModal();
        document.removeEventListener('mousedown', outsideClick);
      }
    }
    document.addEventListener('mousedown', outsideClick);
  }, 100);
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
  women_painters: p => p.artist_gender === 'female',
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
  impressionism: p => [...(p.artist_movement || []), ...(p.movement || [])].some(m => m?.toLowerCase().includes('impressionism')),
  expressionism: p => [...(p.artist_movement || []), ...(p.movement || [])].some(m => m?.toLowerCase().includes('expressionism')),
  norwegian_romantic: p => [...(p.artist_movement || []), ...(p.movement || [])].some(m => 
    m?.toLowerCase().includes('nasjonalromantikk') || 
    m?.toLowerCase().includes('norwegian romantic nationalism') || 
    m?.toLowerCase().includes('romantic nationalism')
  )
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
    document.getElementById('options').innerHTML = `<p>${t('noPaintings')}</p>`;
    return;
  }
  let painting;
  for (let i = 0; i < 10; i++) {
    painting = getWeightedRandomPainting(validPaintings);
    if (painting && painting.artist && painting.url) break;
  }
  if (!painting || !painting.artist || !painting.url) return;
  const img = document.getElementById('painting');
  img.src = painting.url;
  img.alt = stripHtml(painting.title) || t('painting');
  img.loading = 'lazy';
  const optionsDiv = document.getElementById('options');
  
  // Clear options and ensure no leftover classes
  optionsDiv.innerHTML = '';
  
  const artists = generateOptions(painting.artist, validPaintings);
  if (artists.length < 2) {
    optionsDiv.innerHTML = `<p>${t('notEnoughArtists')}</p>`;
    return;
  }
  artists.forEach(artist => {
    const btn = document.createElement('button');
    btn.textContent = artist;
    btn.onclick = () => {
      // Add loading state to prevent multiple clicks
      Array.from(optionsDiv.children).forEach(b => {
        b.classList.add('loading');
        b.disabled = true;
        b.classList.remove('correct', 'wrong');
      });
      
      const correctBtn = Array.from(optionsDiv.children).find(b => b.textContent === painting.artist);
      const selectedBtn = btn;
      
      if (artist === painting.artist) {
        // Correct answer - show encouraging popup and fast transition
        streak++;
        selectedBtn.classList.add('correct');
        
        // Show encouraging popup
        const encouragingMessage = getRandomEncouragingMessage();
        showEncouragingPopup(encouragingMessage);
        
        if (streak >= 10) {
          updateStreakBar();
          setTimeout(showCongratsModal, 500);
          setTimeout(() => showArtistPopup(painting, null), 900);
          return;
        }
        // Quick transition for correct answers
        setTimeout(() => {
          // Remove loading state and reset buttons
          Array.from(optionsDiv.children).forEach(b => {
            b.classList.remove('loading', 'correct', 'wrong');
            b.disabled = false;
          });
          loadQuiz();
        }, 300); // Faster transition for correct answers
      } else {
        // Incorrect answer - keep current timing with bio popup
        streak = 0;
        selectedBtn.classList.add('wrong');
        correctBtn.classList.add('correct');
        showMessage(t('incorrect'), '#e53935');
        updateStreakBar();
        setTimeout(() => {
          showArtistPopup(painting, () => {
            hideMessage();
            // Remove loading state and reset buttons
            Array.from(optionsDiv.children).forEach(b => {
              b.classList.remove('loading', 'correct', 'wrong');
              b.disabled = false;
            });
            loadQuiz();
          });
        }, 500);
      }
      updateStreakBar();
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
  if (!streakBar) return;
  
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
    // Remove all <a> links in the popup (if any)
    Array.from(popup.querySelectorAll('a')).forEach(link => link.remove());
    popup.className = 'artist-popup persistent';
    const overlay = ensureArtistPopupOverlay();
    overlay.classList.add('visible');
    const closeBtn = popup.querySelector('.artist-popup-close');
    if (closeBtn) closeBtn.addEventListener('click', () => hidePopup(popup, onDone));
    setTimeout(() => {
      function outsideClick(e) {
        if (!popup.contains(e.target)) {
          hidePopup(popup, onDone);
          document.removeEventListener('mousedown', outsideClick);
        }
      }
      document.addEventListener('mousedown', outsideClick);
    }, 100);
  } else {
    popup.className = 'artist-popup toast';
    setTimeout(() => hidePopup(popup, onDone), 2000);
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
      // Render as plain text, not a link
      li.textContent = `${name} (${numPaintings})`;
      ul.appendChild(li);
    });
    div.appendChild(ul);
    container.appendChild(div);
  });
  const modal = document.getElementById('artists-modal');
  modal.style.display = 'flex';
  modal.focus();
  // Add click outside to close
  setTimeout(() => {
    function outsideClick(e) {
      if (!modal.querySelector('.artists-modal-content').contains(e.target)) {
        document.getElementById('artists-modal').style.display = 'none';
        document.removeEventListener('mousedown', outsideClick);
      }
    }
    document.addEventListener('mousedown', outsideClick);
  }, 100);
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

function showAboutModal() {
  const modal = document.getElementById('about-modal');
  if (modal) modal.style.display = 'flex';
  modal.focus();
  // Add click outside to close
  setTimeout(() => {
    function outsideClick(e) {
      if (!modal.querySelector('.about-modal-content').contains(e.target)) {
        hideAboutModal();
        document.removeEventListener('mousedown', outsideClick);
      }
    }
    document.addEventListener('mousedown', outsideClick);
  }, 100);
}

function hideAboutModal() {
  const modal = document.getElementById('about-modal');
  if (modal) modal.style.display = 'none';
}

function setupAboutModal() {
  const showLink = document.getElementById('show-about-link');
  const closeBtn = document.getElementById('close-about-modal');
  if (showLink) showLink.addEventListener('click', e => {
    e.preventDefault();
    showAboutModal();
  });
  if (closeBtn) closeBtn.addEventListener('click', hideAboutModal);
}

function getRandomEncouragingMessage() {
  const messages = translations[currentLanguage].encouragingMessages;
  const message = messages[encouragingMessageIndex];
  encouragingMessageIndex = (encouragingMessageIndex + 1) % messages.length;
  return message;
}

function showEncouragingPopup(message) {
  // Remove any existing encouraging popup
  const existingPopup = document.getElementById('encouraging-popup');
  if (existingPopup) {
    existingPopup.remove();
  }
  
  const popup = document.createElement('div');
  popup.id = 'encouraging-popup';
  popup.className = 'encouraging-popup';
  popup.textContent = message;
  
  document.body.appendChild(popup);
  
  // Trigger animation
  setTimeout(() => {
    popup.classList.add('visible');
  }, 10);
  
  // Remove after animation
  setTimeout(() => {
    popup.classList.remove('visible');
    setTimeout(() => {
      if (popup.parentNode) {
        popup.parentNode.removeChild(popup);
      }
    }, 300);
  }, 800);
}

document.addEventListener('DOMContentLoaded', async () => {
  try {
    const res = await fetch('./data/paintings_merged.json');
    if (!res.ok) throw new Error('Failed to load paintings');
    paintings = await res.json();
    await loadArtistBios();
    
    // Initialize all systems
    initializeArtistWeights();
    updateCategoryDropdown();
    updateCollectionInfo();
    renderCategorySelector();
    updateLanguageUI();
    setupLanguageToggle();
    loadQuiz();
    setupArtistModal();
    setupGalleryModal();
    setupAboutModal();
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
        hideAboutModal();
        document.getElementById('artists-modal').style.display = 'none';
      }
    });
  } catch (err) {
    console.error('Error loading data:', err);
    document.getElementById('options').innerHTML = `<p>${t('errorLoading')}</p>`;
  }
});