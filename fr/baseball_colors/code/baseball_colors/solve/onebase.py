import random

import solve.model as model


class Solver(model.Solver):
    """
The method used here is to sort the values from the highest in the left side
to the lowest in the right side.
    """

    def solve(self, gameboard):
        self.gameboard = gameboard

        self.hole_pos       = gameboard.index(None)
        self.most_right_pos = len(gameboard) - 1
        self.last_cell      = self.cell_nb(self.most_right_pos)

        while(self.last_cell != 0):
# Do we have a new "last" cell ?
            if self.find_new_cell_filled():
                self.most_right_pos -= 2
                self.last_cell      -= 1
                continue

# Moving of the hole and then of the token.
            self.token_pos = self.token_to_move()

            yield from self.move_hole()
            yield from self.move_token()


    def find_new_cell_filled(self):
        return self.gameboard[self.most_right_pos] == self.last_cell \
               and self.gameboard[self.most_right_pos - 1] == self.last_cell


    def token_to_move(self):
        pos_1 = self.gameboard.index(self.last_cell)
        pos_2 = self.gameboard.index(self.last_cell, pos_1 + 1)

        if self.cell_nb(pos_2) != self.last_cell:
            return pos_2

        else:
            return pos_1


    def build_next_token_pos(self, cell):
        pos_1 = 2*cell
        pos_2 = pos_1 + 1

        col_1 = self.gameboard[pos_1]
        col_2 = self.gameboard[pos_2]

        if col_1 == col_2:
            self.to_pos = random.randint(pos_1, pos_2)

        elif col_1 == self.last_cell:
            self.to_pos = pos_2

        elif col_2 == self.last_cell:
            self.to_pos = pos_1

        else:
            self.to_pos = random.randint(pos_1, pos_2)


    def move_hole(self):
        token_next_cell = self.cell_nb(self.token_pos) + 1
        hole_cell       = self.cell_nb(self.hole_pos)

# Nothing to do.
        if hole_cell == token_next_cell:
            return

# Moving the hole to the cell at the left of the cell of the token.
        if hole_cell < token_next_cell:
            cellrange = range(hole_cell + 1, token_next_cell + 1)

        else:
            cellrange = range(hole_cell - 1, token_next_cell - 1, -1)

        self.from_pos = self.hole_pos

        for i in cellrange:
            self.build_next_token_pos(cell = i)
            self.swap()
            self.from_pos = self.to_pos

            yield self.gameboard

        self.hole_pos = self.to_pos


    def move_token(self):
        nextcell = self.cell_nb(self.token_pos) + 1

        while(nextcell <= self.last_cell):
# Swaping the hole and the token.
            self.from_pos = self.token_pos
            self.to_pos   = self.hole_pos
            self.swap()

            yield self.gameboard

            self.hole_pos  = self.from_pos
            self.token_pos = self.to_pos

# The hole goes back to the left.
            if nextcell != self.last_cell:
                yield from self.move_hole()

            nextcell += 1
