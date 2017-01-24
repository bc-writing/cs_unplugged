# Source: https://nickcharlton.net/posts/drawing-animating-shapes-matplotlib.html


# mogrify -trim *.png
# mogrify -trim -mattecolor white -frame 10x10 *.png


from math import inf as infinity
from cmath import exp, pi, sin

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mplcolors

class ArtistSolver():
    """
mode = circle,
       snake (des carrées alignées avec retour à la ligne)
       1 ---> 2 ---> 3 ---> 4
                            |
                            ^
       8 <--- 7 <--- 6 <--- 5
       |
       ^
       9 ---> ...
    """

    def __init__(self, solver, mode = "circle", radius = 5):
        self.solver = solver

        self.drawer = globals()[
            "{0}{1}".format(
                mode[0].upper(),
                mode[1:]
            )
        ]()

        self.radius = radius

    def draw(self, gameboard, folder, *args, **kwargs):
        """
folder est une classe de type pathlib.Path où stocker les images
        """
        self.drawer.draw(
            gameboard = gameboard,
            filepath  = folder / "000.png",
            radius    = self.radius
        )

        for i, onestep in enumerate(self.solver.solve(gameboard), 1):
            self.drawer.draw(
                gameboard = onestep,
                filepath  = folder / "{0:03d}.png".format(i),
                radius    = self.radius
            )


def colormap(val, maxval, border = "w", style = "jet"):
    if val is None:
        color = "w"

    elif maxval <= 7:
# b: blue
# g: green
# r: red
# c: cyan
# m: magenta
# y: yellow
# k: black
# w: white
        colors = [x for x in "kbgyrcm"]
        color  = colors[val]

    else:
        my_cmap = cm.get_cmap(style)
        norm = mplcolors.Normalize(0, maxval)
        color = my_cmap(norm(val))

    return [border, color]

class Drawer():
    def __init__(self):
# Let's clear the entire figure
        plt.clf()
    #     self.reset_minmax()
    #
    # def reset_minmax(self):
    #     self.xmin, self.xmax = self.ymin, self.ymax = infinity, - infinity

    def save(self, path):
        plt.savefig(
            str(path),
            dpi         = 72,
            bbox_inches ='tight',
            pad_inches  = 0,
            transparent = True
        )

    # def update_minmax(self, x, y):
    #     if x < self.xmin:
    #         self.xmin = x
    #
    #     if x > self.xmax:
    #         self.xmax = x
    #
    #     if y < self.ymin:
    #         self.ymin = y
    #
    #     if y > self.ymax:
    #         self.ymax = y

    def add_shape(self, shape):
        plt.gca().add_patch(shape)

    def add_rectangle(self, ld_corner, dims, colors):
        # self.update_minmax(
        #     x = ld_corner[0],
        #     y = ld_corner[1]
        # )
        #
        # self.update_minmax(
        #     x = ld_corner[0] + dims[0],
        #     y = ld_corner[1] + dims[1]
        # )

        self.add_shape(
            plt.Rectangle(
                ld_corner,
                dims[0], dims[1],
                color = colors[0],
                fc    = colors[1]
            )
        )

    def add_circle(self, center, radius, colors, alpha = 1):
        # self.update_minmax(
        #     x = center[0] - radius,
        #     y = center[1] - radius
        # )
        #
        # self.update_minmax(
        #     x = center[0] + radius,
        #     y = center[1] + radius
        # )

        self.add_shape(
            plt.Circle(
                center,
                radius = radius,
                color  = colors[0],
                fc     = colors[1],
                lw     = 2,
                alpha  = alpha
            )
        )


class Circle(Drawer):
    def draw(self, gameboard, filepath, radius):
        plt.clf()

        token_radius = radius/4

        bases    = list(zip(gameboard[::2], gameboard[1::2]))
        nb_bases = len(bases)

        alpha = 2 * pi / nb_bases

# Good big radius for bases not interecting (1.2 is an emprici choice).
        big_radius = radius/sin(alpha/2)*1.2

        angle = 0

        for i, onebase in enumerate(bases):
            c = big_radius*exp(angle*1j)

# Draw one base
            colors = colormap(
                val    = i,
                maxval = nb_bases,
                border = "k"
            )

            self.add_circle(
                center = [c.real, c.imag],
                radius = radius,
                colors = colors,
                alpha  = 0.65
            )

# Draw the tokens on that base
            ctoken = (big_radius + 2*token_radius)*exp(angle*1j)
            colors = colormap(val = onebase[0], maxval = nb_bases)

            self.add_circle(
                center = [ctoken.real, ctoken.imag],
                radius = token_radius,
                colors = colors
            )

            ctoken = (big_radius - 2*token_radius)*exp(angle*1j)
            colors = colormap(val = onebase[1], maxval = nb_bases)

            self.add_circle(
                center = [ctoken.real, ctoken.imag],
                radius = token_radius,
                colors = colors
            )

# Let's continue.
            angle += alpha

# Setting the axes
        plt.axis('scaled')
        plt.axis('off')

        self.save(filepath)


class Line(Drawer):
    def draw(self, gameboard, filepath, radius):
        plt.clf()

        token_radius = radius/4

        bases    = list(zip(gameboard[::2], gameboard[1::2]))
        nb_bases = len(bases)

# Let's go
        gap = radius*0.3

        xcenter = 0

        for i, onebase in enumerate(bases):
# Draw one base
            colors = colormap(
                val    = i,
                maxval = nb_bases,
                border = "k"
            )

            self.add_circle(
                center = [xcenter, 0],
                radius = radius,
                colors = colors,
                alpha  = 0.65
            )

# Draw the tokens on that base
            ytoken = 2*token_radius
            colors = colormap(val = onebase[0], maxval = nb_bases)

            self.add_circle(
                center = [xcenter, ytoken],
                radius = token_radius,
                colors = colors
            )

            colors = colormap(val = onebase[1], maxval = nb_bases)

            self.add_circle(
                center = [xcenter, -ytoken],
                radius = token_radius,
                colors = colors
            )

# Let's continue
            xcenter += 2*radius + gap

# Setting the axes
        plt.axis('scaled')
        plt.axis('off')

        self.save(filepath)


class Snake(Drawer):
    def draw(self, gameboard, filepath, radius):
        print(gameboard, filepath)
