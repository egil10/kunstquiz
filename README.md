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

## 🛠️ Data Collection & Update Workflow
1. Run `collect_art.py` to fetch new paintings by artist, URL, or file
2. Data is appended to `data/paintings_appended.json` (never overwritten)
3. Run `merge_artist_tags.py` to merge and enrich data for the quiz
4. (Optional) Run `diagnostics.py` to generate a data health report and update the stats below

## 📊 Diagnostics & Stats
The `diagnostics.py` script checks for data consistency, category coverage, and missing info. It also updates the stats below:

<!-- STATS_START -->
**Latest Art Quiz Stats**
- Total paintings: 4764
- Total unique artists in paintings: 85
- Total artists in bios: 91
- Categories:
  - Full Collection: 4764 paintings, 85 painters
  - Popular Painters: 2239 paintings, 10 painters
  - Landscape Painting: 2560 paintings, 41 painters
  - Portraits: 934 paintings, 34 painters
  - Women Painters: 934 paintings, 34 painters
  - 19th Century: 0 paintings, 0 painters
  - 20th Century: 0 paintings, 0 painters
  - Impressionism: 525 paintings, 9 painters
  - Expressionism: 321 paintings, 5 painters
  - Norwegian Romantic: 0 paintings, 0 painters
<!-- STATS_END -->

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
