from copy import copy
from json import dump, load
import random

import solve.model as model




def nonone(onelist):
    return [
        -1 if x is None
        else x
        for x in onelist
    ]



class Solver(model.Solver):
    """
The method used here is ????
    """

    def build_tree(self):
        gameboard = [None, 0]

        for x in range(1, self.size // 2):
            gameboard += [x, x]

        self.allgameboards = self.nextboards = [gameboard]
        self.moves         = {}
        self.oneboard      = None

        while self.nextboards:
            nextboards = []

            for oneboard in self.build_nextboards():
                if oneboard not in self.allgameboards:
                    print(len(self.allgameboards))

                    nextboards.append(oneboard)

                    self.allgameboards.append(oneboard)

            self.nextboards = nextboards

        self.allgameboards.sort(key = lambda x: nonone(x))

        for i, x in enumerate(self.allgameboards, 1):
            print(i, x)
        exit()
    def next_pos(self):
        hole_pos = self.from_pos

        if hole_pos % 2 == 1:
            hole_pos -= 1

        allpos = [
            (hole_pos + delta) % self.size
            for delta in [-2, -1, 2, 3]
        ]

        for i, j in [(2, 3), (0, 1)]:
            if self.gameboard[allpos[i]] == self.gameboard[allpos[j]]:
                del allpos[j]

        return allpos

    def sort(self, x, y):
        if self.gameboard[x] is not None:
            if self.gameboard[y] is None \
            or self.gameboard[x] > self.gameboard[y]:
                self.gameboard[y], self.gameboard[x] \
                = self.gameboard[x], self.gameboard[y]

    def normalize(self):
# On met le plus petit à droite.
# On met le trou à droite.
        for onepos in [
            self.from_pos,
            self.to_pos
        ]:
            if onepos % 2 == 0:
                x, y = onepos, onepos + 1

            else:
                x, y = onepos - 1, onepos

            self.sort(x, y)


    def build_nextboards(self):
        for onegameboard in self.nextboards:
            self.gameboard = copy(onegameboard)
            self.from_pos = onegameboard.index(None)

            for onepos in self.next_pos():
                self.to_pos = onepos
                self.swap()
                self.normalize()

                yield self.gameboard
                self.gameboard = copy(onegameboard)


    def solve(self, gameboard):
        self.size = len(gameboard)

        self.build_tree()


# --------------------- #
# -- FOR BASIC TESTS -- #
# --------------------- #

if __name__ == "__main__":
    size   = 5
    solver = Solver()

    gameboard = [None] + list(range(1, size)) + list(range(size))
    random.shuffle(gameboard)

# Bugs found
#     gameboard = [3, 3, None, 1, 0, 1, 2, 2, 4, 4, 5, 5]

    printer = lambda g: [
        "X" if x == None
        else str(x)
        for x in g
    ]

    print("Solving {0}".format(printer(gameboard)))

    for onestep in solver.solve(gameboard):
        print("   ---> {0}".format(printer(onestep)))
