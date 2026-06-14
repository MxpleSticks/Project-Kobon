# Project Kobon

**Project Kobon** is a search program designed to find solutions to the Kobon Triangle Problem.<br>
**Check out the project on --> [stardance](https://stardance.hackclub.com/projects/5309) <--**

![Alt text](https://i.imgur.com/Tii75GE.png)

The program includes:
- Simple terminal interface/interactions
- A solver
- A viewer (Visulizes json data)
- Remote reporting (via Discord Webhook)
- CPU-based calculations (via NumPy)


The overall goal of **Project Kobon** is to find arrangements of **k** lines that produce the maximum number of non-overlapping triangles. When reading sources about the Kobon Triangle Problem, you may see **n** used instead of **k**. Both symbols represent the same thing: the number of lines in the arrangement.


# What is the Kobon Triangle Problem?

The Kobon Triangle Problem investigates the maximum number of non-overlapping triangles that can be formed by an arrangement of **k** lines.

There is already a known formula that gives the upper bound for each value of **k**, BUT the problem is still unsolved because it is not known whether these upper bounds are achievable.

This gap between what is theoretically possible vs what can actually be constructed is what keeps the problem unsolved.


# Installation
### Using the Installer (Recommended):

1. Navigate to the GitHub Releases page.

2. Download the latest [.exe](https://github.com/MxpleSticks/Project-Kobon/releases) file.

3. Run the .exe file to launch the application.

### Building from Source:

Make sure to have C++ installed --> [Here](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170) <-- <br>
Python 3.13.13 is recommended (for packages) --> [Here](https://www.python.org/downloads/windows/) <--

1. Clone or download the GitHub repo.

2. Install the required dependencies: pip install -r requirements.txt

3. Run the program: py main.py or python main.py

# Support

| Platform | Minimum Version | Download Link / Instructions |
| :--- | :--- | :--- |
| **Windows** | Windows 10/11 | Download the [.exe](https://github.com/MxpleSticks/Project-Kobon/releases) installer |
| **macOS** | 12.0+ (Monterey) | Not currently supported natively |
| **Linux** | Ubuntu 22.04+ | Not currently supported natively |

**The only way to run this program on macOS or Linux is to build via source.**


# Usage

When the program is launched you will be presented with 3 options:

1. Run solver | searches for a solution over a user-defined amount of time.

2. Run until target | searches until a user-specific number of triangles is reached.

3. Open viewer | Opens the viewer for inspecting the programs outputs.

# Performance

### WARNING: make sure you have a good cooling system/setup
### Project kobon can utilize as much of the cpu as you specify
![Alt text](https://i.imgur.com/szPhFHW.png)