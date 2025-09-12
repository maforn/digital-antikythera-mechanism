# Antikythera Mechanism Simulation

*Part of the presentation for Cost Action CaLISTA General Meeting 2025*

This project presents two interactive simulations of the Antikythera mechanism, the world's oldest known analog computer. It offers both an "ancient" interpretation, reflecting the historical appearance of the device, and a "modern" interpretation with a contemporary user interface.

The simulations are built using Python and Pygame, giving a visual and didactic experience of this hellenistic piece of ancient Greek technology.

## Features

- **Two Distinct Visualizations**:
  - **Ancient Simulation**: A geocentric model with a bronze and papyrus aesthetic, featuring spiral dials as they appeared on the original mechanism.
  - **Modern Simulation**: A heliocentric model with a sleek, dark-themed UI, using circular progress bars and a clean layout to represent the astronomical cycles.
- **Interactive Front and Back Views**:
  - **Front View**: Displays the positions of celestial bodies (Sun, Moon, and planets) and the main calendar and zodiac dials.
  - **Back View**: Shows the complex cycles used for predicting eclipses and tracking calendars, including the Metonic, Saros, Games, and Exeligmos dials.
- **Simulation Controls**:
  - Adjust the simulation speed.
  - Pause and resume the simulation.
  - Switch between the front and back views.

## The Dials Explained

The Antikythera mechanism was used to predict astronomical positions and eclipses. The simulations represent its key functions through various dials:

### Front Face
- **Zodiac Dial**: A fixed ring showing the twelve zodiac signs.
- **Egyptian Calendar Dial**: A 354-day calendar ring that can be rotated to align with the zodiac.

### Back Face
- **Metonic Dial**: A 19-year, 235-month calendar used to align solar years and lunar months. Represented as a 5-turn spiral in the ancient view.
- **Saros Dial**: An 18-year, 223-month cycle used to predict the timing of solar and lunar eclipses. Represented as a 4-turn spiral in the ancient view.
- **Games (Olympiad) Dial**: A 4-year dial tracking the cycle of the Panhellenic Games, including the Olympics.
- **Exeligmos Dial**: A 54-year dial used to provide more accurate eclipse predictions by accounting for the fractional day in the Saros cycle.

## How to Run

### Prerequisites
You need to have Python and Pygame installed. If you don't have Pygame, you can install it via pip:
```bash
pip install pygame
```

### Running the Simulations
You can run either the ancient or the modern simulation by executing the corresponding Python script:

**To run the Ancient Simulation:**
```bash
python ancient_simulation.py
```

**To run the Modern Simulation:**
```bash
python modern_simulation.py
```

## Controls

| Key         | Action                  |
|-------------|-------------------------|
| **UP Arrow**  | Increase simulation speed |
| **DOWN Arrow**| Decrease simulation speed |
| **SPACE**     | Pause / Resume          |
| **TAB**       | Switch between Front and Back views |

## File Structure

The project is organized into two main parts, with shared components:

- `ancient_simulation.py`: Main file for the ancient-style simulation.
- `ancient_drawing.py`: Handles the rendering of the front face for the ancient simulation.
- `ancient_back_face.py`: Handles the rendering of the back face for the ancient simulation.
- `ancient_config.py`: Configuration data for the ancient simulation.

- `modern_simulation.py`: Main file for the modern-style simulation.
- `modern_drawing.py`: Handles the rendering of the front face for the modern simulation.
- `modern_back_face.py`: Handles the rendering of the back face for the modern simulation.
- `modern_config.py`: Configuration data for the modern simulation.