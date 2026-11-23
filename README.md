# Catch the Diamonds! 💎

A simple 2D game created for **CSE 423: Computer Graphics — Assignment 2 (Lab 02)** using Python and OpenGL. The game demonstrates the **Midpoint Line Drawing Algorithm** and **eight-way symmetry** to draw all game objects using only `GL_POINTS`.

## 🎮 Gameplay

Catch falling diamonds with the bowl-shaped catcher at the bottom of the screen. Each successful catch increases your score by **1** and spawns another diamond at a random horizontal position with a random bright color. Diamonds gradually fall faster as the game progresses. **Missing a diamond ends the game.**

## ✨ Features

- Midpoint line drawing for all eight zones, using coordinate conversion to and from Zone 0
- Diamond, catcher, and control icons drawn using the midpoint algorithm (`GL_POINTS` only)
- Random diamond colors and horizontal spawn positions
- Frame-time-based falling movement and increasing difficulty
- AABB collision detection and score reporting in the console
- Game-over state with a red catcher
- Restart, play/pause, and exit controls
- Cheat Mode with automatic horizontal catcher movement

## 🕹️ Controls

| Input | Action |
| --- | --- |
| **← / →** | Move the catcher left or right |
| **C** | Turn Cheat Mode on or off |
| **Teal left arrow** (top-left) | Restart the game and reset the score |
| **Amber play/pause** (top-center) | Pause or resume the game |
| **Red X** (top-right) | Exit the game and print the final score |

## 🚀 How to Run

**Important: The `OpenGL` folder is uploaded as a ZIP file. You must extract it before running the game.** The Python program imports directly from the extracted `OpenGL` folder.

1. Download or clone this repository.
2. Find the zipped OpenGL folder (for example, `OpenGL.zip`) and **extract it**.
3. Make sure the extracted folder is named **`OpenGL`** and is in the **same directory as the game Python file**.
4. Open a terminal in that directory.
5. Run the game with Python 3, replacing `game.py` with the actual name of the Python file in the repository:

   ```bash
   python game.py
   ```

   On systems where Python 3 is launched as `python3`, use `python3 game.py` instead.

### Required folder structure after extraction

```text
Catch-the-Diamonds/
├── README.md
├── game.py           # Example name; use the actual game .py filename
├── OpenGL.zip        # Compressed folder included in the repository
└── OpenGL/           # Extracted folder required to run the game
    └── ...
```

> **Do not try to run the game directly from the ZIP without extracting the `OpenGL` folder.** If you see `ModuleNotFoundError: No module named 'OpenGL'`, check the folder name and location. Some systems may additionally require a compatible GLUT/FreeGLUT runtime.

## 🧠 How It Works

The project uses the midpoint line drawing algorithm for **Zone 0**. To draw a line in any other zone, it:

1. Identifies the original zone from the line's endpoints.
2. Converts the endpoints to Zone 0.
3. Calculates the line pixels using the midpoint decision parameter.
4. Converts each calculated pixel back to the original zone.
5. Draws the pixel using `GL_POINTS`.

The diamond and catcher are each constructed with **four midpoint-drawn lines**. The game uses **AABB (Axis-Aligned Bounding Box)** collision detection to register catches.

## 🛠️ Technologies

- **Python 3**
- **OpenGL / GLUT** (using the supplied OpenGL reference environment)
- Python standard-library modules: `random`, `time`

## 📚 Academic Context

Developed as part of **CSE 423: Computer Graphics, Lab 02 — Midpoint Line Drawing Algorithm**. The implementation follows the assignment's OpenGL function restrictions and uses `GL_POINTS` for drawing rather than built-in line or polygon primitives.
