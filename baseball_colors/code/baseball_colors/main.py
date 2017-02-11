from pathlib import Path

colors = None
colors = "kry"

algoname = "onebase"
# algoname = "heat"
algoname = "treesol"

output   = "asciiart"
output   = "picture"

mode = "circle"
mode = "line"

folder = Path("/Users/projetmbc/tests")

# Bugs found
#     gameboard = [3, 3, None, 1, 0, 1, 2, 2, 4, 4, 5, 5]
#     gameboard = [0, 1, None, 1, 2, 2, 3, 3, 4, 4]
#     gameboard = [None, 0, 2, 2, 1, 1, 3, 3, 4, 4]
#         ---> gotoleft meilleur que greedy

size      = 5
gameboard = [None] + list(range(size)) + list(range(1, size))

import random
random.shuffle(gameboard)

# gameboard = [0, None, 2, 1, 1, 2]

# gameboard = [4, 4, None, 0, 1, 1, 2, 2, 3, 3]
#
# gameboard = [3, 1, 2, None, 4, 1, 4, 0, 2, 3]
# gameboard = [2, None, 4, 1, 4, 0, 2, 3, 3, 1]
# gameboard = [2, None, 4, 1, 0, 2, 3, 3, 1, 4]
# gameboard = [3, 1, 2, 4, 1, 4, 0, 2, 3, None]
#
# gameboard = [4, 2, 3, 0, 2, 3, 1, 4, 1, None]
# gameboard = [3, 1, 2, None, 3, 1, 4, 0, 4, 2]
#
# gameboard = [1, 2, 3, None, 4, 1, 4, 0, 2, 3]
# # gameboard = [1, 2, 3, 1, None, 0, 3, 2, 4, 4]

# gameboard = [2, 1, 1, 2, None, 0]

# > : meilleur que...

# bactrack > onebase >> heat
# gameboard = [1, 1, 2, 2, 0, None]

# bactrack >> heat > onebase
gameboard = [3, 3, 2, 4, 1, 4, 0, 1, 2, None]

gameboard = [1, 0, 1, None, 2, 2]

import importlib

solve  = importlib.import_module('solve.{0}'.format(algoname))
output = importlib.import_module('plot.{0}'.format(output))

if colors:
    output.COLORS = colors

print("Gameboard :", gameboard)

artist = output.ArtistSolver(
    solver = solve.Solver(),
    mode   = mode
)
artist.draw(gameboard, folder)
