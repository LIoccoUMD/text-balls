# Bouncing Balls Simulation

This project simulates bouncing balls with physics and renders them as animated GIFs. It features two Python scripts: `runSim.py` for physics-based animation and `ballsText.py` for converting text into ball rasters, enabling dynamic text effects.

## Overview

- **`runSim.py`**: Drives a physics simulation of balls bouncing in a 16x9 space, outputting `bouncing_balls.gif` using Pymunk and Matplotlib.
- **`ballsText.py`**: Transforms text into a grid of balls with position, velocity, and color, integrable with `runSim.py` for animated text.

## Prerequisites

- **Python 3.x**
- **Libraries**:
  - `numpy`: Array operations and randomization.
  - `matplotlib`: Animation rendering via `FuncAnimation`.
  - `pymunk`: 2D physics engine for collisions and gravity.
  - `pillow` (PIL): Text rasterization with `ImageFont` and `ImageDraw`.
- **Font File**: A TrueType font (e.g., `Artesania.otf`) for `ballsText.py`.

Install dependencies:
```bash
pip install numpy matplotlib pymunk pillow