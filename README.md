# Guerilla War – Tile and Map Tools

This repository provides Python-based tools and documentation for analysing and visualising the background and tilemap data from the arcade game **Guerrilla War** (SNK, 1987). These tools are intended for historical and educational purposes, to explore the data formats and artistic techniques used in the game’s level design.

> ⚠️ **Disclaimer**: No copyrighted ROMs or assets are included. The tools here require original game ROMs, which are not provided. These scripts are purely for documentation and reverse-engineering purposes.

---

## 🧱 Tile Format Overview

- Each **tile block** consists of a **2×2 grid of tiles**, where each tile is made up of smaller 8×8 pixel characters.
- Character data is stored in a packed bitplane format.
- The tilemaps in Guerrilla War are wider than in some similar games (e.g., Ikari Warriors), and are structured in **large horizontal supertiles**.
- Maps are composed using **chunk indices** that refer to these 2x2 tile blocks.

---

## 🛠️ Scripts Included

- `tile2x2_plot_test.py` – Renders the raw tiles using character graphics and palette data.
- `gmap2x2_plot_number.py` – Plots full background maps using 2×2 tile references.
- `make_palette4.py` – Converts raw palette data from PROMs to 8-bit RGB format, we use the same weight approach as MAME (in fact identical).
- `mastermap_plot2.py`—Passed the graphics, the tiles2x2, the tilemaps, and also the master game for the meta tiles so that the whole game image can be created.

Each script accepts command-line parameters for specifying the input files (character data, palettes, chunk maps, etc.) and produces PNG outputs for visual analysis.
The provided generate-data.bat will execute all scripts, when you put the rom files into this folder, and will generate everything you need
---

## 🗺️ Map Structure

- Guerilla War maps are stored in **horizontal strips**, each using a large chunk of 2x2 tiles.
- Chunk data is read in **row-major** order and often repeated to create wide scrolling backgrounds.
- Some maps are reused with variations in palette and enemy placements.

---

## 🎨 Palette Details

- Palettes are stored in a 3 bytes-per-color format (RGB).
- There are multiple palettes per stage.
- Scripts generate a visual for the palettes inside the game proms, as PNG images for references.

---

## 📚 Purpose

This project aims to:
- Document the graphic format and tile engine used in Guerilla War.
- Provide tools to visualize and decode these formats.
- Assist other retro game researchers or homebrew developers working on similar hardware.

---

## 🙌 Acknowledgements

- SNK for the original game and its artistic legacy.
- The MAME development team for their emulator framework and debugging tools.
- Reverse-engineering and preservation communities for keeping these games accessible and understandable.
