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

1. **Finding new images** → `python scripts/workflow.py --collect`
2. **Cleaning them and deleting bad ones** → `python scripts/workflow.py --clean`
3. **Finding manual URLs to add** → `python scripts/workflow.py --add-urls`
4. **Finding manual URLs to remove** → `python scripts/workflow.py --remove-urls`
5. **Push to app** → `python scripts/workflow.py --process` + `python scripts/workflow.py --deploy`
6. **App with working game logic** → Ready to use!

### Quick Start:
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

## 📁 Project Structure
```
kunstquiz/
├── scripts/                    # All Python scripts
│   ├── workflow.py            # Complete 6-step workflow
│   ├── collect_art.py         # Main collection script
│   ├── clean.py               # All cleanup operations
│   ├── stats.py               # All analysis operations
│   ├── process.py             # All data processing
│   ├── utils.py               # All utility operations
│   ├── diagnostics.py         # Comprehensive diagnostics
│   └── consolidate_data.py    # Data consolidation
├── data/                      # Data files
│   ├── paintings_with_inferred_categories.json  # Web app paintings
│   ├── artist_bios.json       # Web app artists
│   ├── raw/                   # Raw collected data
│   ├── processed/             # Clean, processed data
│   └── config/                # Configuration files
├── config/                    # Project configuration
├── docs/                      # Documentation
├── assets/                    # Web app assets (CSS, JS)
├── index.html                 # Main web app
└── README.md                  # This file
```

## 📊 Scripts Overview
The repository uses consolidated scripts for better organization:

- **`scripts/workflow.py`** - Complete 6-step workflow management
- **`scripts/collect_art.py`** - Main collection script
- **`scripts/clean.py`** - All cleanup operations (duplicates, quality, etc.)
- **`scripts/stats.py`** - All analysis and statistics operations
- **`scripts/process.py`** - All data processing operations
- **`scripts/utils.py`** - All utility operations (URLs, backups, health checks)
- **`scripts/diagnostics.py`** - Comprehensive diagnostics
- **`scripts/consolidate_data.py`** - Data consolidation and cleanup

## 📊 Diagnostics & Stats
The `scripts/stats.py --diagnostics` script checks for data consistency, category coverage, and missing info.

## 🗂️ Categories
- Full Collection
- Popular Painters
- Landscapes
- Portraits
- Romanticism
- Expressionism
- Impressionism
- Historical / Nationalism
- 1800s
- National Museum of Norway
- Women Painters

## 🤝 Contributing
Pull requests and suggestions are welcome! See [issues](https://github.com/egil10/kunstquiz/issues) or open a PR.

## 📄 License
MIT. All painting images and artist data are from open Wikimedia/Wikidata sources.

---

*Made with ❤️ for Norwegian art lovers.*
