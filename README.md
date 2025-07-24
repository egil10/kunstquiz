# 🖼️ Norwegian Art Challenge

A fun quiz where you guess the artist behind famous Norwegian paintings.

Try it live on GitHub Pages:  
👉 [Play the game](https://<your-username>.github.io/<your-repo-name>/)

---

## 🎨 Example Artwork Oh Yeah

![The Scream by Edvard Munch](https://upload.wikimedia.org/wikipedia/commons/c/c5/Edvard_Munch%2C_1893%2C_The_Scream%2C_oil%2C_tempera_and_pastel_on_cardboard%2C_91_x_73_cm%2C_National_Gallery_of_Norway.jpg)

---

## 📁 Project Structure


## 🛠️ Data Collection & Update Workflow

To update or expand the quiz's dataset:
1. Run the provided Python script (`collect_norwegian_art.py`) in the project root.
2. The script will fetch and merge artist bios and paintings from Wikidata, Wikipedia, and Wikimedia Commons.
3. The output is a single `paintings.json` file in the `data/` directory, which is used directly by the game.

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

