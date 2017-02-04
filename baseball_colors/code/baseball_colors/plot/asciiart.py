class ArtistSolver():
    def __init__(self, solver, *args, **kwargs):
        self.solver = solver

    def draw(self, gameboard, *args, **kwargs):
        self.size = len(gameboard)

        if self.size > 20:
            raise ValueError("game with more than 10 bases is not supported")

        print(self.draw_oneline(gameboard))

        for onestep in self.solver.solve(gameboard):
            print(self.draw_oneline(onestep))

    def stringify(self, token):
        if token is None:
            return "X"

        else:
            return token

    def draw_oneline(self, gameboard):
        return "  ".join(
            "[{0}.{1}]".format(
                self.stringify(gameboard[i]),
                self.stringify(gameboard[i + 1])
            )
            for i in range(0, self.size, 2)
        )
