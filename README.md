# SWAT Raid

SWAT Raid is a 2D top-down tactical shooter developed in Python. 
The project implements advanced visibility mechanics, specifically dynamic lighting and shadow casting, to simulate limited field of view in a combat scenario.
The application includes a custom-built level editor for map generation and serialization.

## Project Overview

The objective of the simulation is to neutralize hostile targets within a designated time limit while managing resources such as ammunition and health. The core technical feature is the implementation of a raycasting algorithm using geometric operations to render realistic shadows in real-time, occluding objects outside the player's direct line of sight.

## Key Features

* **Dynamic Lighting Engine:** utilizes the `shapely` library to calculate polygon intersections and differences, rendering shadows that conform to map geometry (walls, obstacles) relative to the player's position.
* **Integrated Level Editor:** A built-in tool allowing for real-time map creation, modification, and persistence. Level data (walls, enemies, textures) is serialized and stored in JSON format.
* **Game Loop & State Management:** Handles distinct states including the intro sequence, active gameplay, menu interfaces, and win/loss conditions.
* **Entity Interaction:** Includes collision detection, projectile ballistics, and basic enemy AI that tracks player position based on visibility and proximity.

## Technology Stack

The project is built using the following technologies:

* **Pygame**
* **Shapely**

## Installation and Execution

To run the application locally, follow these steps:

1.  **Prerequisites**
    Ensure Python 3 is installed on the system.

2.  **Install Dependencies**
    Execute the following command in the terminal to install the required libraries:
    ```bash
    pip install pygame shapely
    ```

3.  **Run the Application**
    Start the game by executing the main script:
    ```bash
    python main.py
    ```

## Controls

### Gameplay Controls
* **W, A, S, D**: Movement.
* **Mouse Cursor**: Aiming (character rotation).
* **Left Click**: Fire weapon.
* **R**: Reload weapon.
* **F**: Restart game (available upon Game Over or Victory).
* **M**: Return to Main Menu (from Victory screen).

### Level Editor Controls
* **F1**: Toggle Editor Mode ON/OFF.
* **F5**: Save current level to JSON.
* **F6**: Load level from JSON.
* **Left Click**: Place object.
* **Right Click**: Remove object.
* **Number Keys (Object Selection)**:
    * **1**: Wall
    * **2**: Enemy
    * **3**: Grass Texture
    * **4**: Floor Type 1
    * **5**: Floor Type 2
    * **6**: Tree
    * **7**: Bomb

## Project Structure

* `main.py`: Entry point and main game loop execution.
* `game/`: Package containing game logic modules (Player, Enemy, Editor, Shadows, UI).
* `resources/`: Directory containing assets (sprites, textures, audio files).
* `level_data.json`: serialized data for the map layout.
