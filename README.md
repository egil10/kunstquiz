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

