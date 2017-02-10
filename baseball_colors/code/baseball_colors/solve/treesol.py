from copy import copy
from json import dump, load
import random

import solve.model as model


class Solver(model.Solver):
    """
The method used here uses the following method.

    1) From the winning configuration ``WinConf``, we just look for the
    configurations obtained by moving just one token from the WinConf.

    2) Then for each new configurations, we just look for the
    configurations obtained by moving just one token from all of them.
    We obtain a new set of new configurations.

    3) We repeat the second step until no new configuration appears.


The class also keeps the paths obtained from ``WinConf`` to a configuration.
This gives the shortest paths !
    """

    def build_tree(self):
# We start by the winnning gameboard.
        gameboard = [None, 0]

        for x in range(1, self.size // 2):
            gameboard += [x, x]

        self.allgameboards = self.nextboards = [gameboard]

# Specifications for ``self.moves``.
#
#     * Each key is the index of one gameboard found.
#
#     * Each value is the list of indexes, from teh farest to the nearest,
#       of the gameboards used to obtain the gameboard. We don't put the
#       zero indicating the winning gameboard.
        self.moves = {0: []}

        actual_id = 0

        while self.nextboards:
            nextboards = []

            for parent_id, oneboard in self.build_nextboards():
# One new gameboard.
                if oneboard not in self.allgameboards:
                    nextboards.append(oneboard)

                    self.allgameboards.append(oneboard)
                    actual_id += 1

                    self.moves[actual_id] = [parent_id] + self.moves[parent_id]

            self.nextboards = nextboards


    @property
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


    def sort(self, x = None, y = None):
        if x is None or y is None:
            for x in range(0, self.size, 2):
                self.sort(x, x + 1)

        elif self.gameboard[x] is not None:
            if self.gameboard[y] is None \
            or self.gameboard[x] > self.gameboard[y]:
                self.gameboard[y], self.gameboard[x] \
                = self.gameboard[x], self.gameboard[y]


    def normalize(self):
# The smallest token or the hole must be at the left position.
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
            onegameboard_id = self.allgameboards.index(onegameboard)

            self.gameboard = copy(onegameboard)
            self.from_pos  = onegameboard.index(None)

            for onepos in self.next_pos:
                self.to_pos = onepos
                self.swap()
                self.normalize()

                yield onegameboard_id, self.gameboard
                self.gameboard = copy(onegameboard)


    def usergameboard(self):
        usergameboard = copy(self.lastgameboard)

        hole_start = self.lastgameboard.index(None)
        hole_end   = self.nextgameboard.index(None)

        other_start = self.neighboor_pos(hole_start)
        other_end   = self.neighboor_pos(hole_end)

# Right tokens at the right place...
        for hpos, opos in [
            (hole_start, other_start),
            (hole_end, other_end)
        ]:
            if self.lastgameboard[opos] == self.nextgameboard[opos]:
                self.lastgameboard[hpos] = self.nextgameboard[hpos]

            else:
                self.lastgameboard[hpos], self.lastgameboard[opos] \
                = self.nextgameboard[opos], self.nextgameboard[hpos]

        return self.lastgameboard


    def solve(self, gameboard):
        self.size = len(gameboard)

        self.build_tree()

# We need to normalize the gameboard.
        self.gameboard = copy(gameboard)
        self.sort()
        gameboard_id  = self.allgameboards.index(self.gameboard)

        self.lastgameboard = copy(gameboard)

# We have to show the right position for the hole because we work with
# normalized representations of the gameboard.
        for oneid in self.moves[gameboard_id]:
            self.nextgameboard = self.allgameboards[oneid]

            yield self.usergameboard()
