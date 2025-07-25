# 🖼️ Norwegian Art Challenge

A fun quiz where you guess the artist behind famous Norwegian paintings.

Try it live on GitHub Pages:  
👉 [Play the game](https://<your-username>.github.io/<your-repo-name>/)

---

## 🎨 Example Artwork 

![The Scream by Edvard Munch](https://upload.wikimedia.org/wikipedia/commons/c/c5/Edvard_Munch%2C_1893%2C_The_Scream%2C_oil%2C_tempera_and_pastel_on_cardboard%2C_91_x_73_cm%2C_National_Gallery_of_Norway.jpg)

---

## 📁 Project Structure


## 🛠️ Data Collection & Update Workflow

To update or expand the quiz's dataset:
1. Run the unified Python script (`collect_art.py`) in the project root. You can collect by artist name, by URL, or from a file of names/URLs.
2. The script will fetch and append new paintings to `paintings_appended.json` (deduplicated, never overwritten).
3. Run `merge_artist_tags.py` to merge and enrich the data, producing `paintings_merged.json` for the game.
4. (Optional) Run `diagnose_art.py` to generate a `diagnostics.md` report of your data health and category coverage.

This workflow is repeatable and can be run any time you want to refresh or expand the dataset.

## 🇳🇴 Featured Norwegian Painters

This quiz features works from 50 of Norway's most important and influential painters, including:
- Edvard Munch
- Johan Christian Dahl
- Christian Krohg
- Theodor Kittelsen
- Harriet Backer
- Kitty Lange Kielland
- Peter Nicolai Arbo
- Hans Gude
- Peder Balke
- Frits Thaulow
- Nikolai Astrup
- Odd Nerdrum
- Harald Sohlberg
- Erik Werenskiold
- Adolph Tidemand
- Lars Hertervig
- Oda Krohg
- Eilif Peterssen
- Hans Dahl
- Per Krohg
- August Cappelen
- Asta Nørregaard
- Amaldus Nielsen
- Christian Skredsvig
- Gunnar Berg
- Halfdan Egedius
- Thorolf Holmboe
- Jakob Weidemann
- Peder Aadnes
- Martin Aagaard
- Rolf Aamot
- Johannes Flintoe
- Rolf Groven
- Konrad Knudsen
- Wilhelm Peters
- Halvard Storm
- Jacob Gløersen
- Gustav Wentzel
- Oscar Wergeland
- Carl Sundt-Hansen
- Adelsteen Normann
- Axel Revold
- Jean Heiberg
- Olav Christopher Jenssen
- Bjarne Melgaard
- Fredrik Værslev
- Charlotte Wankel
- Inger Sitter
- Cora Sandel
- Paul René Gauguin

## 🖼️ About the Image Data

All paintings and artist information are sourced from open data repositories, primarily Wikimedia Commons and Wikidata. Each entry includes:
- High-quality image URL (hotlinked, not stored locally)
- Artist name, bio, birth/death years
- Painting title, year, medium, dimensions, location, and license (where available)

The dataset is designed to be scalable and is regularly updated by running the included Python script. This ensures the quiz always features a rich, diverse, and growing collection of Norwegian art, ready for filtering by artist, period, style, and more.



<!-- STATS_START -->
**Latest Art Quiz Stats**
- Total paintings: 3574
- Total unique artists in paintings: 81
- Total artists in bios: 91
- Categories:
  - Full Collection: 3574 paintings, 81 painters
  - Popular Painters: 1646 paintings, 10 painters
  - Landscape Painting: 353 paintings, 36 painters
  - Romanticism: 48 paintings, 1 painters
  - Impressionism: 189 paintings, 2 painters
  - Expressionism: 199 paintings, 2 painters
  - Portraits: 314 paintings, 32 painters
  - Historical/Nationalism: 172 paintings, 8 painters
  - 19th Century: 3173 paintings, 53 painters
  - 20th Century: 103 paintings, 20 painters
<!-- STATS_END -->
