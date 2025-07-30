# Kunstquiz: Norwegian Art Challenge

A fun, modern quiz where you guess the artist behind famous Norwegian paintings. Built for art lovers, students, and anyone curious about Norway's rich visual heritage.

## 🎨 Features
- 1000s of paintings from 80+ Norwegian artists
- Multiple quiz categories: movements, genres, museums, and more
- Responsive, mobile-friendly UI
- Artist bios, tags, and painting galleries
- Data sourced from open Wikimedia and Wikidata APIs
- Diagnostics and data health checks

## 🕹️ How to Play
1. Select a category (e.g., Impressionism, Women Painters, National Museum)
2. View a painting and choose the correct artist from four options
3. Get instant feedback and learn about each artist
4. Try to build a streak and explore the gallery!

## 🛠️ Complete Workflow (6 Steps)

The repository now supports a complete 6-step workflow:

1. **Finding new images** → `workflow.py --collect`
2. **Cleaning them and deleting bad ones** → `workflow.py --clean`
3. **Finding manual URLs to add** → `workflow.py --add-urls`
4. **Finding manual URLs to remove** → `workflow.py --remove-urls`
5. **Push to app** → `workflow.py --process` + `workflow.py --deploy`
6. **App with working game logic** → Ready to use!

### Quick Start:
```bash
# Initialize the workflow structure
python workflow.py --init

# Run complete workflow (all 6 steps)
python workflow.py --full

# Run quick workflow (collect, clean, process, deploy)
python workflow.py --quick

# Individual steps
python workflow.py --collect --url "https://commons.wikimedia.org/wiki/Category:Paintings_by_Artist"
python workflow.py --clean --quality --duplicates
python workflow.py --add-urls --file data/config/urls_to_add.txt
python workflow.py --remove-urls --file data/config/urls_to_remove.txt
python workflow.py --process
python workflow.py --deploy
```

## 📊 Scripts Overview
The repository now uses consolidated scripts for better organization:

- **`workflow.py`** - Complete 6-step workflow management
- **`collect_art.py`** - Main collection script (unchanged)
- **`clean.py`** - All cleanup operations (duplicates, quality, etc.)
- **`stats.py`** - All analysis and statistics operations
- **`process.py`** - All data processing operations
- **`utils.py`** - All utility operations (URLs, backups, health checks)
- **`diagnostics.py`** - Comprehensive diagnostics (unchanged)
- **`consolidate_data.py`** - Data consolidation and cleanup

## 📊 Diagnostics & Stats
The `stats.py --diagnostics` script checks for data consistency, category coverage, and missing info. It also updates the stats below:

<!-- STATS_START -->
**Latest Art Quiz Stats**
- Total paintings: 3282
- Total unique artists in paintings: 81
- Total artists in bios: 91
- Categories:
  - Full Collection: 3282 paintings, 81 painters
  - Popular Painters: 1513 paintings, 10 painters
  - Landscape Painting: 1745 paintings, 41 painters
  - Portraits: 584 paintings, 34 painters
  - Women Painters: 584 paintings, 34 painters
  - 19th Century: 0 paintings, 0 painters
  - 20th Century: 0 paintings, 0 painters
  - Impressionism: 392 paintings, 9 painters
  - Expressionism: 253 paintings, 5 painters
  - Norwegian Romantic: 0 paintings, 0 painters
<!-- STATS_END -->

## 🗂️ Categories
- Full Collection: All paintings
- Popular Painters: Top 10 artists by painting count
- Landscape: Landscape paintings (34 artists)
- Realism: Realist movement (15 artists)
- Impressionism: Impressionist paintings (12 artists)
- Romantic Nationalism: Norwegian romantic nationalism (10 artists)
- Modernism: Modern works (10 artists)
- Female Artists: Female painters (4 artists)

## 🤝 Contributing
Pull requests and suggestions are welcome! See [issues](https://github.com/egil10/kunstquiz/issues) or open a PR.

## 📄 License
MIT. All painting images and artist data are from open Wikimedia/Wikidata sources.

---

*Made with ❤️ for Norwegian art lovers.*
*B.r*
