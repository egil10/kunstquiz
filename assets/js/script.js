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
    artists: 'Painters',
    gallery: 'Gallery',
    about: 'About',
    language: 'Language',
    paintings: 'paintings',
    painting: 'painting',
    painters: 'painters',
    // Footer links
    github: 'GitHub',
    instagram: 'Instagram',
    tiktok: 'TikTok',
    // Modal buttons and labels
    selectCategory: 'Select quiz category',
    // Correct answer messages
    correctMessages: [
      'Correct!',
      'Perfect!',
      'Excellent!',
      'Brilliant!',
      'Fantastic!',
      'Outstanding!',
      'Amazing!',
      'Superb!',
      'Incredible!',
      'Wonderful!',
      'Spectacular!',
      'Marvelous!',
      'Splendid!',
      'Magnificent!',
      'Exceptional!'
    ],
    // Incorrect answer messages
    incorrectMessages: [
      'Incorrect!',
      'Wrong!',
      'Not quite!',
      'Try again!',
      'Not right!',
      'That\'s not it!',
      'Incorrect answer!',
      'Wrong choice!',
      'Not the right one!',
      'That\'s not correct!',
      'Wrong artist!',
      'Not quite right!',
      'Incorrect!',
      'Wrong answer!',
      'That\'s not the one!'
    ],
    // Settings modal
    settings: 'Settings',
    languageLabel: 'Language',
    english: 'English',
    norwegian: 'Norwegian',
    // Round feedback messages
    roundFeedback: {
      '0/10': [
        'Don\'t worry, every expert was once a beginner!',
        'This is just the start of your art journey!',
        'Keep learning and you\'ll get better!',
        'Art appreciation takes time to develop!',
        'Every wrong answer is a learning opportunity!',
        'You\'re building the foundation for great knowledge!'
      ],
      '1/10': [
        'Getting started!',
        'First step on your art journey!',
        'One down, nine to go!',
        'A good beginning!'
      ],
      '2-4/10': [
        'Keep going! You\'re learning!',
        'Nice progress!',
        'You\'re getting the hang of it!',
        'Building momentum!',
        'Every answer teaches you something!',
        'You\'re on your way!'
      ],
      '5-6/10': [
        'Halfway there! Great work!',
        'You\'re doing really well!',
        'Impressive knowledge!',
        'You know your Norwegian art!',
        'Excellent progress!',
        'You\'re a natural!'
      ],
      '7-8/10': [
        'Outstanding performance!',
        'You\'re really good at this!',
        'Almost perfect! Amazing!',
        'You have great taste in art!',
        'Fantastic knowledge!',
        'You\'re an art expert!'
      ],
      '9/10': [
        'Incredible! Just one more!',
        'You\'re so close to perfection!',
        'Almost flawless! Outstanding!',
        'One step away from greatness!',
        'You\'re a Norwegian art master!',
        'Nearly perfect! Amazing!'
      ],
      '10/10': [
        'Perfect score! You\'re a Norwegian art expert!',
        'Flawless victory! Outstanding knowledge!',
        '100%! You know Norwegian art inside out!',
        'Perfect! You\'re a true art connoisseur!',
        'Incredible! Complete mastery!',
        'Outstanding! You\'re a Norwegian art legend!'
      ]
    },
    // Round stats
    roundStats: {
      title: 'Round Results',
      score: 'Score',
      correct: 'Correct',
      incorrect: 'Incorrect',
      artists: 'Painters featured',
      playAgain: 'Play Another Round',
      close: 'Close'
    },
    // Diploma
    diploma: {
      title: 'Certificate of Excellence',
      subtitle: 'Norwegian Art Mastery',
      achievement: 'Perfect Score Achievement',
      description: 'This certificate is awarded for achieving a perfect score of 10/10 in the Norwegian Art Quiz, demonstrating exceptional knowledge of Norwegian art history.',
      awardedTo: 'Awarded to',
      date: 'Date',
      download: 'Download the diploma',
      close: 'Close'
    },
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
    aboutTechnicalText: 'Built with modern web technologies, featuring responsive design for all devices. The quiz uses intelligent artist weighting to ensure fair representation regardless of collection size.'
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
    artists: 'Malere',
    gallery: 'Galleri',
    about: 'Om',
    language: 'Språk',
    paintings: 'malerier',
    painting: 'maleri',
    painters: 'malere',
    // Footer links
    github: 'GitHub',
    instagram: 'Instagram',
    tiktok: 'TikTok',
    // Modal buttons and labels
    selectCategory: 'Velg quiz-kategori',
    // Correct answer messages
    correctMessages: [
      'Riktig!',
      'Perfekt!',
      'Utmerket!',
      'Strålende!',
      'Fantastisk!',
      'Fremragende!',
      'Suverent!',
      'Utrolig!',
      'Vidunderlig!',
      'Spektakulært!',
      'Marveløst!',
      'Praktfullt!',
      'Magnifikt!',
      'Exceptionelt!',
      'Fantastisk!'
    ],
    // Incorrect answer messages
    incorrectMessages: [
      'Feil!',
      'Galt!',
      'Ikke helt riktig!',
      'Prøv igjen!',
      'Ikke riktig!',
      'Det er ikke det!',
      'Feil svar!',
      'Feil valg!',
      'Ikke den riktige!',
      'Det er ikke riktig!',
      'Feil kunstner!',
      'Ikke helt riktig!',
      'Feil!',
      'Feil svar!',
      'Det er ikke den!'
    ],
    // Settings modal
    settings: 'Innstillinger',
    languageLabel: 'Språk',
    english: 'Engelsk',
    norwegian: 'Norsk',
    // Round feedback messages
    roundFeedback: {
      '0/10': [
        'Ikke bekymre deg, hver ekspert var engang en nybegynner!',
        'Dette er bare starten på din kunstreise!',
        'Fortsett å lære og du blir bedre!',
        'Kunstappresiasjon tar tid å utvikle!',
        'Hvert feil svar er en læremulighet!',
        'Du bygger grunnlaget for stor kunnskap!'
      ],
      '1/10': [
        'Kom i gang!',
        'Første steg på din kunstreise!',
        'En ned, ni igjen!',
        'En god start!'
      ],
      '2-4/10': [
        'Fortsett! Du lærer!',
        'Fin fremgang!',
        'Du får taket på det!',
        'Bygger opp momentum!',
        'Hvert svar lærer deg noe!',
        'Du er på vei!'
      ],
      '5-6/10': [
        'Halvveis! Bra jobb!',
        'Du gjør det veldig bra!',
        'Imponerende kunnskap!',
        'Du kan din norske kunst!',
        'Utmerket fremgang!',
        'Du er en naturtalent!'
      ],
      '7-8/10': [
        'Fremragende prestasjon!',
        'Du er veldig flink til dette!',
        'Nesten perfekt! Fantastisk!',
        'Du har god smak i kunst!',
        'Fantastisk kunnskap!',
        'Du er en kunstekspert!'
      ],
      '9/10': [
        'Utrolig! Bare én til!',
        'Du er så nær perfeksjon!',
        'Nesten feilfri! Fremragende!',
        'Ett skritt fra storhet!',
        'Du er en norsk kunstmester!',
        'Nesten perfekt! Fantastisk!'
      ],
      '10/10': [
        'Perfekt poengsum! Du er en norsk kunstekspert!',
        'Feilfri seier! Fremragende kunnskap!',
        '100%! Du kan norsk kunst ut og inn!',
        'Perfekt! Du er en ekte kunstkjenner!',
        'Utrolig! Komplett mestring!',
        'Fremragende! Du er en norsk kunstlegende!'
      ]
    },
    // Round stats
    roundStats: {
      title: 'Runderesultat',
      score: 'Poengsum',
      correct: 'Riktig',
      incorrect: 'Feil',
      artists: 'Malere med',
      playAgain: 'Spill en ny runde',
      close: 'Lukk'
    },
    // Diploma
    diploma: {
      title: 'Eksellensbevis',
      subtitle: 'Norsk Kunstmesterskap',
      achievement: 'Perfekt Poengsum',
      description: 'Dette beviset tildeles for å oppnå en perfekt poengsum på 10/10 i Norsk Kunstquiz, som demonstrerer enestående kunnskap om norsk kunsthistorie.',
      awardedTo: 'Tildelt til',
      date: 'Dato',
      download: 'Last ned diplom',
      close: 'Lukk'
    },
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
    aboutTechnicalText: 'Bygget med moderne webteknologier, med responsivt design for alle enheter. Quizen bruker intelligent kunstnervektlegging for å sikre rettferdig representasjon uansett samlingsstørrelse.'
  }
};

// Round tracking system
let currentRound = {
  questionNumber: 1,
  correctAnswers: 0,
  incorrectAnswers: 0,
  artists: new Set(),
  answers: [] // Array to track each answer for stats
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
  // Handle nested keys like 'roundStats.title'
  const keys = key.split('.');
  let value = translations[currentLanguage];
  
  for (const k of keys) {
    if (value && typeof value === 'object' && k in value) {
      value = value[k];
    } else {
      return key; // Return the key if translation not found
    }
  }
  
  return value || key;
}

function updateLanguageUI() {
  // Update title
  const title = document.querySelector('.title');
  if (title) title.textContent = t('title');
  
  // Update category labels
  const customLink = document.getElementById('custom-category-link');
  if (customLink) {
    const category = CATEGORY_DEFS.find(cat => cat.value === selectedCategory);
    if (category) {
      customLink.textContent = t(category.label);
    }
  }
  
  // Update collection info
  updateCollectionInfo();
  

  
  // Update page title and meta description
  updatePageMeta();
  
  // Update language flag in footer
  updateLanguageFlag();
  
  // Update footer links
  updateFooterLinks();
  
  // Update category selector aria-label
  updateCategorySelector();
  
  // Render category selector
  renderCategorySelector();
  
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
  const languageToggle = document.getElementById('language-toggle');
  
  if (languageToggle) {
    languageToggle.addEventListener('click', (e) => {
      e.preventDefault();
      // Toggle between languages
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
  
  // Ensure the select has the correct value
  catSelect.value = selectedCategory;
  
  updateCollectionInfo();
  
  // Update aria-label
  catSelect.setAttribute('aria-label', t('selectCategory'));
}

function setupCategoryChangeInfoBar() {
  const catSelect = document.getElementById('category-select');
  if (catSelect) {
    catSelect.addEventListener('change', () => {
      selectedCategory = catSelect.value;
      startNewRound(); // Reset quiz completely for new category
      updateCollectionInfo();
    });
  }
}

function renderCategorySelector() {
  const catSelect = document.getElementById('category-select');
  const selectorDiv = document.querySelector('.category-selector');
  if (!catSelect || !selectorDiv) {
    console.error('Category selector elements not found:', { catSelect: !!catSelect, selectorDiv: !!selectorDiv });
    return;
  }
  catSelect.style.display = 'none';
  let custom = document.getElementById('custom-category-link');
  if (!custom) {
    custom = document.createElement('button');
    custom.id = 'custom-category-link';
    custom.className = 'custom-category-link';
    custom.type = 'button';
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
    if (menu) {
      menu.remove();
      return;
    }
    menu = document.createElement('div');
    menu.id = 'custom-category-menu';
    menu.className = 'custom-category-menu';
    options.forEach(opt => {
      const item = document.createElement('button');
      item.className = 'custom-category-item';
      item.type = 'button';
      item.textContent = t(opt.label);
      item.onclick = ev => {
        ev.stopPropagation();
        catSelect.value = opt.value;
        selectedCategory = opt.value;
        startNewRound(); // Reset quiz completely for new category
        updateCollectionInfo();
        renderCategorySelector();
        menu.remove();
      };
      menu.appendChild(item);
    });
    selectorDiv.appendChild(menu);
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
        document.removeEventListener('click', outsideClick);
      }
    }
    document.addEventListener('click', outsideClick);
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
  
  // Check if round is complete
  if (currentRound.questionNumber > 10) {
    showRoundResults();
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
      
      // Track this answer
      const isCorrect = artist === painting.artist;
      currentRound.answers.push({
        question: currentRound.questionNumber,
        correct: isCorrect,
        selectedArtist: artist,
        correctArtist: painting.artist,
        painting: painting
      });
      
      if (isCorrect) {
        // Correct answer
        currentRound.correctAnswers++;
        streak++;
        selectedBtn.classList.add('correct');
        
        // Show correct message
        const correctMessage = getRandomCorrectMessage();
        showMessage(correctMessage, '#388e3c');
        
        // Add artist to set
        currentRound.artists.add(painting.artist);
        
        // Quick transition for correct answers
        setTimeout(() => {
          hideMessage(); // Hide the correct message
          // Remove loading state and reset buttons
          Array.from(optionsDiv.children).forEach(b => {
            b.classList.remove('loading', 'correct', 'wrong');
            b.disabled = false;
          });
          currentRound.questionNumber++;
          loadQuiz();
        }, 1000);
      } else {
        // Incorrect answer
        currentRound.incorrectAnswers++;
        streak = 0;
        selectedBtn.classList.add('wrong');
        correctBtn.classList.add('correct');
        const incorrectMessage = getRandomIncorrectMessage();
        showMessage(incorrectMessage, '#e53935');
        
        // Add correct artist to set (only count the actual featured artist)
        currentRound.artists.add(painting.artist);
        
        updateStreakBar();
        setTimeout(() => {
          showArtistPopup(painting, () => {
            hideMessage();
            // Remove loading state and reset buttons
            Array.from(optionsDiv.children).forEach(b => {
              b.classList.remove('loading', 'correct', 'wrong');
              b.disabled = false;
            });
            currentRound.questionNumber++;
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
  
  // Create 10 circles for the round
  for (let i = 0; i < 10; i++) {
    const circle = document.createElement('div');
    circle.className = 'streak-circle';
    
    // Color based on round progress
    if (i < currentRound.questionNumber - 1) {
      // Check if this answer was correct or incorrect
      const answer = currentRound.answers[i];
      if (answer && answer.correct) {
        circle.classList.add('filled'); // Green for correct
      } else if (answer && !answer.correct) {
        circle.classList.add('incorrect'); // Red for incorrect
      }
    }
    
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
    
    // Use language-specific bio with proper fallback
    const bioText = currentLanguage === 'no' ? 
      (bioInfo.norwegian_bio || bioInfo.bio || '') : 
      (bioInfo.english_bio || bioInfo.bio || '');
    bioHtml = bioText ? `<span class="artist-bio">${bioText}</span>` : '';
    
    let tagList = [...(bioInfo.awards || []), ...(bioInfo.movement || []), ...(bioInfo.genre || [])];
    if (tagList.length) {
      tagsHtml = `<div class="artist-tags">${tagList.map(tag => `<span class="artist-tag">${tag}</span>`).join('')}</div>`;
    }
    bioHtml += ` <span class="artist-painting-count">(${numPaintings} ${currentLanguage === 'no' ? 'maleri' : 'painting'}${numPaintings === 1 ? '' : currentLanguage === 'no' ? 'er' : 's'})</span>`;
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
  // Click outside to close
  setTimeout(() => {
    function outsideClick(e) {
      if (!modal.querySelector('.artist-list-modal').contains(e.target)) {
        modal.style.display = 'none';
        document.removeEventListener('click', outsideClick);
      }
    }
    document.addEventListener('click', outsideClick);
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

function generateAboutContent() {
  // Get category counts dynamically
  const categoryCounts = {};
  const validPaintings = paintings.filter(p => p.artist && p.url);
  
  // Calculate category counts
  categoryCounts.all = validPaintings.length;
  
  // Popular painters (top 10)
  const artistCounts = {};
  validPaintings.forEach(p => {
    artistCounts[p.artist] = (artistCounts[p.artist] || 0) + 1;
  });
  const topArtists = Object.entries(artistCounts)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 10)
    .map(([artist]) => artist);
  categoryCounts.popular = validPaintings.filter(p => topArtists.includes(p.artist)).length;
  
  // Landscape paintings
  categoryCounts.landscape = validPaintings.filter(p => 
    (p.artist_genre && p.artist_genre.some(g => g && g.toLowerCase().includes('landscape'))) ||
    (p.genre && p.genre.some(g => g && g.toLowerCase().includes('landscape')))
  ).length;
  
  // Portraits
  categoryCounts.portraits = validPaintings.filter(p => 
    (p.artist_genre && p.artist_genre.some(g => g && g.toLowerCase().includes('portrait'))) ||
    (p.genre && p.genre.some(g => g && g.toLowerCase().includes('portrait')))
  ).length;
  
  // Women painters
  categoryCounts.women_painters = validPaintings.filter(p => p.artist_gender === 'female').length;
  
  // 19th century
  categoryCounts.nineteenthCentury = validPaintings.filter(p => {
    const bio = artistBios.find(b => b.name === p.artist);
    return bio && bio.birth_year && 1800 <= parseInt(bio.birth_year) && parseInt(bio.birth_year) < 1900;
  }).length;
  
  // 20th century
  categoryCounts.twentiethCentury = validPaintings.filter(p => {
    const bio = artistBios.find(b => b.name === p.artist);
    return bio && bio.birth_year && 1900 <= parseInt(bio.birth_year) && parseInt(bio.birth_year) < 2000;
  }).length;
  
  // Impressionism
  categoryCounts.impressionism = validPaintings.filter(p => 
    (p.artist_movement && p.artist_movement.some(m => m && m.toLowerCase().includes('impressionism'))) ||
    (p.movement && p.movement.some(m => m && m.toLowerCase().includes('impressionism')))
  ).length;
  
  // Expressionism
  categoryCounts.expressionism = validPaintings.filter(p => 
    (p.artist_movement && p.artist_movement.some(m => m && m.toLowerCase().includes('expressionism'))) ||
    (p.movement && p.movement.some(m => m && m.toLowerCase().includes('expressionism')))
  ).length;
  
  // Norwegian Romantic
  categoryCounts.norwegianRomantic = validPaintings.filter(p => 
    (p.artist_movement && p.artist_movement.some(m => 
      m && (m.toLowerCase().includes('nasjonalromantikk') || 
           m.toLowerCase().includes('norwegian romantic nationalism') ||
           m.toLowerCase().includes('romantic nationalism'))
    )) ||
    (p.movement && p.movement.some(m => 
      m && (m.toLowerCase().includes('nasjonalromantikk') || 
           m.toLowerCase().includes('norwegian romantic nationalism') ||
           m.toLowerCase().includes('romantic nationalism'))
    ))
  ).length;
  
  // Count unique artists
  const uniqueArtists = new Set(validPaintings.map(p => p.artist));
  
  // Generate content based on current language
  const content = {
    collection: {
      title: t('aboutCollection'),
      text: currentLanguage === 'no' 
        ? `Kunstquiz inneholder ${categoryCounts.all.toLocaleString()} malerier fra ${uniqueArtists.size} norske kunstnere, noe som gjør det til en av de mest omfattende norske kunstquizene tilgjengelig. Vår samling spenner fra 1800-tallet til samtidsverk, og dekker ulike bevegelser og stiler.`
        : `Kunstquiz features ${categoryCounts.all.toLocaleString()} paintings from ${uniqueArtists.size} Norwegian artists, making it one of the most comprehensive Norwegian art quizzes available. Our collection spans from the 19th century to contemporary works, covering various movements and styles.`
    },
    categories: {
      title: t('aboutCategories'),
      items: [
        { label: t('fullCollection'), count: categoryCounts.all, suffix: currentLanguage === 'no' ? 'malerier' : 'paintings' },
        { label: t('popularPainters'), count: categoryCounts.popular, suffix: currentLanguage === 'no' ? 'verk' : 'works' },
        { label: t('landscapePainting'), count: categoryCounts.landscape, suffix: currentLanguage === 'no' ? 'landskapsverk' : 'landscape works' },
        { label: t('portraits'), count: categoryCounts.portraits, suffix: currentLanguage === 'no' ? 'portrettmalerier' : 'portrait paintings' },
        { label: t('womenPainters'), count: categoryCounts.women_painters, suffix: currentLanguage === 'no' ? 'verk av kvinnelige kunstnere' : 'works by female artists' },
        { label: t('impressionism'), count: categoryCounts.impressionism, suffix: currentLanguage === 'no' ? 'impressionistiske verk' : 'impressionist works' },
        { label: t('expressionism'), count: categoryCounts.expressionism, suffix: currentLanguage === 'no' ? 'ekspresjonistiske malerier' : 'expressionist paintings' },
        { label: t('norwegianRomantic'), count: categoryCounts.norwegianRomantic, suffix: currentLanguage === 'no' ? 'romantisk nasjonalistiske verk' : 'romantic nationalist works' }
      ]
    },
    howToPlay: {
      title: t('aboutHowToPlay'),
      text: t('aboutHowToPlayText')
    },
    facts: {
      title: t('aboutFacts'),
      items: currentLanguage === 'no' ? [
        'Data hentet fra åpne Wikimedia og Wikidata APIer',
        'Inneholder 33 ulike kunstgenrer inkludert landskap, portrett og abstrakt maleri',
        'Inkluderer 7 store kunstbevegelser fra impressionisme til samtidskunst',
        'Samlingen spenner over 200 år med norsk kunsthistorie',
        'Alle bilder er fritt tilgjengelige under åpne lisenser'
      ] : [
        'Data sourced from open Wikimedia and Wikidata APIs',
        'Features 33 different art genres including landscape, portrait, and abstract painting',
        'Includes 7 major art movements from Impressionism to Contemporary art',
        'Collection spans over 200 years of Norwegian art history',
        'All images are freely available under open licenses'
      ]
    },
    technical: {
      title: t('aboutTechnical'),
      text: t('aboutTechnicalText')
    }
  };
  
  return content;
}

function showAboutModal() {
  const modal = document.getElementById('about-modal');
  const title = document.getElementById('about-title');
  const aboutContent = document.getElementById('about-content');
  
  if (!modal) return;
  
  // Update title
  title.textContent = t('aboutTitle');
  
  // Generate dynamic content
  const content = generateAboutContent();
  
  // Clear existing content
  aboutContent.innerHTML = '';
  
  // Collection section
  const collectionSection = document.createElement('div');
  collectionSection.className = 'about-section';
  collectionSection.innerHTML = `
    <h3>${content.collection.title}</h3>
    <p>${content.collection.text}</p>
  `;
  aboutContent.appendChild(collectionSection);
  
  // Categories section
  const categoriesSection = document.createElement('div');
  categoriesSection.className = 'about-section';
  const categoriesList = content.categories.items.map(item => 
    `<li><strong>${item.label}:</strong> ${item.count.toLocaleString()} ${item.suffix}</li>`
  ).join('');
  categoriesSection.innerHTML = `
    <h3>${content.categories.title}</h3>
    <ul>${categoriesList}</ul>
  `;
  aboutContent.appendChild(categoriesSection);
  
  // How to play section
  const howToPlaySection = document.createElement('div');
  howToPlaySection.className = 'about-section';
  howToPlaySection.innerHTML = `
    <h3>${content.howToPlay.title}</h3>
    <p>${content.howToPlay.text}</p>
  `;
  aboutContent.appendChild(howToPlaySection);
  
  // Facts section
  const factsSection = document.createElement('div');
  factsSection.className = 'about-section';
  const factsList = content.facts.items.map(fact => `<li>${fact}</li>`).join('');
  factsSection.innerHTML = `
    <h3>${content.facts.title}</h3>
    <ul>${factsList}</ul>
  `;
  aboutContent.appendChild(factsSection);
  
  // Technical section
  const technicalSection = document.createElement('div');
  technicalSection.className = 'about-section';
  technicalSection.innerHTML = `
    <h3>${content.technical.title}</h3>
    <p>${content.technical.text}</p>
  `;
  aboutContent.appendChild(technicalSection);
  
  modal.style.display = 'flex';
  modal.focus();
  
  // Add click outside to close
  setTimeout(() => {
    function outsideClick(e) {
      if (!modal.querySelector('.about-modal-content').contains(e.target)) {
        hideAboutModal();
        document.removeEventListener('click', outsideClick);
      }
    }
    document.addEventListener('click', outsideClick);
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



function getRandomCorrectMessage() {
  const messages = translations[currentLanguage].correctMessages;
  const randomIndex = Math.floor(Math.random() * messages.length);
  return messages[randomIndex];
}

function getRandomIncorrectMessage() {
  const messages = translations[currentLanguage].incorrectMessages;
  const randomIndex = Math.floor(Math.random() * messages.length);
  return messages[randomIndex];
}

function getRandomRoundFeedback(score) {
  let category;
  if (score === 0) category = '0/10';
  else if (score === 1) category = '1/10';
  else if (score >= 2 && score <= 4) category = '2-4/10';
  else if (score >= 5 && score <= 6) category = '5-6/10';
  else if (score >= 7 && score <= 8) category = '7-8/10';
  else if (score === 9) category = '9/10';
  else category = '10/10';
  
  const messages = translations[currentLanguage].roundFeedback[category];
  const randomIndex = Math.floor(Math.random() * messages.length);
  return messages[randomIndex];
}

function showRoundResults() {
  const modal = document.getElementById('round-results-modal');
  const title = document.getElementById('round-results-title');
  const score = document.getElementById('round-results-score');
  const artistsList = document.getElementById('round-results-artists-list');
  const feedback = document.getElementById('round-results-feedback');
  const playAgainBtn = document.getElementById('round-results-play-again');
  const downloadBtn = document.getElementById('round-results-download');
  
  if (!modal) return;
  
  const totalCorrect = currentRound.correctAnswers;
  const uniqueArtists = [...currentRound.artists].sort();
  
  // For perfect scores, go directly to diploma
  if (totalCorrect === 10) {
    showDiploma();
    return;
  }
  
  // Update content with proper translations
  title.textContent = t('roundStats.title');
  score.textContent = `${totalCorrect}/10`;
  
  // Populate artists list
  artistsList.innerHTML = '';
  uniqueArtists.forEach(artist => {
    const artistTag = document.createElement('span');
    artistTag.className = 'artist-tag-small';
    artistTag.textContent = artist;
    artistsList.appendChild(artistTag);
  });
  
  feedback.textContent = getRandomRoundFeedback(totalCorrect);
  playAgainBtn.textContent = t('roundStats.playAgain');
  
  // Show modal
  modal.style.display = 'flex';
  modal.focus();
  
  // Setup event listeners
  playAgainBtn.onclick = () => {
    hideRoundResults();
    startNewRound();
  };
  
  // Click outside to close
  setTimeout(() => {
    function outsideClick(e) {
      if (!modal.querySelector('.round-results-content').contains(e.target)) {
        hideRoundResults();
        document.removeEventListener('click', outsideClick);
      }
    }
    document.addEventListener('click', outsideClick);
  }, 100);
}

function hideRoundResults() {
  const modal = document.getElementById('round-results-modal');
  if (modal) modal.style.display = 'none';
}

function showDiploma() {
  const modal = document.getElementById('diploma-modal');
  const title = document.getElementById('diploma-title');
  const subtitle = document.getElementById('diploma-subtitle');
  const achievement = document.getElementById('diploma-achievement-text');
  const description = document.getElementById('diploma-description-text');
  const awardedLabel = document.getElementById('diploma-awarded-label');
  const awardedValue = document.getElementById('diploma-awarded-value');
  const dateLabel = document.getElementById('diploma-date-label');
  const dateValue = document.getElementById('diploma-date-value');
  const downloadBtn = document.getElementById('diploma-download');
  const playAgainBtn = document.getElementById('diploma-play-again');
  const paintingBg = document.querySelector('.diploma-painting-bg');
  
  if (!modal) return;
  
  // Set dynamic background painting from current round
  let backgroundPainting = null;
  if (paintingBg && currentRound.artists.size > 0) {
    // Get a random painting from the current round
    const roundPaintings = paintings.filter(p => currentRound.artists.has(p.artist));
    if (roundPaintings.length > 0) {
      backgroundPainting = roundPaintings[Math.floor(Math.random() * roundPaintings.length)];
      paintingBg.style.backgroundImage = `url(${backgroundPainting.image})`;
      paintingBg.style.backgroundSize = 'cover';
      paintingBg.style.backgroundPosition = 'center';
      paintingBg.style.backgroundRepeat = 'no-repeat';
      paintingBg.style.opacity = '0.15';
      
      // Add artist attribution to the background
      paintingBg.setAttribute('data-artist', backgroundPainting.artist);
      paintingBg.setAttribute('title', `Background: ${backgroundPainting.artist}`);
      
      // Set artist attribution text
      const artistAttribution = document.querySelector('.diploma-artist-attribution');
      if (artistAttribution) {
        artistAttribution.textContent = `Background: ${backgroundPainting.artist}`;
        setTimeout(() => {
          artistAttribution.classList.add('visible');
        }, 1000);
      }
      
      // Make background clickable to show full painting
      const diplomaBackground = document.querySelector('.diploma-background');
      if (diplomaBackground && backgroundPainting) {
        diplomaBackground.style.cursor = 'pointer';
        diplomaBackground.onclick = () => {
          showArtistPopup(backgroundPainting, () => {
            // Return to diploma after closing popup
            showDiploma();
          });
        };
        diplomaBackground.title = `Click to view: ${backgroundPainting.title} by ${backgroundPainting.artist}`;
      }
    }
  }
  
  // Update content with translations
  title.textContent = t('diploma.title');
  subtitle.textContent = t('diploma.subtitle');
  achievement.textContent = t('diploma.achievement');
  description.textContent = t('diploma.description');
  awardedLabel.textContent = t('diploma.awardedTo');
  dateLabel.textContent = t('diploma.date');
  downloadBtn.textContent = t('diploma.download');
  playAgainBtn.textContent = t('playAgain');
  
  // Set awardee name (you could make this customizable)
  awardedValue.textContent = 'Art Enthusiast';
  
  // Set current date
  const now = new Date();
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  dateValue.textContent = now.toLocaleDateString(currentLanguage === 'no' ? 'nb-NO' : 'en-US', options);
  
  // Show modal
  modal.style.display = 'flex';
  modal.focus();
  
  // Setup event listeners
  downloadBtn.onclick = downloadDiploma;
  playAgainBtn.onclick = () => {
    hideDiploma();
    startNewRound();
  };
  
  // Click outside to close
  setTimeout(() => {
    function outsideClick(e) {
      if (!modal.querySelector('.diploma-content').contains(e.target)) {
        hideDiploma();
        document.removeEventListener('click', outsideClick);
      }
    }
    document.addEventListener('click', outsideClick);
  }, 100);
}

function hideDiploma() {
  const modal = document.getElementById('diploma-modal');
  if (modal) modal.style.display = 'none';
}

function downloadDiploma() {
  const diplomaContainer = document.querySelector('.diploma-container');
  if (!diplomaContainer) return;
  
  // Use html2canvas to capture the diploma
  if (typeof html2canvas !== 'undefined') {
    html2canvas(diplomaContainer, {
      scale: 2,
      backgroundColor: null,
      useCORS: true,
      allowTaint: true
    }).then(canvas => {
      // Create download link
      const link = document.createElement('a');
      link.download = `kunstquiz-diploma-${new Date().toISOString().split('T')[0]}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    });
  } else {
    // Fallback: prompt user to take screenshot
    alert('Please take a screenshot of your diploma!');
  }
}

function startNewRound() {
  currentRound = {
    questionNumber: 1,
    correctAnswers: 0,
    incorrectAnswers: 0,
    artists: new Set(),
    answers: []
  };
  streak = 0;
  updateStreakBar();
  loadQuiz();
}

function updatePageMeta() {
  // Update HTML lang attribute
  const htmlElement = document.getElementById('html-element');
  if (htmlElement) {
    htmlElement.lang = currentLanguage === 'no' ? 'no' : 'en';
  }
  
  // Update page title
  if (currentLanguage === 'no') {
    document.title = 'Kunstquiz - Norsk Kunstutfordring';
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
      metaDesc.content = 'En morsom quiz hvor du gjetter kunstneren bak berømte norske malerier. Test din kunnskap om norsk kunsthistorie!';
    }
  } else {
    document.title = 'Kunstquiz - Norwegian Art Challenge';
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
      metaDesc.content = 'A fun quiz where you guess the artist behind famous Norwegian paintings. Test your knowledge of Norwegian art history!';
    }
  }
}

function updateLanguageFlag() {
  const languageToggle = document.getElementById('language-toggle');
  if (languageToggle) {
    languageToggle.textContent = currentLanguage === 'no' ? '🇳🇴' : '🇬🇧';
  }
}

function updateFooterLinks() {
  // Update footer link texts
  const artistsLink = document.getElementById('show-artists-link');
  if (artistsLink) artistsLink.textContent = t('artists');
  
  const galleryLink = document.getElementById('show-gallery-link');
  if (galleryLink) galleryLink.textContent = t('gallery');
  
  const aboutLink = document.getElementById('show-about-link');
  if (aboutLink) aboutLink.textContent = t('about');
}

function updateCategorySelector() {
  const categorySelect = document.getElementById('category-select');
  if (categorySelect) {
    categorySelect.setAttribute('aria-label', t('selectCategory'));
  }
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
    updateLanguageUI();
    setupLanguageToggle();
    startNewRound(); // Start with a new round
    setupArtistModal();
    setupGalleryModal();
    setupAboutModal();
    setupLogoReset();
    setupCategoryChangeInfoBar();
    
    // Ensure category selector is properly rendered
    console.log('Rendering category selector...');
    renderCategorySelector();
    console.log('Category selector rendered');
    
    // Test category selector
    setTimeout(() => {
      const customLink = document.getElementById('custom-category-link');
      const selectorDiv = document.querySelector('.category-selector');
      console.log('Category selector test:', {
        customLink: !!customLink,
        selectorDiv: !!selectorDiv,
        customLinkText: customLink?.textContent,
        selectorDivChildren: selectorDiv?.children?.length
      });
    }, 1000);
    
    const resetBtn = document.getElementById('reset-btn');
    if (resetBtn) resetBtn.addEventListener('click', () => {
      streak = 0;
      updateStreakBar();
      hideCongratsModal();
      startNewRound();
    });
    
    // Add Esc key to close modals
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') {
        hideCongratsModal();
        hideGalleryModal();
        hideAboutModal();
        hideRoundResults();
        document.getElementById('artists-modal').style.display = 'none';
      }
    });
  } catch (err) {
    console.error('Error loading data:', err);
    document.getElementById('options').innerHTML = `<p>${t('errorLoading')}</p>`;
  }
});