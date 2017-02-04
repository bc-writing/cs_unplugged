class Solver():
    """
The main method of this class is ``solve`` which is an iterator yielding each
step of the solving.

The game board is modelized usin a list of integer and None for the hole.
    """

    def solve(self):
        raise NotImplementedError("the method ``solve`` must be implemented")

    def swap(self):
        self.gameboard[self.to_pos], self.gameboard[self.from_pos] \
        = self.gameboard[self.from_pos], self.gameboard[self.to_pos]

    def cell_nb(self, pos):
        return pos // 2

    def neighboor_pos(self, pos):
        if pos % 2 == 0:
            return pos + 1

        return pos - 1
