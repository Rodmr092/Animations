# Mathematical Animations with Python and Manim

This repository contains educational animations created with Manim to explain mathematical concepts.

## Setup

1. Create virtual environment:
\\\ash
python -m venv animaciones
\\\

2. Activate virtual environment:
\\\ash
# Windows
.\\animaciones\\Scripts\\activate

# Linux/Mac
source animaciones/bin/activate
\\\

3. Install dependencies:
\\\ash
pip install -r requirements.txt
\\\

## Project Structure

- \/src\: Source code for animations
- \/media\: Generated animations (not tracked in git)
- \/docs\: Documentation files

## Running Animations

To render an animation:
\\\ash
python -m manim src/filename.py SceneName -pql
\\\

## License

MIT License

