# Pong - Block Breaker Game

## Project Overview
This project is a 2D block-breaker game developed in Python using the **Pygame** library. The game features a dynamic physics system for ball trajectories, a level-based progression system with progress persistence, and a custom level editor. 

The game combines traditional arcade mechanics with features like trajectory prediction and multi-page menu navigation.


## Core Features

### 1. Game Mechanics and Physics
* **Collision Detection**: Implements precise line-rectangle collision handling to determine bounce angles based on which
side of a block or the platform is hit.
* **Dynamic Bounce**: The ball's return angle is influenced by its distance from the center of the platform on impact, allowing
for tactical control.


### 2. Progression System
* **Level Management**: Includes a grid-based level selection screen where levels are unlocked sequentially.
* **Persistence**: Player progress and scores are stored in a local `setup` file, ensuring that unlocked levels
and high scores are saved between sessions.
* **Victory Conditions**: A level is completed once all breakable blocks in the matrix are destroyed.


### 3. Level Editor (`makelvl.py`)
* **Custom Creation**: A standalone utility that allows developers to design levels by clicking on a grid to place or
remove blocks.
* **Matrix Export**: Saves the coordinates of placed blocks into a formatted matrix file that the main engine can load.


## Technical Specifications
* **Resolution**: 1200 x 800 pixels
* **Framerate**: Capped at 100 FPS
* **Input**: Supports both Mouse (UI navigation) and Keyboard (A/D or Arrow keys for movement)


## Project Structure
* `main.py`: The central game loop handling state management (Menu, Level Selection, Gameplay).
* `movement.py`: Contains the `Player` class responsible for physics, collision logic, and ball movement.
* `build.py`: Handles asset loading, image scaling, and matrix-to-level rendering.
* `makelvl.py`: An interactive tool for creating new game levels.
* `docs/levelX/matrix`: Data files containing block coordinate mappings for each level.


## Setup and Installation

### 1. Environment Configuration
It is recommended to use a virtual environment to manage dependencies:
```
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Running the Game

 1. **Launch Game:**

    ```
    python main.py
    ```

 2. **Launch Level Editor:**

    ```
    python makelvl.py
    ```

    Follow the console prompt to enter the level number you wish to edit.


