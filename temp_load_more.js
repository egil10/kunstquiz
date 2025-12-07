async function loadMoreGalleryImages(count = 9) {
    // Validate state
    if (!galleryPageGrid) {
        console.warn('loadMoreGalleryImages: galleryPageGrid not found');
        return;
    }

    if (galleryPageLoadedCount >= galleryPagePaintings.length) {
        updateLoadMoreButton();
        return;
    }

    // Get the next batch
    const nextBatch = galleryPagePaintings.slice(galleryPageLoadedCount, galleryPageLoadedCount + count);

    if (nextBatch.length === 0) {
        updateLoadMoreButton();
        return;
    }

    // Show loading indicator
    const loadingIndicator = document.createElement('div');
    loadingIndicator.className = 'gallery-loading-indicator';
    loadingIndicator.textContent = currentLanguage === 'no' ? 'Laster bilder...' : 'Loading images...';
    loadingIndicator.style.textAlign = 'center';
    loadingIndicator.style.padding = '2rem';
    loadingIndicator.style.color = '#666';
    galleryPageGrid.appendChild(loadingIndicator);

    // Create images OFF-DOM
    const imagePromises = nextBatch.map(painting => {
        if (!painting || !painting.url) return Promise.resolve(null);

        return new Promise((resolve) => {
            const img = createGalleryImage(painting);
            if (!img) {
                resolve(null);
                return;
            }

            img.style.opacity = '0';

            const timeout = setTimeout(() => {
                resolve(null); // Failed to load in time
            }, 10000);

            img.onload = () => {
                clearTimeout(timeout);
                resolve(img);
            };

            img.onerror = () => {
                clearTimeout(timeout);
                resolve(null);
            };
        });
    });

    // Wait for ALL images
    const loadedImages = await Promise.all(imagePromises);

    // Remove loading indicator
    loadingIndicator.remove();

    // Filter out failed images and append all at once
    const fragment = document.createDocumentFragment();
    const successfulImages = loadedImages.filter(img => img !== null && img.complete && img.naturalWidth > 0);

    successfulImages.forEach(img => {
        img.style.opacity = '0';
        img.style.transform = 'scale(0.98)';
        fragment.appendChild(img);
    });

    // Append ALL at once
    galleryPageGrid.appendChild(fragment);

    // Fade in ALL simultaneously
    requestAnimationFrame(() => {
        successfulImages.forEach(img => {
            img.style.opacity = '1';
            img.style.transform = 'scale(1)';
        });
    });

    // Update counter
    galleryPageLoadedCount += nextBatch.length;

    // Update button
    requestAnimationFrame(() => {
        updateLoadMoreButton();
        const galleryBtn = document.querySelector('.gallery-load-more-btn');
        const galleryPage = document.getElementById('gallery-page');
        if (galleryBtn && galleryPage && galleryPage.style.display !== 'none' && galleryPageLoadedCount < galleryPagePaintings.length) {
            galleryBtn.classList.add('visible');
            galleryBtn.classList.remove('hidden');
        }
        updateLoadMoreButtonVisibility();
    });
}
