# Project Kobon

**Project Kobon** is a search program designed to find solutions to the Kobon Triangle Problem.


The program includes:
- Simple terminal interactions
- A solver
- A viewer
- Remote reporting (via Discord)
- CPU-based calculations (via NumPy)


The overall goal of **Project Kobon** is to find arrangements of **k** lines that produce the maximum number of non-overlapping triangles. When reading sources about the Kobon Triangle Problem, you may see **n** used instead of **k**. Both symbols represent the same thing: the number of lines in the arrangement.


# What is the Kobon Triangle Problem?

The Kobon Triangle Problem investigates the maximum number of non-overlapping triangles that can be formed by an arrangement of **k** lines.

There is already a known formula that gives the upper bound for each value of **k**, BUT the problem is still unsolved because it is not known whether these upper bounds are achievable.

This gap between what is theoretically possible vs what can actually be constructed is what keeps the problem unsolved.


# Installation

1. Clone or download the GitHub repo.

2. Install the required dependencies: pip install -r requirements.txt

3. Run the program: python main.py


# Usage

When the program is launched you will be presented with 3 options:

1. Run solver | searches for a solution over a user-defined amount of time.

2. Run until target | searches until a user-specific number of triangles is reached.

3. Open viewer | Opens the viewer for inspecting the programs outputs.