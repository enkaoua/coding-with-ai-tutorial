# How to use AI properly: a hands-on tutorial

Learn to use AI to help you learn and build, without trusting it blindly. You will work with a simulated Arduino board that reads an ECG.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/enkaoua/coding-with-ai-tutorial/blob/main/using_AI_tutorial_STUDENT.ipynb)

## Run it in Colab (nothing to install)

1. Click the **Open in Colab** button above.
2. Sign in with a Google account if Colab asks you to.
3. Run the first cell (**Setup**), then work through the notebook from top to bottom.
4. To keep your work, use **File > Save a copy in Drive**. Colab does not save your changes back to GitHub.

## Run it on your own computer

1. Install Python 3.10 or later and VS Code (with its Python and Jupyter extensions).
2. Download this repository (green **Code** button > **Download ZIP**) and unzip it.
3. In VS Code, open the whole folder (**File > Open Folder**).
4. In a terminal in that folder: `python -m venv .venv`, activate it, then `pip install -r requirements.txt`.
5. Open `using_AI_tutorial_STUDENT.ipynb`, choose the `.venv` kernel, and run the first cell.

## What is in this repository

| File | What it is |
| --- | --- |
| `using_AI_tutorial_STUDENT.ipynb` | The tutorial |
| `tests.py` | The answer checkers and the simulated board used by the notebook. Ignore this file, you don't need to read or edit it. |
| `requirements.txt` | The Python packages needed to run the tutorial on your own computer |
