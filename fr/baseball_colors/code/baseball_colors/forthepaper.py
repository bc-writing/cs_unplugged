from collections import OrderedDict
from copy import copy
from pathlib import Path
import random

from solve import treesol
from plot import picture

folder = Path("/Users/projetmbc/tests")

size      = 3
gameboard = [None] + list(range(size)) + list(range(1, size))

picture.COLORS = "kry"
drawer = picture.Line()

solver = treesol.Solver()

solver.size = len(gameboard)
solver.build_tree()


# All the gameboards with good positions !
allgameboards = solver.allgameboards
themoves      = solver.moves

depth    = 0
gotonext = True

while(gotonext):
    depth   += 1
    gotonext = False

    for board_id, parents in themoves.items():
        if len(parents) == depth:
            gotonext = True

            solver.lastgameboard = copy(allgameboards[parents[0]])
            solver.nextgameboard = copy(allgameboards[board_id])

            allgameboards[board_id] = copy(solver.usergameboard())


# Let's build the pictures.
for board_id, board in enumerate(allgameboards):
    drawer.draw(
        gameboard = allgameboards[board_id],
        filepath  = folder / "moves/{0}.png".format(board_id),
        radius    = 5
    )


# LaTeX output.

def update_tree(parents, onedict):
    oldest = parents[0]
    childs = parents[1:]

    if oldest not in onedict:
        onedict[oldest] = OrderedDict()


    if childs:
        onedict[oldest] = update_tree(
            parents = childs,
            onedict = onedict[oldest]
        )

    return onedict


tree_of_sol = OrderedDict()

for board_id, parents in solver.moves.items():
    if parents:
        parents.reverse()
        parents.append(board_id)

        tree_of_sol = update_tree(parents, tree_of_sol)


# TiKz.

tikztemplate = r"""
\begin<<center>>
    \begin<<tikzpicture>>[
    rotate={rotate},
    level distance={distance},
{sibling}
    ]
    {tikztree}
    \end<<tikzpicture>>
\end<<center>>
"""

tikznode = r"node<<\includegraphics[scale={scale}]<<content/optimal/tree_sol/moves/{nb}.png>>>>"

# tikznode = r"node<<{0}>>"

tikzchild = r"child<<{0}>>"

tikzconfigs = {
    3 : {
        "scale"  : 0.14,
        "sibling": ["5cm", "2.25cm"],
        "rotate" : 0,
        "distance": "1.5cm"
    },
    4 : {
        "scale"  : 0.12,
        "sibling": ["8.5cm", "4.75cm", "2cm"],
        "rotate" : 0,
        "distance": "1.5cm"
    },
    7 : {
        "scale"   : 0.12,
        "sibling" : ["10cm", "5cm", "2cm", "1cm", "0.5cm"],
        "rotate"  : 90,
        "distance": "2.5cm"
    },
}


def tikzslibing():
    global config

    onelevel = " "*8 + "level {0}/.style=<<sibling distance={1}>>,"

    lines = []
    for i, length in enumerate(config["sibling"], 1):
        lines.append(onelevel.format(i, length))

    return "\n".join(lines)

def latexclean(text):
    return text.replace("<<", "{") \
               .replace(">>", "}")

def latexlines(onedict, depth = 0):
    global config, depthmax

    lines = []

    if depth < depthmax:
        for key, val in onedict.items():
            content  = [
                tikznode.format(
                    scale = config["scale"],
                    nb    = key
                )
            ]
            sublines = latexlines(val, depth + 1)

            if sublines:
                if depth < depthmax - 1:
                    content.append(
                        "\n".join([
                            tikzchild.format(x) for x in sublines
                        ])
                    )

                else:
                    content.append("\n".join(sublines))

            lines.append("\n".join(content))

    return lines

for depthmax in tikzconfigs:
    config = tikzconfigs[depthmax]

    tikztree = "\n".join(latexlines(tree_of_sol))
    tikztree = "\\" + tikztree + ";"

    with open(
        file = str(folder / "depthmax-{0}.tikz".format(depthmax)),
        mode = "w"
    ) as f:
        f.write(
            latexclean(
                tikztemplate.format(
                    sibling  = tikzslibing(),
                    rotate   = config["rotate"],
                    distance = config["distance"],
                    tikztree = tikztree
                )
            )
        )
