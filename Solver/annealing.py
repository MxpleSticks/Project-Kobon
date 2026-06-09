import numpy as np
import random

from Solver.geometry import count_triangles
from Solver.state import create_random_state, nudge
from Theory.theory import tamura_upper_bound

startTemperature = 10.0
coolingRate = 0.995

