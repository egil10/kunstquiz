# Kunstquiz: Norwegian Art Challenge

A fun, modern quiz where you guess the artist behind famous Norwegian paintings. Built for art lovers, students, and anyone curious about Norway's rich visual heritage.

## Features

- 1000s of paintings from 80+ Norwegian artists
- Multiple quiz categories: movements, genres, museums, and more
- Responsive, mobile-friendly UI
- Artist bios, tags, and painting galleries
- Data sourced from open Wikimedia and Wikidata APIs
- Diagnostics and data health checks

## How to Play

1. Select a category (e.g., Impressionism, Women Painters, National Museum)
2. View a painting and choose the correct artist from four options
3. Get instant feedback and learn about each artist
4. Try to build a streak and explore the gallery!

## Complete Workflow (6 Steps)

The repository supports a complete 6-step workflow:

1. **Finding new images** → `python scripts/workflow.py --collect`
2. **Cleaning them and deleting bad ones** → `python scripts/workflow.py --clean`
3. **Finding manual URLs to add** → `python scripts/workflow.py --add-urls`
4. **Finding manual URLs to remove** → `python scripts/workflow.py --remove-urls`
5. **Push to app** → `python scripts/workflow.py --process` + `python scripts/workflow.py --deploy`
6. **App with working game logic** → Ready to use!

### Quick Start

```bash
# Initialize the workflow structure
python scripts/workflow.py --init

# Run complete workflow (all 6 steps)
python scripts/workflow.py --full

# Run quick workflow (collect, clean, process, deploy)
python scripts/workflow.py --quick

# Individual steps
python scripts/workflow.py --collect --url "https://commons.wikimedia.org/wiki/Category:Paintings_by_Artist"
python scripts/workflow.py --clean --quality --duplicates
python scripts/workflow.py --add-urls --file data/config/urls_to_add.txt
python scripts/workflow.py --remove-urls --file data/config/urls_to_remove.txt
python scripts/workflow.py --process
python scripts/workflow.py --deploy
```

## Project Structure

```
kunstquiz/
├── scripts/                    # All Python scripts
│   ├── workflow.py            # Complete 6-step workflow
│   ├── collect_art.py         # Main collection script
│   ├── clean.py               # All cleanup operations
│   ├── stats.py               # All analysis operations
│   ├── process.py             # All data processing
│   ├── utils.py               # All utility operations
│   └── diagnostics.py         # Comprehensive diagnostics
├── data/                      # Data files
│   ├── paintings.json         # Web app paintings
│   ├── artists.json           # Web app artists
│   ├── app_data.json         # Unified app data
│   └── config/                # Configuration files
├── docs/                      # Documentation
│   └── category_strategy.md   # Collection strategy guide
├── assets/                    # Web app assets (CSS, JS)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── index.html                 # Main web app
└── README.md                  # This file
```

## Scripts Overview

The repository uses consolidated scripts for better organization:

- **`scripts/workflow.py`** - Complete 6-step workflow management
- **`scripts/collect_art.py`** - Main collection script
- **`scripts/clean.py`** - All cleanup operations (duplicates, quality, etc.)
- **`scripts/stats.py`** - All analysis and statistics operations
- **`scripts/process.py`** - All data processing operations
- **`scripts/utils.py`** - All utility operations (URLs, backups, health checks)
- **`scripts/diagnostics.py`** - Comprehensive diagnostics report generation

## Diagnostics & Stats

The `scripts/stats.py --diagnostics` script checks for data consistency, category coverage, and missing info. It also updates the stats below:

<!-- STATS_START -->
**Latest Art Quiz Stats**
- Total paintings: 3036
- Total unique artists in paintings: 59
- Total artists in bios: 91
- Categories:
  - Full Collection: 3036 paintings, 59 painters
  - Popular Painters: 1444 paintings, 10 painters
  - Landscape: 1661 paintings, 40 painters
  - Realism: 379 paintings, 3 painters
  - Impressionism: 376 paintings, 8 painters
  - Romantic Nationalism: 732 paintings, 7 painters
  - Modernism: 73 paintings, 2 painters
  - Female Artists: 240 paintings, 4 painters
<!-- STATS_END -->

## Categories

- Full Collection: All paintings
- Popular Painters: Top 10 artists by painting count
- Landscape: Landscape paintings (34 artists)
- Realism: Realist movement (15 artists)
- Impressionism: Impressionist paintings (12 artists)
- Romantic Nationalism: Norwegian romantic nationalism (10 artists)
- Modernism: Modern works (10 artists)
- Female Artists: Female painters (4 artists)

## Contributing

Pull requests and suggestions are welcome! See [issues](https://github.com/egil10/kunstquiz/issues) or open a PR.

## License

MIT. All painting images and artist data are from open Wikimedia/Wikidata sources.

---

*Made with love for Norwegian art lovers.*
