

*This project has been created as part of the 42 curriculum by emarette and efoyer.*

## Description
**Dark-Man** is a hellish, dark-themed reimagining of the classic **Pac-Man** arcade game. In this project, the traditional maze has been transformed into a dark, atmospheric environment where the player navigates to consume "pacgums" and "super pacgums" while avoiding relentless Minotaurs (which act as the ghosts: Blinky, Clyde, Inky, and Pinky). The project focuses on rigorous game logic, custom entity behaviors, and structured file validation to create a robust and engaging arcade experience.

## Instructions

### Prerequisites
* Python 3.10 or higher.
* `uv` package manager installed on your system.
* The `mazegenerator`  package

### Compilation & Installation
To install the dependencies and set up the virtual environment, simply run:

```bash
make install
```

### Execution

To launch the game with the default configuration, use:

Bash

```bash
make run

```

You can also run the game with a specific configuration file by passing the `CONFIG` argument:

Bash

```bash
make run CONFIG=path/to/your/config.json

```

To run the game in debug mode:

Bash

```bash
make debug

```

### Linting & Cleaning

The codebase strictly adheres to `flake8` and `mypy` standards.

-   Run `make lint` to check for styling and typing errors using `flake8` and `mypy`.
    
-   Run `make lint-strict` to run the linters with the `--strict` flag enabled for `mypy`.
    
-   Run `make clean` to remove cache directories like `__pycache__` and `.ruff_cache`, as well as compiled `.pyc` files.
    
-   Run `make fclean` to perform a clean and additionally remove the `.venv` environment.
    

## Resources

-   **Python Arcade Library**: The core framework used for rendering, window management, and sprite handling (specifically version 3.3.3).
    
-   **Pydantic Documentation**: Used extensively for data validation and managing the configuration file constraints.
    
-   **AI Usage**: Use as an aid to bring code up to standard (mypy and flake8) and to explain complex concepts..
    

## Configuration

The game configuration is managed via a JSON file (e.g., `config.json`) and validated at runtime using a Pydantic `Config` model to ensure data integrity.

**Structure & Default Values:**

-   `score_file`: Path to the highscore file (default: `"highscores.json"`).
    
-   `level`: A list of dictionaries defining the parameters for each level. Each level requires a `width` (10-46), `height` (10-46), and `nb_pacgum`.
    
-   `lives`: The starting number of lives (default: 3).
    
-   `nb_pacgum`: The total number of standard pacgums in the starting maze (default: 42).
    
-   `pt_per_pacgum`: Points awarded per regular pacgum (default: 10).
    
-   `pt_per_super_pacgum`: Points awarded per super pacgum (default: 50).
    
-   `pt_per_ghost`: Points awarded for defeating a Minotaur (default: 200).
    
-   `lvl_max_time`: The time limit for a level in seconds (default: 90).
    
-   `seed`: The generation seed used for the maze (default: 904).
    
-   `volume`: Global audio volume, constrained between 0 and 100 (default: 100).
    
-   `cheats_enabled`: Boolean to toggle the cheat menu (default: false).
    

## Highscore

The highscore system is designed to persist player achievements across sessions. It works by serializing and deserializing a dedicated JSON file (e.g., `scoreboard.json` or `highscores.json`).

**Implementation Reasoning:** A JSON-based approach was chosen because it integrates seamlessly with Python's standard library and Pydantic's validation tools. Whenever the game ends, the system reads the JSON file, appends the new player's name and score, sorts the list in descending order, and truncates it to keep only the top players. This ensures the file remains lightweight while maintaining an accurate and validated leaderboard.

## Maze Generation

The project relies on the assigned A-Maze-ing package (`mazegenerator-00001-py3-none-any.whl`) to programmatically build the tile maps. The package takes the `width`, `height`, and `seed` values defined in the current level's configuration to procedurally generate a grid. This grid is then parsed by the game logic to place walls, empty paths, pacgums, and spawn points for both the player and the Minotaurs.

## Implementation

The project is built on a modern Python stack (>=3.10) utilizing `uv` for lightning-fast dependency locking and resolution.

-   **Data Validation:** Pydantic ensures that all configurations and scoreboard entries are strictly typed and bounded before the game loop starts.
    
-   **Rendering & Audio:** The Python Arcade library manages the visual rendering of the dark-themed sprites (fire, dark logos) and handles the spatial audio (e.g., atmospheric music).
    
-   **Typing:** The entire project enforces strict static typing, validated through `mypy`, preventing runtime type errors and ensuring a highly predictable state.
    

## General Software Architecture

The software architecture is heavily modularized, separating concerns into distinct views and managers:

-   `src/config.py`: Contains the Pydantic models responsible for parsing and validating `config.json`.
    
-   `src/__main__.py`: The entry point that initializes the Arcade window and injects the loaded configuration.
    
-   `src/game_view/`: The core gameplay module.
    
    -   `game_view.py`: The main Arcade View managing the gameplay loop, rendering, and input handling.
        
    -   `map.py`: Handles the procedural maze generation and tilemap state.
        
    -   `player.py`: Manages the player's movement, state, and collision detection.
        
    -   `ghost/`: Contains the AI logic and pathfinding for the Minotaurs (`blinky.py`, `clyde.py`, `inky.py`, `pinky.py`) managed by a central `ghost_manager.py`.
        
    -   `game_menu/`: Contains the overlay panels (escape menu, cheat menu, stats panel).
        
-   `src/menu_view/`: Handles the main menu and instructions screens.
    
-   `src/scoreboard_view/`: Manages the UI and logic for displaying the top scores.
    
-   `src/setting_view/`: Interfaces for modifying game settings (like volume) dynamically.
    

## Project Management

The project was managed using an iterative, feature-branch approach. Tasks were broken down into core components (e.g., Configuration, Map Generation, Ghost AI, UI Views) and tracked linearly to ensure dependencies (like having a working map before writing ghost pathfinding) were met in order.
