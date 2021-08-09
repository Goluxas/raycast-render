import math

from objects import Vector, Line


def intersects(ray: Vector, line: Line) -> bool:
    """
    TODO: This needs to be a few functions I think. What does it do?
    1. Finds intersection
    2. If none exists, returns False
    3. Checks if the intersection point is within the target line segment
    4. If not, returns False
    5. Finds the distance and converts to a height value
    """
    intersection = ray.intersects_at(line)
    if not intersection:
        return False

    if line.contains_point(intersection):
        # return True
        # value max 9 min 1
        # 9 at 1 or less
        # 1 at 10 or more
        distance = intersection.distance((0, 0))
        if distance <= 1:
            value = 9
        elif distance >= 10:
            value = 1
        else:
            """
            factor = 9/9ths of 9 at distance 1, 1/9th of 9 at distance 10
            height is inversely proprotional to distance
            y = mx+b
            h = md+b
            line from (1,9) to (10,1), m = 1-9 / 10-1 = -8/9
            intersect = 9 = (-8/9)(1) + b, 9 = -8/9 + b, b = 9+8/9 = 89/9
            intersect = 1 = (-8/9)(10) + b, 1 = -80/9 + b, b = 9/9 + 80/9 = 89/9
            """
            value = (-8.0 / 9) * distance + (89.0 / 9)
            value = math.floor(value)
        return str(value)
    else:
        return False


def render(player, direction, fov, environment, horizontal_resolution):
    wall = environment.offset(-player)
    starting_view_vector = direction.rotate(fov / 2)
    d_theta = fov / horizontal_resolution

    out = ""

    for i in range(horizontal_resolution):
        view_vector = starting_view_vector.rotate(-d_theta * i)
        value = intersects(view_vector, wall)
        if value:
            out += value
        else:
            out += "."

    print(out)


if __name__ == "__main__":
    player = Vector(0, 0)
    direction = Vector(0.5, 0.5)
    fov: float = math.pi / 2  # 90 degrees
    wall = Line(Vector(1, 5), Vector(5, 1))
    resolution = 100

    # move player around the wall widely
    time_per_action = 5
    d_theta = (-math.pi / 2) / time_per_action  # -90 degrees = turn right 90 degrees
    d_pos = (
        7 / time_per_action
    )  # since we're moving straight vertical/horizontal this is easy

    # 0, 0 -> 0, 7
    for dt in range(time_per_action):
        render(player, direction, fov, wall, resolution)
        player = player + (0, d_pos)
    print("Walked North")
    # rotate view 90 degrees right
    for dt in range(time_per_action):
        render(player, direction, fov, wall, resolution)
        direction = direction.rotate(d_theta)
    print("Turned right")
    # 0, 7 -> 7, 7
    for dt in range(time_per_action):
        render(player, direction, fov, wall, resolution)
        player = player + (d_pos, 0)
    print("Walked East")
    # rotate view 90 degrees right
    for dt in range(time_per_action):
        render(player, direction, fov, wall, resolution)
        direction = direction.rotate(d_theta)
    print("Turned right")
    # 7, 7 -> 7, 0
    for dt in range(time_per_action):
        render(player, direction, fov, wall, resolution)
        player = player + (0, -d_pos)
    print("Walked South")
    # rotate view 90 degrees right
    for dt in range(time_per_action):
        render(player, direction, fov, wall, resolution)
        direction = direction.rotate(d_theta)
    print("Turned right")

    """
    # simulate turning left over time
    # let's say, turn 90 degrees left in 20 frames
    total_turn = math.pi / 2
    frames = 20
    turn_per_frame = total_turn / frames
    for i in range(frames):
        cur_dir = direction.rotate(turn_per_frame * i)
        render(cur_dir, fov, wall, steps)
    """
