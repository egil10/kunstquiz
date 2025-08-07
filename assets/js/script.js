'use strict';

// Performance optimizations
const PERFORMANCE_CONFIG = {
  // Image preloading
  PRELOAD_COUNT: 5,
  PRELOAD_DELAY: 100,
  
  // Memory management
  MAX_CACHE_SIZE: 50,
  CLEANUP_INTERVAL: 30000, // 30 seconds
  
  // Animation throttling
  ANIMATION_THROTTLE: 16, // ~60fps
  
  // DOM updates batching
  BATCH_DELAY: 10
};

// Global performance variables
let preloadQueue = [];
let cleanupTimer = null;
let animationFrameId = null;
let batchUpdateTimer = null;
let pendingUpdates = new Set();

// Performance monitoring
const performanceMetrics = {
  startTime: Date.now(),
  operations: 0,
  cacheHits: 0,
  cacheMisses: 0
};

// Memory management
const memoryCache = new Map();
const imageCache = new Map();
const domCache = new Map();

// Throttled function wrapper
function throttle(func, delay) {
  let lastCall = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastCall >= delay) {
      lastCall = now;
      return func.apply(this, args);
    }
  };
}

// Debounced function wrapper
function debounce(func, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func.apply(this, args), delay);
  };
}

// Efficient DOM updates
function batchDOMUpdates() {
  if (batchUpdateTimer) return;
  
  batchUpdateTimer = requestAnimationFrame(() => {
    pendingUpdates.forEach(update => update());
    pendingUpdates.clear();
    batchUpdateTimer = null;
  });
}

// Memory cleanup
function cleanupMemory() {
  // Clear old cache entries
  if (memoryCache.size > PERFORMANCE_CONFIG.MAX_CACHE_SIZE) {
    const entries = Array.from(memoryCache.entries());
    const toDelete = entries.slice(0, entries.length - PERFORMANCE_CONFIG.MAX_CACHE_SIZE);
    toDelete.forEach(([key]) => memoryCache.delete(key));
  }
  
  // Clear old image cache
  if (imageCache.size > PERFORMANCE_CONFIG.MAX_CACHE_SIZE) {
    const entries = Array.from(imageCache.entries());
    const toDelete = entries.slice(0, entries.length - PERFORMANCE_CONFIG.MAX_CACHE_SIZE);
    toDelete.forEach(([key]) => imageCache.delete(key));
  }
  
  // Clear old DOM cache
  if (domCache.size > PERFORMANCE_CONFIG.MAX_CACHE_SIZE) {
    const entries = Array.from(domCache.entries());
    const toDelete = entries.slice(0, entries.length - PERFORMANCE_CONFIG.MAX_CACHE_SIZE);
    toDelete.forEach(([key]) => domCache.delete(key));
  }
  
  // Force garbage collection if available
  if (window.gc) {
    window.gc();
  }
}

// Start periodic cleanup
function startMemoryCleanup() {
  if (cleanupTimer) clearInterval(cleanupTimer);
  cleanupTimer = setInterval(cleanupMemory, PERFORMANCE_CONFIG.CLEANUP_INTERVAL);
}

// Performance monitoring function
function getPerformanceMetrics() {
  const uptime = Date.now() - performanceMetrics.startTime;
  const memoryUsage = performance.memory ? {
    used: Math.round(performance.memory.usedJSHeapSize / 1024 / 1024),
    total: Math.round(performance.memory.totalJSHeapSize / 1024 / 1024),
    limit: Math.round(performance.memory.jsHeapSizeLimit / 1024 / 1024)
  } : null;
  
  return {
    uptime: Math.round(uptime / 1000),
    operations: performanceMetrics.operations,
    cacheHits: performanceMetrics.cacheHits,
    cacheMisses: performanceMetrics.cacheMisses,
    cacheHitRate: performanceMetrics.cacheHits / (performanceMetrics.cacheHits + performanceMetrics.cacheMisses) || 0,
    memoryUsage,
    imageCacheSize: imageCache.size,
    memoryCacheSize: memoryCache.size,
    domCacheSize: domCache.size
  };
}

// Debug function to log performance metrics
function logPerformanceMetrics() {
  const metrics = getPerformanceMetrics();
  console.log('🎯 Performance Metrics:', metrics);
  return metrics;
}

// Image optimization monitoring
const imageOptimizationMetrics = {
  totalImages: 0,
  optimizedImages: 0,
  webpImages: 0,
  fallbackImages: 0,
  averageLoadTime: 0,
  loadTimes: []
};

function logImageOptimizationMetrics() {
  const avgLoadTime = imageOptimizationMetrics.loadTimes.length > 0 
    ? imageOptimizationMetrics.loadTimes.reduce((a, b) => a + b, 0) / imageOptimizationMetrics.loadTimes.length
    : 0;
    
  console.log('🖼️ Image Optimization Metrics:', {
    totalImages: imageOptimizationMetrics.totalImages,
    optimizedImages: imageOptimizationMetrics.optimizedImages,
    webpImages: imageOptimizationMetrics.webpImages,
    fallbackImages: imageOptimizationMetrics.fallbackImages,
    averageLoadTime: `${avgLoadTime.toFixed(2)}ms`,
    optimizationRate: `${(imageOptimizationMetrics.optimizedImages / imageOptimizationMetrics.totalImages * 100).toFixed(1)}%`
  });
}

// Language support
let currentLanguage = 'en'; // 'en' for English, 'no' for Norwegian
const translations = {
  en: {
    title: 'Kunstquiz',
    collectionInfo: 'paintings, painters',
    fullCollection: 'Full Collection',
    popularPainters: 'Popular Painters',
    landscape: 'Landscape',
    realism: 'Realism',
    impressionism: 'Impressionism',
    expressionism: 'Expressionism',
    romanticNationalism: 'Romantic Nationalism',
    femaleArtists: 'Female Artists',
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
    about: 'About',
    aboutTitle: 'About',
    language: 'Language',
    paintings: 'paintings',
    painting: 'painting',
    painters: 'Painters',
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
      category: 'Category',
      date: 'Date',
      download: 'Download the diploma',
      close: 'Close'
    },
    // About modal translations
    aboutTitle: 'About Kunstquiz',
    aboutCollection: 'The Collection',
    aboutCollectionText: 'Kunstquiz features 3,282 paintings from 81 Norwegian artists, making it one of the most comprehensive Norwegian art quizzes available. Our collection spans from the 19th century to contemporary works, covering various movements and styles.',
    aboutCategories: 'Quiz Categories',
    aboutCategoriesText: 'Full Collection: All paintings, Popular Painters: Top 10 artists by painting count, Landscape: Landscape paintings (34 artists), Realism: Realist movement (15 artists), Impressionism: Impressionist paintings (12 artists), Expressionism: Expressionist paintings (8 artists), Romantic Nationalism: Norwegian romantic nationalism (10 artists), Female Artists: Female painters (4 artists)',
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
    landscape: 'Landskap',
    realism: 'Realisme',
    impressionism: 'Impressionisme',
    expressionism: 'Ekspresjonisme',
    romanticNationalism: 'Romantisk Nasjonalisme',
    femaleArtists: 'Kvinnelige Kunstnere',
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
    about: 'Om',
    aboutTitle: 'Om',
    language: 'Språk',
    paintings: 'malerier',
    painting: 'maleri',
    painters: 'Malere',
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
      category: 'Kategori',
      date: 'Dato',
      download: 'Last ned diplom',
      close: 'Lukk'
    },
    // About modal translations
    aboutTitle: 'Om Kunstquiz',
    aboutCollection: 'Samlingen',
    aboutCollectionText: 'Kunstquiz inneholder 3,282 malerier fra 81 norske kunstnere, noe som gjør det til en av de mest omfattende norske kunstquizene tilgjengelig. Vår samling spenner fra 1800-tallet til samtidsverk, og dekker ulike bevegelser og stiler.',
    aboutCategories: 'Quiz-kategorier',
    aboutCategoriesText: 'Full Samling: Alle malerier, Populære Malere: Topp 10 kunstnere etter antall malerier, Landskap: Landskapsmalerier (34 kunstnere), Realisme: Realistisk bevegelse (15 kunstnere), Impressionisme: Impressionistiske malerier (12 kunstnere), Ekspresjonisme: Ekspresjonistiske malerier (8 kunstnere), Romantisk Nasjonalisme: Norsk romantisk nasjonalisme (10 kunstnere), Kvinnelige Kunstnere: Kvinnelige malere (4 kunstnere)',
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

// Performance optimizations
let validPaintingsCache = null;
let validPaintingsCacheCategory = null;
let artistBioMapCache = null;
let categoryCountsCache = new Map();
let imagePreloadQueue = [];
let isPreloading = false;

// Encouraging message counter
let encouragingMessageIndex = 0;

let streak = 0;
let paintings = [];
let lastPaintingIndex = -1;
let selectedCategory = 'all';
let artistBios = [];
let currentPainting = null;

// Analytics tracking
let analyticsData = {
  sessionStart: Date.now(),
  totalCorrect: 0,
  totalIncorrect: 0,
  perfectScores: 0,
  gamesPlayed: 0,
  categoryUsage: {},
  sessionDuration: 0
};

// Analytics tracking functions
function trackEvent(eventName, parameters = {}) {
  if (typeof gtag !== 'undefined') {
    gtag('event', eventName, {
      ...parameters,
      custom_parameter_1: 'game_events',
      custom_parameter_2: 'quiz_metrics'
    });
  }
}

function trackGameStart() {
  analyticsData.gamesPlayed++;
  trackEvent('game_start', {
    category: selectedCategory,
    games_played: analyticsData.gamesPlayed
  });
}

function trackAnswer(isCorrect, artist, category) {
  if (isCorrect) {
    analyticsData.totalCorrect++;
  } else {
    analyticsData.totalIncorrect++;
  }
  
  trackEvent('answer_submitted', {
    correct: isCorrect,
    artist: artist,
    category: category,
    total_correct: analyticsData.totalCorrect,
    total_incorrect: analyticsData.totalIncorrect,
    accuracy_rate: analyticsData.totalCorrect / (analyticsData.totalCorrect + analyticsData.totalIncorrect)
  });
}

function trackPerfectScore() {
  analyticsData.perfectScores++;
  trackEvent('perfect_score', {
    perfect_scores: analyticsData.perfectScores,
    category: selectedCategory
  });
}

function trackCategoryChange(newCategory) {
  analyticsData.categoryUsage[newCategory] = (analyticsData.categoryUsage[newCategory] || 0) + 1;
  trackEvent('category_changed', {
    new_category: newCategory,
    category_usage: analyticsData.categoryUsage
  });
}

function trackSessionEnd() {
  analyticsData.sessionDuration = Date.now() - analyticsData.sessionStart;
  trackEvent('session_end', {
    session_duration: analyticsData.sessionDuration,
    total_correct: analyticsData.totalCorrect,
    total_incorrect: analyticsData.totalIncorrect,
    games_played: analyticsData.gamesPlayed,
    perfect_scores: analyticsData.perfectScores
  });
}

// Track page visibility changes for session duration
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    trackSessionEnd();
  }
});

// Track before user leaves the page
window.addEventListener('beforeunload', () => {
  trackSessionEnd();
});

// List of categories with consistent labels - Updated based on actual data
const CATEGORY_DEFS = [
  { value: 'all', label: 'fullCollection' },
  { value: 'popular', label: 'popularPainters' },
  { value: 'landscape', label: 'landscape' },
  { value: 'realism', label: 'realism' },
  { value: 'expressionism', label: 'expressionism' },
  { value: 'impressionism', label: 'impressionism' },
  { value: 'romantic_nationalism', label: 'romanticNationalism' },
  { value: 'female_artists', label: 'femaleArtists' }
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
  
  const howToPlayTitle = document.getElementById('how-to-play-title');
  if (howToPlayTitle) howToPlayTitle.textContent = t('aboutHowToPlay');
  
  const closeArtistsBtn = document.getElementById('close-artists-modal');
  if (closeArtistsBtn) closeArtistsBtn.textContent = t('close');
  
  const closeGalleryBtn = document.getElementById('close-gallery-modal');
  if (closeGalleryBtn) closeGalleryBtn.textContent = t('close');
  
  const closeHowToPlayBtn = document.getElementById('close-how-to-play-modal');
  if (closeHowToPlayBtn) closeHowToPlayBtn.textContent = t('close');
  
  // Update round results modal elements
  const roundResultsTitle = document.getElementById('round-results-title');
  if (roundResultsTitle) roundResultsTitle.textContent = t('roundStats.title');
  
  const roundResultsScoreLabel = document.querySelector('#round-results-modal .stat-label');
  if (roundResultsScoreLabel) roundResultsScoreLabel.textContent = t('roundStats.score') + ':';
  
  const roundResultsArtistsLabel = document.querySelector('#round-results-artists .stat-label');
  if (roundResultsArtistsLabel) roundResultsArtistsLabel.textContent = t('roundStats.artists') + ':';
  
  const roundResultsPlayAgainBtn = document.getElementById('round-results-play-again');
  if (roundResultsPlayAgainBtn) roundResultsPlayAgainBtn.textContent = t('roundStats.playAgain');
  
  // Update diploma modal elements
  const diplomaTitle = document.getElementById('diploma-title');
  if (diplomaTitle) diplomaTitle.textContent = t('diploma.title');
  
  const diplomaSubtitle = document.getElementById('diploma-subtitle');
  if (diplomaSubtitle) diplomaSubtitle.textContent = t('diploma.subtitle');
  
  const diplomaAchievement = document.getElementById('diploma-achievement-text');
  if (diplomaAchievement) diplomaAchievement.textContent = t('diploma.achievement');
  
  const diplomaDescription = document.getElementById('diploma-description-text');
  if (diplomaDescription) {
    const categoryNameForDesc = selectedCategory === 'all' ? t('fullCollection') : t(CATEGORY_DEFS.find(cat => cat.value === selectedCategory)?.label || 'fullCollection');
    const descriptionWithCategory = t('diploma.description') + (selectedCategory !== 'all' ? ` (${categoryNameForDesc})` : '');
    diplomaDescription.textContent = descriptionWithCategory;
  }
  
  const diplomaAwardedLabel = document.getElementById('diploma-awarded-label');
  if (diplomaAwardedLabel) diplomaAwardedLabel.textContent = t('diploma.awardedTo') + ':';
  
  const diplomaCategoryLabel = document.getElementById('diploma-category-label');
  if (diplomaCategoryLabel) diplomaCategoryLabel.textContent = t('diploma.category') + ':';
  
  const diplomaDateLabel = document.getElementById('diploma-date-label');
  if (diplomaDateLabel) diplomaDateLabel.textContent = t('diploma.date') + ':';
  
  const diplomaDownloadBtn = document.getElementById('diploma-download');
  if (diplomaDownloadBtn) diplomaDownloadBtn.textContent = t('diploma.download');
  
  const diplomaPlayAgainBtn = document.getElementById('diploma-play-again');
  if (diplomaPlayAgainBtn) diplomaPlayAgainBtn.textContent = t('playAgain');
  
  // Update diploma category and date values
  const diplomaCategoryValue = document.getElementById('diploma-category-value');
  if (diplomaCategoryValue) {
    const categoryName = selectedCategory === 'all' ? t('fullCollection') : t(CATEGORY_DEFS.find(cat => cat.value === selectedCategory)?.label || 'fullCollection');
    diplomaCategoryValue.textContent = categoryName;
  }
  
  const diplomaDateValue = document.getElementById('diploma-date-value');
  if (diplomaDateValue) {
    const now = new Date();
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    diplomaDateValue.textContent = now.toLocaleDateString(currentLanguage === 'no' ? 'nb-NO' : 'en-US', options);
  }
  
  const diplomaAwardedValue = document.getElementById('diploma-awarded-value');
  if (diplomaAwardedValue) {
    diplomaAwardedValue.textContent = 'Art Enthusiast';
  }
  
  // Update artist gallery text if any galleries are open
  const artistGalleries = document.querySelectorAll('.artist-gallery-section');
  artistGalleries.forEach(gallery => {
    const title = gallery.querySelector('.artist-gallery-title');
    if (title) {
      title.textContent = currentLanguage === 'no' ? 'Malerier' : 'Paintings';
    }
    
    const loadMoreBtn = gallery.querySelector('.artist-gallery-load-more');
    if (loadMoreBtn) {
      const total = parseInt(loadMoreBtn.dataset.total);
      const loaded = parseInt(loadMoreBtn.dataset.loaded);
      const remaining = total - loaded;
      if (remaining > 0) {
        loadMoreBtn.textContent = `${currentLanguage === 'no' ? 'Vis flere' : 'Load More'} (${remaining})`;
      } else {
        loadMoreBtn.style.display = 'none';
      }
    }
  });
  
  // Also update any artist popups that might be open
  const artistPopups = document.querySelectorAll('.artist-popup.toast.persistent');
  artistPopups.forEach(popup => {
    // Update close button
    const closeBtn = popup.querySelector('.persistent-popup-close-btn');
    if (closeBtn) {
      closeBtn.textContent = t('close');
      closeBtn.setAttribute('aria-label', t('close'));
    }
    
    const gallery = popup.querySelector('.artist-gallery-section');
    if (gallery) {
      const title = gallery.querySelector('.artist-gallery-title');
      if (title) {
        title.textContent = currentLanguage === 'no' ? 'Malerier' : 'Paintings';
      }
      
      const loadMoreBtn = gallery.querySelector('.artist-gallery-load-more');
      if (loadMoreBtn) {
        const total = parseInt(loadMoreBtn.dataset.total);
        const loaded = parseInt(loadMoreBtn.dataset.loaded);
        const remaining = total - loaded;
        if (remaining > 0) {
          loadMoreBtn.textContent = `${currentLanguage === 'no' ? 'Vis flere' : 'Load More'} (${remaining})`;
        } else {
          loadMoreBtn.style.display = 'none';
        }
      }
    }
  });
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
  
  // Calculate balanced weights using a more gentle scaling approach
  // This provides a middle ground between pure random and extreme inverse weighting
  const maxCount = Math.max(...Object.values(artistCounts));
  const minCount = Math.min(...Object.values(artistCounts));
  
  Object.keys(artistCounts).forEach(artist => {
    const count = artistCounts[artist];
    
    // Use a more gentle scaling: cube root instead of square root
    // This makes the weighting even less aggressive
    const baseWeight = Math.pow(maxCount, 1/3) / Math.pow(count, 1/3);
    
    // Add a very small bonus for very small collections (1-2 paintings) to ensure they appear occasionally
    const smallCollectionBonus = count <= 2 ? 1.2 : 1.0;
    
    // Apply a cap to prevent extreme weighting differences
    const cappedWeight = Math.min(baseWeight * smallCollectionBonus, 3.0);
    
    artistWeights.set(artist, cappedWeight);
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
    if (lastSelectedArtists.size > 3) {
      // Keep only last 3 artists (reduced from 5 for more variety)
      const artistsArray = Array.from(lastSelectedArtists);
      lastSelectedArtists = new Set(artistsArray.slice(-3));
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
  // Use cache if available
  const cacheKey = categoryValue || 'all';
  if (categoryCountsCache.has(cacheKey)) {
    return categoryCountsCache.get(cacheKey);
  }
  
  let filtered = paintings.filter(p => p.artist && p.url);
  if (categoryValue && categoryValue !== 'all') {
    const prev = selectedCategory;
    selectedCategory = categoryValue;
    filtered = getValidPaintings();
    selectedCategory = prev;
  }
  const count = filtered.length;
  const painterCount = new Set(filtered.map(p => p.artist)).size;
  const result = { count, painterCount };
  
  // Cache the result
  categoryCountsCache.set(cacheKey, result);
  return result;
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
  
  // Clear caches when category dropdown is updated
  clearCaches();
  
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
      const newCategory = catSelect.value;
      trackCategoryChange(newCategory);
      selectedCategory = newCategory;
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
    } else {
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
          trackCategoryChange(opt.value);
          selectedCategory = opt.value;
          startNewRound(); // Reset quiz completely for new category
          updateCollectionInfo();
          renderCategorySelector();
          menu.remove();
        };
        menu.appendChild(item);
      });
      custom.appendChild(menu);
      document.addEventListener('click', () => {
        if (menu) menu.remove();
      }, { once: true });
    }
  };
  
  // Add mobile-specific touch support without affecting web
  if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
    // Only add touch events on mobile devices
    custom.addEventListener('touchend', e => {
      e.preventDefault();
      e.stopPropagation();
      // Trigger the same logic as onclick
      custom.onclick(e);
    });
  }
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

// Gallery state management
let galleryPaintings = [];
let galleryLoadedCount = 0;
let galleryLoadingMore = false;

function showGalleryModal(paintingsArray = null, initialCount = 12) {
  const modal = document.getElementById('gallery-modal');
  const collage = document.getElementById('gallery-collage');
  if (!modal || !collage) return;
  
  // Initialize gallery state
  if (paintingsArray) {
    galleryPaintings = paintingsArray;
    galleryLoadedCount = initialCount;
  } else {
    // Fallback for direct calls
    galleryPaintings = [...paintings];
    shuffleArray(galleryPaintings);
    galleryLoadedCount = initialCount;
  }
  
  collage.innerHTML = '';
  const grid = document.createElement('div');
  grid.className = 'gallery-collage-grid';
  
  // Add initial batch of images
  for (let i = 0; i < galleryLoadedCount; i++) {
    const p = galleryPaintings[i];
    if (p) {
      const img = createGalleryImage(p);
      grid.appendChild(img);
    }
  }
  
  collage.appendChild(grid);
  modal.style.display = 'flex';
  modal.focus();
  
  // Setup scroll-based loading
  setupGalleryScrollLoading(modal, grid);
  
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

function createGalleryImage(painting) {
  const img = document.createElement('img');
  // Use preloaded URL if available, otherwise fallback to optimized URL
  const preloadedUrl = galleryPreloadCache.get(painting.url);
  img.src = preloadedUrl || optimizeImageUrl(painting.url, 400);
  img.alt = painting.title || '';
  img.className = 'gallery-collage-img';
  img.loading = 'eager';
  return img;
}

function setupGalleryScrollLoading(modal, grid) {
  const modalContent = modal.querySelector('.gallery-modal-content');
  let loadingMore = false;
  
  const loadMoreImages = async () => {
    if (loadingMore || galleryLoadingMore) return;
    
    const scrollPosition = modalContent.scrollTop + modalContent.clientHeight;
    const scrollHeight = modalContent.scrollHeight;
    
    // Load more when user is near the bottom (within 200px)
    if (scrollHeight - scrollPosition < 200 && galleryLoadedCount < galleryPaintings.length) {
      await loadNextBatch();
    }
  };
  
  const loadNextBatch = async () => {
    if (loadingMore || galleryLoadingMore || galleryLoadedCount >= galleryPaintings.length) return;
    
    loadingMore = true;
    galleryLoadingMore = true;
    
    // Show loading indicator
    let loadingIndicator = grid.querySelector('.gallery-loading-indicator');
    if (!loadingIndicator) {
      loadingIndicator = document.createElement('div');
      loadingIndicator.className = 'gallery-loading-indicator';
      loadingIndicator.textContent = 'Loading more images...';
      grid.appendChild(loadingIndicator);
    }
    
    try {
      // Load next batch
      const batchSize = 8;
      const nextBatch = galleryPaintings.slice(galleryLoadedCount, galleryLoadedCount + batchSize);
      
      // Preload the batch
      await Promise.allSettled(
        nextBatch.map(painting => preloadGalleryImage(painting.url))
      );
      
      // Remove loading indicator
      if (loadingIndicator) {
        loadingIndicator.remove();
      }
      
      // Add images to grid
      nextBatch.forEach(painting => {
        const img = createGalleryImage(painting);
        grid.appendChild(img);
      });
      
      galleryLoadedCount += batchSize;
      
      // Update or add load more button
      updateLoadMoreButton();
      
      // Small delay to prevent rapid loading
      await new Promise(resolve => setTimeout(resolve, 100));
      
    } catch (error) {
      console.error('Error loading more gallery images:', error);
      // Remove loading indicator on error
      if (loadingIndicator) {
        loadingIndicator.remove();
      }
    } finally {
      loadingMore = false;
      galleryLoadingMore = false;
    }
  };
  
  const updateLoadMoreButton = () => {
    // Remove existing load more button
    const existingButton = grid.querySelector('.gallery-load-more-btn');
    if (existingButton) {
      existingButton.remove();
    }
    
    // Add new load more button if there are more images
    if (galleryLoadedCount < galleryPaintings.length) {
      const loadMoreBtn = document.createElement('button');
      loadMoreBtn.className = 'gallery-load-more-btn';
      loadMoreBtn.textContent = 'Load More';
      loadMoreBtn.addEventListener('click', loadNextBatch);
      grid.appendChild(loadMoreBtn);
    }
  };
  
  // Add initial load more button
  updateLoadMoreButton();
  
  // Throttled scroll handler
  let scrollTimeout;
  modalContent.addEventListener('scroll', () => {
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(loadMoreImages, 100);
  });
  
  // Initial check in case content is already scrollable
  setTimeout(loadMoreImages, 500);
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
    preloadAndShowGallery();
  });
  if (closeBtn) closeBtn.addEventListener('click', hideGalleryModal);
}

// Gallery preloading system
let galleryPreloadCache = new Map();
let galleryPreloadInProgress = false;
let galleryBackgroundPreloadStarted = false;

async function preloadAndShowGallery() {
  if (galleryPreloadInProgress) {
    // If preloading is already in progress, wait for it
    return;
  }
  
  // Show loading indicator
  const showLink = document.getElementById('show-gallery-link');
  const originalText = showLink.textContent;
  showLink.textContent = 'Loading...';
  showLink.style.pointerEvents = 'none';
  showLink.classList.add('loading');
  
  try {
    galleryPreloadInProgress = true;
    
    // Get paintings for gallery
    const shuffled = [...paintings];
    shuffleArray(shuffled);
    
    // Preload only the first batch quickly
    const initialBatchSize = 12; // Show first 12 images immediately
    const initialBatch = shuffled.slice(0, initialBatchSize);
    
    // Preload first batch
    await Promise.allSettled(
      initialBatch.map(painting => preloadGalleryImage(painting.url))
    );
    
    // Show the gallery modal immediately with first batch
    showGalleryModal(shuffled, initialBatchSize);
    
  } catch (error) {
    console.error('Error preloading initial gallery images:', error);
    // Still show gallery even if preloading fails
    showGalleryModal(shuffled, 12);
  } finally {
    // Reset button state
    showLink.textContent = originalText;
    showLink.style.pointerEvents = 'auto';
    showLink.classList.remove('loading');
    galleryPreloadInProgress = false;
  }
}

async function preloadGalleryImage(url) {
  // Check cache first
  if (galleryPreloadCache.has(url)) {
    return galleryPreloadCache.get(url);
  }
  
  try {
    const optimizedUrl = optimizeImageUrl(url, 400);
    const img = new Image();
    
    const loadPromise = new Promise((resolve, reject) => {
      img.onload = () => {
        galleryPreloadCache.set(url, optimizedUrl);
        resolve(optimizedUrl);
      };
      img.onerror = () => {
        // Fallback to original URL
        galleryPreloadCache.set(url, url);
        resolve(url);
      };
    });
    
    img.src = optimizedUrl;
    return await loadPromise;
    
  } catch (error) {
    console.error('Error preloading image:', url, error);
    galleryPreloadCache.set(url, url);
    return url;
  }
}

// Start background preloading of gallery images
function startGalleryBackgroundPreload() {
  if (galleryBackgroundPreloadStarted || !paintings || paintings.length === 0) {
    return;
  }
  
  galleryBackgroundPreloadStarted = true;
  
  // Start preloading in the background after a short delay
  setTimeout(async () => {
    try {
      const shuffled = [...paintings];
      shuffleArray(shuffled);
      
      // Preload first 20 images in the background
      const imagesToPreload = shuffled.slice(0, 20);
      
      for (const painting of imagesToPreload) {
        await preloadGalleryImage(painting.url);
        // Small delay to prevent blocking the main thread
        await new Promise(resolve => setTimeout(resolve, 50));
      }
    } catch (error) {
      console.error('Background gallery preload error:', error);
    }
  }, 2000); // Start after 2 seconds to let the main page load first
}

function getArtistBioMap() {
  // Use cached version if available
  if (artistBioMapCache) {
    return artistBioMapCache;
  }
  
  if (!Array.isArray(artistBios)) return {};
  const bioMap = artistBios.reduce((map, b) => {
    map[b.name] = b;
    return map;
  }, {});
  
  // Cache the result
  artistBioMapCache = bioMap;
  return bioMap;
}

// Normalize value to array for robust category/movement/genre handling
function toArray(value) {
  if (value == null) return [];
  return Array.isArray(value) ? value : [value];
}

const categoryFilters = {
  popular: (paintings) => {
    // Get top 10 artists by number of paintings
    const artistCounts = {};
    paintings.forEach(p => {
      if (p.artist) {
        artistCounts[p.artist] = (artistCounts[p.artist] || 0) + 1;
      }
    });
    const topArtists = Object.entries(artistCounts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 10)
      .map(([artist]) => artist);
    return paintings.filter(p => topArtists.includes(p.artist));
  },
  impressionism: p => {
    const categories = toArray(p.categories);
    const inferredCategories = toArray(p.inferred_categories);
    const hasImpressionismCategory = categories.some(cat => 
      cat?.toLowerCase().includes('impressionism')
    );
    const hasInferredImpressionism = inferredCategories.some(cat => 
      cat?.toLowerCase().includes('impressionism')
    );
    const hasImpressionismMovement = toArray(p.artist_movement).concat(toArray(p.movement)).some(m => 
      m?.toLowerCase().includes('impressionism')
    );
    return hasImpressionismCategory || hasInferredImpressionism || hasImpressionismMovement;
  },
  expressionism: p => {
    const categories = toArray(p.categories);
    const hasExpressionismCategory = categories.some(cat => 
      cat?.toLowerCase().includes('expressionism')
    );
    const hasExpressionismMovement = toArray(p.artist_movement).concat(toArray(p.movement)).some(m => 
      m?.toLowerCase().includes('expressionism')
    );
    return hasExpressionismCategory || hasExpressionismMovement;
  },
  romanticism: p => {
    const categories = toArray(p.categories);
    const hasRomanticCategory = categories.some(cat => 
      cat?.toLowerCase().includes('romantic')
    );
    const hasRomanticMovement = toArray(p.artist_movement).concat(toArray(p.movement)).some(m => 
      m?.toLowerCase().includes('romantic')
    );
    return hasRomanticCategory || hasRomanticMovement;
  },
  realism: p => {
    const categories = toArray(p.categories);
    const inferredCategories = toArray(p.inferred_categories);
    const hasRealismCategory = categories.some(cat => 
      cat?.toLowerCase().includes('realism')
    );
    const hasInferredRealism = inferredCategories.some(cat => 
      cat?.toLowerCase().includes('realism')
    );
    const hasRealismMovement = toArray(p.artist_movement).concat(toArray(p.movement)).some(m => 
      m?.toLowerCase().includes('realism')
    );
    return hasRealismCategory || hasInferredRealism || hasRealismMovement;
  },
  naturalism: p => {
    const categories = toArray(p.categories);
    const hasNaturalismCategory = categories.some(cat => 
      cat?.toLowerCase().includes('naturalism')
    );
    const hasNaturalismMovement = toArray(p.artist_movement).concat(toArray(p.movement)).some(m => 
      m?.toLowerCase().includes('naturalism')
    );
    return hasNaturalismCategory || hasNaturalismMovement;
  },
  symbolism: p => {
    const categories = toArray(p.categories);
    const hasSymbolismCategory = categories.some(cat => 
      cat?.toLowerCase().includes('symbolism')
    );
    const hasSymbolismMovement = toArray(p.artist_movement).concat(toArray(p.movement)).some(m => 
      m?.toLowerCase().includes('symbolism')
    );
    return hasSymbolismCategory || hasSymbolismMovement;
  },

  contemporary: p => {
    const categories = toArray(p.categories);
    const hasContemporaryCategory = categories.some(cat => 
      cat?.toLowerCase().includes('contemporary')
    );
    const hasContemporaryMovement = toArray(p.artist_movement).concat(toArray(p.movement)).some(m => 
      m?.toLowerCase().includes('contemporary')
    );
    return hasContemporaryCategory || hasContemporaryMovement;
  },
  landscape: p => {
    const categories = toArray(p.categories);
    const inferredCategories = toArray(p.inferred_categories);
    const hasLandscapeCategory = categories.some(cat => 
      cat?.toLowerCase().includes('landscape')
    );
    const hasInferredLandscape = inferredCategories.some(cat => 
      cat?.toLowerCase().includes('landscape')
    );
    const hasLandscapeGenre = toArray(p.artist_genre).concat(toArray(p.genre)).some(g => 
      g?.toLowerCase().includes('landscape')
    );
    return hasLandscapeCategory || hasInferredLandscape || hasLandscapeGenre;
  },
  portraits: p => {
    const categories = toArray(p.categories);
    const hasPortraitCategory = categories.some(cat => 
      cat?.toLowerCase().includes('portrait')
    );
    const hasPortraitGenre = toArray(p.artist_genre).concat(toArray(p.genre)).some(g => 
      g?.toLowerCase().includes('portrait')
    );
    return hasPortraitCategory || hasPortraitGenre;
  },
  historical: p => {
    const categories = toArray(p.categories);
    const hasHistoricalCategory = categories.some(cat => 
      cat?.toLowerCase().includes('historical')
    );
    const hasHistoricalGenre = toArray(p.artist_genre).concat(toArray(p.genre)).some(g => 
      g?.toLowerCase().includes('historical')
    );
    return hasHistoricalCategory || hasHistoricalGenre;
  },
  religious: p => {
    const categories = toArray(p.categories);
    const hasReligiousCategory = categories.some(cat => 
      cat?.toLowerCase().includes('religious')
    );
    const hasReligiousGenre = toArray(p.artist_genre).concat(toArray(p.genre)).some(g => 
      g?.toLowerCase().includes('religious')
    );
    return hasReligiousCategory || hasReligiousGenre;
  },
  genre: p => {
    const categories = toArray(p.categories);
    const hasGenreCategory = categories.some(cat => 
      cat?.toLowerCase().includes('genre')
    );
    const hasGenreGenre = toArray(p.artist_genre).concat(toArray(p.genre)).some(g => 
      g?.toLowerCase().includes('genre')
    );
    return hasGenreCategory || hasGenreGenre;
  },
  still_life: p => {
    const categories = toArray(p.categories);
    const hasStillLifeCategory = categories.some(cat => 
      cat?.toLowerCase().includes('still life') || cat?.toLowerCase().includes('stilleben')
    );
    const hasStillLifeGenre = toArray(p.artist_genre).concat(toArray(p.genre)).some(g => 
      g?.toLowerCase().includes('still life') || g?.toLowerCase().includes('stilleben')
    );
    return hasStillLifeCategory || hasStillLifeGenre;
  },
  abstract: p => {
    const categories = toArray(p.categories);
    const hasAbstractCategory = categories.some(cat => 
      cat?.toLowerCase().includes('abstract')
    );
    const hasAbstractGenre = toArray(p.artist_genre).concat(toArray(p.genre)).some(g => 
      g?.toLowerCase().includes('abstract')
    );
    return hasAbstractCategory || hasAbstractGenre;
  },
  women_painters: p => p.artist_gender === 'female',
  female_artists: p => p.artist_gender === 'female',
  romantic_nationalism: p => {
    const categories = toArray(p.categories);
    const inferredCategories = toArray(p.inferred_categories);
    const hasRomanticNationalismCategory = categories.some(cat => 
      cat?.toLowerCase().includes('romantic nationalism') || 
      cat?.toLowerCase().includes('romantisk nasjonalisme') ||
      cat?.toLowerCase().includes('nasjonalromantikk')
    );
    const hasInferredRomantic = inferredCategories.some(cat => 
      cat?.toLowerCase().includes('romantic')
    );
    const hasRomanticNationalismMovement = toArray(p.artist_movement).concat(toArray(p.movement)).some(m => 
      m?.toLowerCase().includes('romantic nationalism') || 
      m?.toLowerCase().includes('romantisk nasjonalisme') ||
      m?.toLowerCase().includes('national romantic') ||
      m?.toLowerCase().includes('nasjonalromantikk') ||
      m?.toLowerCase().includes('norwegian romantic nationalism')
    );
    const hasRomanticNationalismBio = p.artist_bio?.toLowerCase().includes('romantic nationalism') || 
                                     p.artist_bio?.toLowerCase().includes('nasjonalromantikk');
    return hasRomanticNationalismCategory || hasInferredRomantic || hasRomanticNationalismMovement || hasRomanticNationalismBio;
  }
};

function getValidPaintings() {
  // Use cache if available and category hasn't changed
  if (validPaintingsCache && validPaintingsCacheCategory === selectedCategory) {
    return validPaintingsCache;
  }
  
  let filtered = paintings.filter(p => p.artist && p.url);
  if (!selectedCategory || selectedCategory === 'all') {
    validPaintingsCache = filtered;
    validPaintingsCacheCategory = selectedCategory;
    return filtered;
  }
  
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
  
  // Cache the result
  validPaintingsCache = filtered;
  validPaintingsCacheCategory = selectedCategory;
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
  
  // Use optimized image loading with progressive enhancement
  loadImageProgressive(img, painting.url).then(() => {
    img.alt = stripHtml(painting.title) || t('painting');
  }).catch(() => {
    // Fallback to original URL if optimization fails
    img.src = painting.url;
    img.alt = stripHtml(painting.title) || t('painting');
  });
  
  // Set current painting for viewer
  currentPainting = painting;
  
  // Setup painting viewer click handler
  img.onclick = function() {
    if (currentPainting) {
      showPaintingViewer(currentPainting);
    }
  };
  
  // Start preloading next few images in background
  preloadNextImages(validPaintings);
  const optionsDiv = document.getElementById('options');
  
  // Clear options and ensure no leftover classes
  optionsDiv.innerHTML = '';
  
  const artists = generateOptions(painting.artist, validPaintings);
  if (artists.length < 2) {
    optionsDiv.innerHTML = `<p>${t('notEnoughArtists')}</p>`;
    return;
  }
  
  // Create all buttons at once to reduce DOM operations
  const fragment = document.createDocumentFragment();
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
        
        // Track analytics
        trackAnswer(true, painting.artist, selectedCategory);
        
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
        
        // Track analytics
        trackAnswer(false, artist, selectedCategory);
        
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
    fragment.appendChild(btn);
  });
  
  // Append all buttons at once
  optionsDiv.appendChild(fragment);
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
            const res = await fetch('./data/artists.json');
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

function createPopupTemplate({ name, bioInfo, artistPaintings, persistent, imgHtml, yearsHtml, bioHtml, tagsHtml, closeBtnHtml, paintingsHtml, galleryHtml }) {
  return `
    <div class="artist-popup-content toast-content">
      ${imgHtml}
      <div class="artist-popup-text toast-text">
        <span class="artist-name">${name}</span>
        ${yearsHtml}
        ${bioHtml}
        ${tagsHtml}
      </div>
      ${galleryHtml || ''}
    </div>
    ${paintingsHtml}
    ${closeBtnHtml}
  `;
}

function createArtistGalleryHtml(artistPaintings, artistName) {
  if (!artistPaintings || artistPaintings.length === 0) {
    return '';
  }
  
  const initialCount = 4; // Show first 4 paintings
  const initialPaintings = artistPaintings.slice(0, initialCount);
  const hasMore = artistPaintings.length > initialCount;
  
  const paintingsHtml = initialPaintings.map((painting, index) => {
    const title = painting.title || 'Untitled';
    const optimizedUrl = optimizeImageUrl(painting.url, 150); // Even smaller thumbnails for better performance
    return `
      <div class="artist-gallery-item" data-painting-index="${index}">
        <img src="${optimizedUrl}" alt="${title}" title="" loading="lazy" 
             onerror="this.src='${painting.url}'"
             onload="this.style.opacity='1'"
             style="opacity: 0; transition: opacity 0.3s ease;">
        <div class="artist-gallery-item-title">${title}</div>
      </div>
    `;
  }).join('');
  
  const loadMoreHtml = hasMore ? `
    <button class="artist-gallery-load-more" data-artist="${artistName}" data-loaded="${initialCount}" data-total="${artistPaintings.length}">
      ${currentLanguage === 'no' ? 'Vis flere' : 'Load More'} (${artistPaintings.length - initialCount})
    </button>
  ` : '';
  
  return `
    <div class="artist-gallery-section">
      <div class="artist-gallery-header">
        <h3 class="artist-gallery-title">${currentLanguage === 'no' ? 'Malerier' : 'Paintings'}</h3>
        <span class="artist-gallery-count">${artistPaintings.length}</span>
      </div>
      <div class="artist-gallery-grid">
        ${paintingsHtml}
      </div>
      ${loadMoreHtml}
    </div>
  `;
}

function setupArtistGalleryHandlers(popup, artistPaintings, artistName) {
  // Handle gallery item clicks to show full painting
  const galleryItems = popup.querySelectorAll('.artist-gallery-item');
  galleryItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.stopPropagation();
      const paintingIndex = parseInt(item.dataset.paintingIndex);
      const painting = artistPaintings[paintingIndex];
      if (painting) {
        // Pass return context so we can return to the artist popup
        showPaintingViewer(painting, { artistPopup: true });
      }
    });
  });
  
  // Handle load more button
  const loadMoreBtn = popup.querySelector('.artist-gallery-load-more');
  if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      loadMoreArtistPaintings(popup, artistPaintings, artistName, loadMoreBtn);
    });
  }
}

function preloadArtistGalleryImages(paintings) {
  if (!paintings || paintings.length === 0) return;
  
  paintings.forEach(painting => {
    const optimizedUrl = optimizeImageUrl(painting.url, 150);
    const img = new Image();
    img.src = optimizedUrl;
  });
}

function loadMoreArtistPaintings(popup, artistPaintings, artistName, loadMoreBtn) {
  const currentLoaded = parseInt(loadMoreBtn.dataset.loaded);
  const total = parseInt(loadMoreBtn.dataset.total);
  const loadCount = 4; // Load 4 more paintings
  const nextBatch = artistPaintings.slice(currentLoaded, currentLoaded + loadCount);
  
  if (nextBatch.length === 0) {
    loadMoreBtn.style.display = 'none';
    return;
  }
  
  // Show loading state
  loadMoreBtn.classList.add('loading');
  loadMoreBtn.textContent = currentLanguage === 'no' ? 'Laster...' : 'Loading...';
  
  // Preload next batch for smoother experience
  const nextNextBatch = artistPaintings.slice(currentLoaded + loadCount, currentLoaded + loadCount * 2);
  preloadArtistGalleryImages(nextNextBatch);
  
  // Simulate loading delay for better UX
  setTimeout(() => {
    const galleryGrid = popup.querySelector('.artist-gallery-grid');
    
    // Add new paintings to the grid
    nextBatch.forEach((painting, batchIndex) => {
      const title = painting.title || 'Untitled';
      const optimizedUrl = optimizeImageUrl(painting.url, 150);
      const actualIndex = currentLoaded + batchIndex; // Calculate the actual index in the full array
      const itemHtml = `
        <div class="artist-gallery-item" data-painting-index="${actualIndex}">
          <img src="${optimizedUrl}" alt="${title}" title="" loading="lazy" 
               onerror="this.src='${painting.url}'"
               onload="this.style.opacity='1'"
               style="opacity: 0; transition: opacity 0.3s ease;">
          <div class="artist-gallery-item-title">${title}</div>
        </div>
      `;
      galleryGrid.insertAdjacentHTML('beforeend', itemHtml);
    });
    
    // Update load more button
    const newLoaded = currentLoaded + loadCount;
    loadMoreBtn.dataset.loaded = newLoaded;
    
    if (newLoaded >= total) {
      loadMoreBtn.style.display = 'none';
    } else {
      loadMoreBtn.textContent = `${currentLanguage === 'no' ? 'Vis flere' : 'Load More'} (${total - newLoaded})`;
    }
    
    loadMoreBtn.classList.remove('loading');
    
    // Re-attach event handlers to new items
    const newItems = galleryGrid.querySelectorAll('.artist-gallery-item');
    newItems.forEach(item => {
      if (!item.hasAttribute('data-handler-attached')) {
        item.setAttribute('data-handler-attached', 'true');
        item.addEventListener('click', (e) => {
          e.stopPropagation();
          const paintingIndex = parseInt(item.dataset.paintingIndex);
          const painting = artistPaintings[paintingIndex];
          if (painting) {
            // Pass return context so we can return to the artist popup
            showPaintingViewer(painting, { artistPopup: true });
          }
        });
      }
    });
  }, 300);
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
  let closeBtnHtml = persistent ? `<div class="persistent-popup-close-container"><button class="persistent-popup-close-btn" aria-label="${t('close')}">${t('close')}</button></div>` : '';
  let paintingsHtml = '';
  
  // Create gallery HTML for persistent popups
  let galleryHtml = '';
  if (persistent && artistPaintings.length > 0) {
    galleryHtml = createArtistGalleryHtml(artistPaintings, name);
  }
  
  popup.innerHTML = createPopupTemplate({ name, bioInfo, artistPaintings, persistent, imgHtml, yearsHtml, bioHtml, tagsHtml, closeBtnHtml, paintingsHtml, galleryHtml });
  popup.style.opacity = '0';
  popup.style.display = 'flex';
  popup.classList.add('visible');
  setTimeout(() => popup.style.opacity = '1', 10);
  
  // Add event handlers for gallery if it exists
  if (persistent && artistPaintings.length > 0) {
    setupArtistGalleryHandlers(popup, artistPaintings, name);
    // Preload next batch of images for smoother experience
    preloadArtistGalleryImages(artistPaintings.slice(8, 16));
  }
  if (persistent) {
    // Remove all <a> links in the popup (if any)
    Array.from(popup.querySelectorAll('a')).forEach(link => link.remove());
    popup.className = 'artist-popup toast persistent';
    // No overlay for persistent popups - they appear directly on the page
    const closeBtn = popup.querySelector('.persistent-popup-close-btn');
    if (closeBtn) closeBtn.addEventListener('click', (e) => {
      e.stopPropagation(); // Prevent event from bubbling up
      hidePopup(popup, onDone);
    });
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
      // Reset everything to start a completely new quiz
      selectedCategory = 'all';
      const catSelect = document.getElementById('category-select');
      if (catSelect) catSelect.value = 'all';
      streak = 0;
      updateStreakBar();
      
      // Clear any existing messages
      hideMessage();
      
      // Hide any open modals
      hideCongratsModal();
      hideGalleryModal();
      hideAboutModal();
      hideRoundResults();
      document.getElementById('artists-modal').style.display = 'none';
      
      // Start a completely fresh round
      startNewRound();
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
      // Make artist names clickable to show persistent info popup
      li.innerHTML = `<span class="clickable-artist-name">${name}</span> (${numPaintings})`;
      
      // Add click event to show artist info popup
      const artistNameSpan = li.querySelector('.clickable-artist-name');
      artistNameSpan.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent modal from closing
        showArtistPopup(name, null, true); // persistent = true
      });
      
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
    toArray(p.artist_genre).concat(toArray(p.genre)).some(g => g && g.toLowerCase().includes('landscape'))
  ).length;
  
  // Portraits
  categoryCounts.portraits = validPaintings.filter(p => 
    toArray(p.artist_genre).concat(toArray(p.genre)).some(g => g && g.toLowerCase().includes('portrait'))
  ).length;
  
  // Women painters
  categoryCounts.women_painters = validPaintings.filter(p => p.artist_gender === 'female').length;
  
  // 19th century
  categoryCounts['1800s'] = validPaintings.filter(p => {
    const bio = artistBios.find(b => b.name === p.artist);
    return bio && bio.birth_year && 1800 <= parseInt(bio.birth_year) && parseInt(bio.birth_year) < 1900;
  }).length;
  
  // 20th century
  categoryCounts['1900s'] = validPaintings.filter(p => {
    const bio = artistBios.find(b => b.name === p.artist);
    return bio && bio.birth_year && 1900 <= parseInt(bio.birth_year) && parseInt(bio.birth_year) < 2000;
  }).length;
  
  // Impressionism
  categoryCounts.impressionism = validPaintings.filter(p => 
    toArray(p.artist_movement).concat(toArray(p.movement)).some(m => m && m.toLowerCase().includes('impressionism'))
  ).length;
  
  // Expressionism
  categoryCounts.expressionism = validPaintings.filter(p => 
    toArray(p.artist_movement).concat(toArray(p.movement)).some(m => m && m.toLowerCase().includes('expressionism'))
  ).length;
  
  // Norwegian Romantic
  categoryCounts.romantic_nationalism = validPaintings.filter(p => 
    toArray(p.artist_movement).concat(toArray(p.movement)).some(m => 
      m && (m.toLowerCase().includes('nasjonalromantikk') || 
             m.toLowerCase().includes('norwegian romantic nationalism') ||
             m.toLowerCase().includes('romantic nationalism'))
    )
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
  const modal = document.getElementById('how-to-play-modal');
  const title = document.getElementById('how-to-play-title');
  const content = document.getElementById('how-to-play-content');
  
  if (!modal) return;
  
  // Update title
  title.textContent = t('aboutHowToPlay');
  
  // Update content based on language
  if (currentLanguage === 'no') {
    content.innerHTML = `
      <div class="how-to-play-section">
        <h3>Utfordringen</h3>
        <p>Test din kunnskap om norsk kunsthistorie! Du vil bli vist berømte norske malerier og må identifisere kunstneren som skapte dem.</p>
      </div>
      
      <div class="how-to-play-section">
        <h3>Slik fungerer det</h3>
        <ul>
          <li>Se på maleriet som vises til venstre</li>
          <li>Velg riktig kunstner fra de fire alternativene til høyre</li>
          <li>Få umiddelbar tilbakemelding på svaret ditt</li>
          <li>Følg fremgangen din med strek-indikatoren</li>
        </ul>
      </div>
      
      <div class="how-to-play-section">
        <h3>Poengsum</h3>
        <ul>
          <li>Hvert riktig svar legger til i strekken din</li>
          <li>Få 10 på rad for en perfekt poengsum!</li>
          <li>Se resultatene dine på slutten av hver runde</li>
          <li>Last ned sertifikater for perfekte poengsummer</li>
        </ul>
      </div>
      
      <div class="how-to-play-section">
        <h3>Kategorier</h3>
        <p>Velg fra forskjellige kategorier for å fokusere på spesifikke kunstnere eller tidsperioder. Bruk rullegardinmenyen øverst til høyre for å velge din foretrukne kategori.</p>
      </div>
      
      <div class="how-to-play-section">
        <h3>Lær mer</h3>
        <p>Klikk "Malere" for å se alle kunstnere i samlingen, eller "Galleri" for å bla gjennom alle malerier. Hver kunstner har en detaljert biografi og sine verk.</p>
      </div>
    `;
  } else {
    content.innerHTML = `
      <div class="how-to-play-section">
        <h3>The Challenge</h3>
        <p>Test your knowledge of Norwegian art history! You'll be shown famous Norwegian paintings and need to identify the artist who created them.</p>
      </div>
      
      <div class="how-to-play-section">
        <h3>How It Works</h3>
        <ul>
          <li>Look at the painting displayed on the left</li>
          <li>Choose the correct artist from the four options on the right</li>
          <li>Get instant feedback on your answer</li>
          <li>Track your progress with the streak indicator</li>
        </ul>
      </div>
      
      <div class="how-to-play-section">
        <h3>Scoring</h3>
        <ul>
          <li>Each correct answer adds to your streak</li>
          <li>Get 10 in a row for a perfect score!</li>
          <li>View your results at the end of each round</li>
          <li>Download certificates for perfect scores</li>
        </ul>
      </div>
      
      <div class="how-to-play-section">
        <h3>Categories</h3>
        <p>Choose from different categories to focus on specific artists or time periods. Use the dropdown menu at the top right to select your preferred category.</p>
      </div>
      
      <div class="how-to-play-section">
        <h3>Learn More</h3>
        <p>Click "Painters" to see all artists in the collection, or "Gallery" to browse all paintings. Each artist has a detailed biography and their works.</p>
      </div>
    `;
  }
  
  modal.style.display = 'flex';
  modal.focus();
  
  // Add click outside to close
  setTimeout(() => {
    function outsideClick(e) {
      if (!modal.querySelector('.how-to-play-modal-content').contains(e.target)) {
        hideAboutModal();
        document.removeEventListener('click', outsideClick);
      }
    }
    document.addEventListener('click', outsideClick);
  }, 100);
}

function hideAboutModal() {
  const modal = document.getElementById('how-to-play-modal');
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = '';
  }
}

function setupAboutModal() {
  const showLink = document.getElementById('show-how-to-play-link');
  const modal = document.getElementById('how-to-play-modal');
  const closeBtn = document.getElementById('close-how-to-play-modal');
  
  // Remove previous event listeners if any
  if (showLink) {
    // Remove all existing event listeners by cloning
    const newShowLink = showLink.cloneNode(true);
    showLink.parentNode.replaceChild(newShowLink, showLink);
    
    // Add the event listener to the new element
    newShowLink.addEventListener('click', e => {
      e.preventDefault();
      showAboutModal();
    });
  }
  
  if (closeBtn) {
    // Remove all existing event listeners by cloning
    const newCloseBtn = closeBtn.cloneNode(true);
    closeBtn.parentNode.replaceChild(newCloseBtn, closeBtn);
    
    // Add the event listener to the new element
    newCloseBtn.addEventListener('click', hideAboutModal);
  }
  
  if (modal) {
    modal.onclick = function(e) {
      if (e.target === modal) {
        hideAboutModal();
      }
    };
  }
}

// Painting Viewer Functions
function showPaintingViewer(painting, returnContext = null) {
  const modal = document.getElementById('painting-viewer-modal');
  const image = document.getElementById('painting-viewer-image');
  
  if (!modal || !image) return;
  
  // Store return context for when viewer is closed
  modal.dataset.returnContext = returnContext ? JSON.stringify(returnContext) : '';
  
  // Use the painting URL that was passed to the function
  image.src = painting.url;
  image.style.display = 'block';
  
  // Show modal with animation
  modal.style.display = 'flex';
  modal.classList.add('visible');
  document.body.style.overflow = 'hidden';
}

function hidePaintingViewer() {
  const modal = document.getElementById('painting-viewer-modal');
  if (modal) {
    // Check if there's a return context
    const returnContextStr = modal.dataset.returnContext;
    if (returnContextStr) {
      try {
        const returnContext = JSON.parse(returnContextStr);
        
        // If we have an artist popup to return to, make sure it's visible
        if (returnContext.artistPopup) {
          const artistPopup = document.querySelector('.artist-popup.toast.persistent');
          if (artistPopup) {
            artistPopup.style.display = 'flex';
            artistPopup.classList.add('visible');
          }
        }
        
        // Clear the return context
        modal.dataset.returnContext = '';
      } catch (e) {
        console.warn('Failed to parse return context:', e);
      }
    }
    
    modal.classList.remove('visible');
    modal.style.display = 'none';
    document.body.style.overflow = '';
  }
}

function setupPaintingViewer() {
  const modal = document.getElementById('painting-viewer-modal');
  
  // Close on escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && modal && modal.style.display === 'flex') {
      hidePaintingViewer();
    }
  });
  
  // Close on any click (background or image)
  if (modal) {
    modal.onclick = function(e) {
      hidePaintingViewer();
    };
  }
  
  // Make painting clickable in quiz
  const paintingElement = document.getElementById('painting');
  if (paintingElement) {
    paintingElement.onclick = function() {
      // Get current painting data from the quiz state
      if (currentPainting) {
        showPaintingViewer(currentPainting);
      }
    };
  }
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
    trackPerfectScore();
    showDiploma();
    return;
  }
  
  // Update content with proper translations
  title.textContent = t('roundStats.title');
  score.textContent = `${totalCorrect}/10`;
  
  // Update labels
  const scoreLabel = document.querySelector('#round-results-modal .stat-label');
  if (scoreLabel) scoreLabel.textContent = t('roundStats.score') + ':';
  
  const artistsLabel = document.querySelector('#round-results-artists .stat-label');
  if (artistsLabel) artistsLabel.textContent = t('roundStats.artists') + ':';
  
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
  const categoryLabel = document.getElementById('diploma-category-label');
  const categoryValue = document.getElementById('diploma-category-value');
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
  
  // Add category information to description
  const categoryNameForDesc = selectedCategory === 'all' ? t('fullCollection') : t(CATEGORY_DEFS.find(cat => cat.value === selectedCategory)?.label || 'fullCollection');
  const descriptionWithCategory = t('diploma.description') + (selectedCategory !== 'all' ? ` (${categoryNameForDesc})` : '');
  description.textContent = descriptionWithCategory;
  
  awardedLabel.textContent = t('diploma.awardedTo') + ':';
  categoryLabel.textContent = t('diploma.category') + ':';
  dateLabel.textContent = t('diploma.date') + ':';
  downloadBtn.textContent = t('diploma.download');
  playAgainBtn.textContent = t('playAgain');
  
  // Set awardee name (you could make this customizable)
  awardedValue.textContent = 'Art Enthusiast';
  
  // Set category name
  const categoryName = selectedCategory === 'all' ? t('fullCollection') : t(CATEGORY_DEFS.find(cat => cat.value === selectedCategory)?.label || 'fullCollection');
  categoryValue.textContent = categoryName;
  
  // Set current date
  const now = new Date();
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  dateValue.textContent = now.toLocaleDateString(currentLanguage === 'no' ? 'nb-NO' : 'en-US', options);
  
  // Show modal
  modal.style.display = 'flex';
  modal.focus();
  
  // Setup event listeners
  if (downloadBtn) {
    downloadBtn.onclick = downloadDiploma;
    console.log('Download button found and configured');
  } else {
    console.error('Download button not found!');
  }
  
  if (playAgainBtn) {
    playAgainBtn.onclick = () => {
      hideDiploma();
      startNewRound();
    };
    console.log('Play Again button found and configured');
  } else {
    console.error('Play Again button not found!');
  }
  
  // No outside click to close - diploma must be closed via buttons only
}

function hideDiploma() {
  const modal = document.getElementById('diploma-modal');
  if (modal) modal.style.display = 'none';
}

function downloadDiploma() {
  const diplomaContent = document.querySelector('.diploma-content');
  if (!diplomaContent) return;
  
  // Use html2canvas to capture just the diploma content (without buttons)
  if (typeof html2canvas !== 'undefined') {
    html2canvas(diplomaContent, {
      scale: 2,
      backgroundColor: '#ffffff',
      useCORS: true,
      allowTaint: true,
      width: diplomaContent.offsetWidth,
      height: diplomaContent.offsetHeight
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
  
  // Track game start
  trackGameStart();
  
  // Clear caches when starting new round
  clearCaches();
  loadQuiz();
}

function clearCaches() {
  // Clear existing caches
  validPaintingsCache = null;
  validPaintingsCacheCategory = null;
  artistBioMapCache = null;
  categoryCountsCache.clear();
  
  // Clear performance caches
  memoryCache.clear();
  domCache.clear();
  
  // Force memory cleanup
  cleanupMemory();
  
  // Update performance metrics
  performanceMetrics.operations++;
}

function preloadNextImages(validPaintings) {
  if (isPreloading) return;
  isPreloading = true;
  
  // Use performance config for preloading
  const preloadCount = Math.min(PERFORMANCE_CONFIG.PRELOAD_COUNT, validPaintings.length);
  const startIndex = Math.floor(Math.random() * validPaintings.length);
  
  // Batch preload with delay to prevent blocking
  let loadedCount = 0;
  
  const preloadImage = (index) => {
    const painting = validPaintings[index];
    if (painting && painting.url && !imageCache.has(painting.url)) {
      preloadOptimizedImage(painting.url).then(img => {
        imageCache.set(painting.url, img);
        loadedCount++;
        if (loadedCount >= preloadCount) {
          setTimeout(() => { isPreloading = false; }, PERFORMANCE_CONFIG.PRELOAD_DELAY);
        }
      }).catch(() => {
        loadedCount++;
        if (loadedCount >= preloadCount) {
          setTimeout(() => { isPreloading = false; }, PERFORMANCE_CONFIG.PRELOAD_DELAY);
        }
      });
    } else {
      loadedCount++;
      if (loadedCount >= preloadCount) {
        setTimeout(() => { isPreloading = false; }, PERFORMANCE_CONFIG.PRELOAD_DELAY);
      }
    }
  };
  
  // Stagger preloading to prevent blocking
  for (let i = 0; i < preloadCount; i++) {
    const index = (startIndex + i) % validPaintings.length;
    setTimeout(() => preloadImage(index), i * 50);
  }
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
  if (artistsLink) artistsLink.textContent = t('painters'); // Changed from 'artists' to 'painters'
  
  const galleryLink = document.getElementById('show-gallery-link');
  if (galleryLink) galleryLink.textContent = t('gallery');
  
  const aboutLink = document.getElementById('show-how-to-play-link');
  if (aboutLink) aboutLink.textContent = t('aboutHowToPlay');

  // Always re-attach About modal event listener in case the link was replaced
  setupAboutModal();
}

function updateCategorySelector() {
  const categorySelect = document.getElementById('category-select');
  if (categorySelect) {
    categorySelect.setAttribute('aria-label', t('selectCategory'));
  }
}

// Image optimization functions
function optimizeImageUrl(url, targetWidth = 800) {
  if (!url || !url.includes('wikimedia.org')) return url;
  
  // Wikimedia Commons optimization patterns
  const optimizations = [
    // Try WebP first (best compression)
    url.replace(/\.(jpg|jpeg|png)$/i, '.webp'),
    // Try smaller thumbnail versions
    url.replace(/\/commons\//, '/commons/thumb/').replace(/\.(jpg|jpeg|png|webp)$/i, `/${targetWidth}px-$1`),
    // Try medium size
    url.replace(/\/commons\//, '/commons/thumb/').replace(/\.(jpg|jpeg|png|webp)$/i, '/600px-$1'),
    // Try small size
    url.replace(/\/commons\//, '/commons/thumb/').replace(/\.(jpg|jpeg|png|webp)$/i, '/400px-$1')
  ];
  
  return optimizations[0]; // Return WebP version
}

function getResponsiveImageUrl(url, containerWidth = 800) {
  if (!url || !url.includes('wikimedia.org')) return url;
  
  // Calculate optimal size based on container
  let targetWidth = 800;
  if (containerWidth <= 400) targetWidth = 400;
  else if (containerWidth <= 600) targetWidth = 600;
  else if (containerWidth <= 800) targetWidth = 800;
  else targetWidth = 1200;
  
  return optimizeImageUrl(url, targetWidth);
}

// Progressive image loading
function loadImageProgressive(imgElement, url, fallbackUrl = null) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    
    img.onload = () => {
      imgElement.src = img.src;
      imgElement.classList.add('loaded');
      resolve(img);
    };
    
    img.onerror = () => {
      if (fallbackUrl && fallbackUrl !== url) {
        // Try fallback URL
        loadImageProgressive(imgElement, fallbackUrl).then(resolve).catch(reject);
      } else {
        // Use original URL as last resort
        imgElement.src = url;
        imgElement.classList.add('loaded');
        resolve(img);
      }
    };
    
    // Start with optimized URL
    img.src = optimizeImageUrl(url);
  });
}

// Lazy loading with intersection observer
function setupLazyLoading() {
  if (!('IntersectionObserver' in window)) {
    // Fallback for older browsers
    document.querySelectorAll('img[data-src]').forEach(img => {
      img.src = img.dataset.src;
      img.classList.add('loaded');
    });
    return;
  }
  
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        const url = img.dataset.src;
        const fallbackUrl = img.dataset.fallback;
        
        if (url) {
          loadImageProgressive(img, url, fallbackUrl).then(() => {
            img.removeAttribute('data-src');
            img.removeAttribute('data-fallback');
            observer.unobserve(img);
          });
        }
      }
    });
  }, {
    rootMargin: '50px 0px', // Start loading 50px before image enters viewport
    threshold: 0.01
  });
  
  // Observe all lazy images
  document.querySelectorAll('img[data-src]').forEach(img => {
    imageObserver.observe(img);
  });
}

// Image preloading with optimization
function preloadOptimizedImage(url) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error('Failed to load image'));
    img.src = optimizeImageUrl(url);
  });
}

document.addEventListener('DOMContentLoaded', async () => {
  try {
    // Start performance monitoring
    performanceMetrics.startTime = Date.now();
    
    // Start memory cleanup
    startMemoryCleanup();
    
            const res = await fetch('./data/paintings.json');
    if (!res.ok) throw new Error('Failed to load paintings');
    paintings = await res.json();
    await loadArtistBios();
    
    // Initialize all systems with performance optimizations
    initializeArtistWeights();
    updateCategoryDropdown();
    updateCollectionInfo();
    updateLanguageUI();
    setupLanguageToggle();
    startNewRound(); // Start with a new round
    setupArtistModal();
    setupGalleryModal();
    setupAboutModal();
    setupPaintingViewer();
    
    // Start background preloading of gallery images
    startGalleryBackgroundPreload();
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
    
    // Add throttled scroll and resize handlers for performance
    window.addEventListener('scroll', throttle(() => {
      // Handle any scroll-based updates here
      performanceMetrics.operations++;
    }, PERFORMANCE_CONFIG.ANIMATION_THROTTLE));
    
    window.addEventListener('resize', debounce(() => {
      // Handle any resize-based updates here
      performanceMetrics.operations++;
    }, 250));
    
    // Add visibility change handler to pause operations when tab is not visible
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        // Pause heavy operations when tab is not visible
        if (cleanupTimer) clearInterval(cleanupTimer);
      } else {
        // Resume operations when tab becomes visible
        startMemoryCleanup();
      }
    });
  } catch (err) {
    console.error('Error loading data:', err);
    document.getElementById('options').innerHTML = `<p>${t('errorLoading')}</p>`;
  }
});