import math
from tkinter import Tk, Canvas, mainloop
from random import randrange


class Star:
    __slots__ = ['x', 'y', 'z', 'id', 'radius', 'fill']

    def __init__(self, x, y, z) -> None:
        super().__init__()
        self.id = None
        self.x = x
        self.y = y
        self.z = z
        self.radius = 1
        self.fill = 0


class StarField:

    def __init__(self, width, height, depth=32, num_stars=500):
        self.master = Tk()
        self.master.title("StarField")
        self.master.resizable(False, False)
        self.master.maxsize(width, height)
        self.fov = 180 * math.pi / 180
        self.view_distance = 0
        self.stars = []
        self.width = width
        self.height = height
        self.max_depth = depth
        self.canvas = Canvas(self.master, width=width, height=height, bg="#000000")
        self.canvas.pack()

        for x in range(num_stars):
            star = Star(x=randrange(-self.width, self.width),
                        y=randrange(-self.height, self.height),
                        z=randrange(1, self.max_depth))
            star.id = self.canvas.create_oval(star.x - star.radius, star.y - star.radius, star.x + star.radius, star.y + star.radius,
                                              fill='#FFFFFF')
            self.stars.append(star)
        self.draw()
        mainloop()

    def draw(self):
        for star in self.stars:
            # move depth
            star.z -= 0.19
            star.radius = (1 - float(star.z) / self.max_depth) * 1.7
            star.fill = int((1 - float(star.z) / self.max_depth) * 255)

            # reset depth
            if star.z <= 0:
                star.x = randrange(-self.width, self.width)
                star.y = randrange(-self.height, self.height)
                star.z = self.max_depth
                star.radius = 1
                star.fill = 0

            # Transforms this 3D point to 2D using a perspective projection.
            factor = self.fov / (self.view_distance + star.z)
            x = star.x * factor + self.width / 2
            y = -star.y * factor + self.height / 2

            self.canvas.coords(star.id, x - star.radius, y - star.radius, x + star.radius, y + star.radius)
            self.canvas.itemconfig(star.id, fill='#%02x%02x%02x' % (star.fill, star.fill, star.fill))
        self.canvas.after(30, self.draw)


if __name__ == '__main__':
    s = StarField(800, 600)
