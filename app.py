import math

import pyglet
from pyglet.window import key
from pyglet import shapes

from objects import Vector, Line

# initialize
# CONSTANTS
# the render screen
SCREEN = {
    "width": 960,
    "height": 540,
}
FIELD = {
    "width": 100,
    "height": 100,
}
START_POSITION = Vector(FIELD["width"] // 2, FIELD["height"] // 2)
START_VIEW_DIR = Vector(0, 1)

# Game objects
# the game field
class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._set_bound_lines()

    def _set_bound_lines(self):
        bound_N = Line((0, 0), (self.width, 0))
        bound_E = Line((self.width, 0), (self.width, self.height))
        bound_S = Line((0, self.height), (self.width, self.height))
        bound_W = Line((0, 0), (0, self.height))

        self.lines = [bound_N, bound_E, bound_S, bound_W]

    def init_render(self, game):
        self.repr = []
        for line in self.lines:
            line.init_render(game)
            self.repr.append(line.repr)


# the player object
class Player:
    # should have set all consts like this, i think
    size = 3
    fov = math.pi / 2

    def __init__(self, pos: Vector, view: Vector):
        self.position = pos
        self.view_dir = view

    def init_render(self, game):
        point = shapes.Circle(
            self.position.x, self.position.y, radius=self.size, batch=game.batch
        )
        view_cone_L_line = Line(
            self.position,
            self.view_dir.rotate(self.fov / 2).intersects_at(
                self.view_dir.intersects_which(game.field.lines)
            ),
        )
        view_cone_R_line = Line(
            self.position,
            self.view_dir.rotate(-self.fov / 2).intersects_at(
                self.view_dir.intersects_which(game.field.lines)
            ),
        )

        view_cone_L = view_cone_L_line.init_render(game)
        view_cone_R = view_cone_R_line.init_render(game)

        self.repr = (point, view_cone_L, view_cone_R)


# objects in the game
class Game(pyglet.window.Window):
    player = Player(START_POSITION, START_VIEW_DIR)
    field = Field(FIELD["width"], FIELD["height"])

    def __init__(self, width, height):
        super().__init__(width, height)
        self.batch = pyglet.graphics.Batch()

        self.player.init_render(self)
        self.field.init_render(self)

    def on_draw(self):
        self.clear()
        self.batch.draw()


if __name__ == "__main__":
    game = Game(
        SCREEN["width"], SCREEN["height"]
    )  # consider would state = AppState() fit here?
    event_logger = pyglet.window.event.WindowEventLogger()
    game.push_handlers(event_logger)
    pyglet.app.run()
