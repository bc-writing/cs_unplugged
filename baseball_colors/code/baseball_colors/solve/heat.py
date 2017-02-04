import random

import solve.model as model

class Solver(model.Solver):
    """
The method used here is to move the hole from left to right and conversely,
and to move the token the farthest from its base.
    """

    def solve(self, gameboard):
        self.gameboard = gameboard

        self.hole_pos      = gameboard.index(None)
        self.most_left_pos = len(gameboard) - 1
        self.last_cell     = self.cell_nb(self.most_left_pos)
        self.direction     = 1

        while(True):
            self.hole_cell = self.cell_nb(self.hole_pos)

# Change of direction ?
            if self.hole_cell == self.last_cell:
                self.direction = -1

            elif self.hole_cell == 0:
                if self.stopmoving():
                    break

                self.direction = 1

# Let's walk.
            yield from self.movehole()


    def stopmoving(self):
        for i, val in enumerate(self.gameboard):
            if val is not None and val != i // 2:
                return False

        return True


    def movehole(self):
        self.from_pos = self.hole_pos

        i  = 2*(self.hole_cell + self.direction)
        ii = i + 1

        if self.gameboard[i] == self.gameboard[ii]:
            next_token_pos = i

        else:
            self.somechges = True

            if self.gameboard[i]  < self.gameboard[ii]:
                minmax = [i, ii]

            else:
                minmax = [ii, i]

            if self.direction == -1:
                minmax.reverse()

            next_token_pos = minmax[0]

# The hole lets its place to the good token.
        self.to_pos = next_token_pos
        self.swap()

        yield self.gameboard

        self.hole_pos = next_token_pos


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
#     gameboard = [0, 1, None, 1, 2, 2, 3, 3, 4, 4]
    gameboard = [None, 0, 2, 2, 1, 1, 3, 3, 4, 4]

    printer = lambda g: [
        "X" if x == None
        else str(x)
        for x in g
    ]

    print("Solving {0}".format(printer(gameboard)))

    for onestep in solver.solve(gameboard):
        print("   ---> {0}".format(printer(onestep)))
