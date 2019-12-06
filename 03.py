# The task here is two-fold:
#   1. find the intersections of two paths on a 2D-grid
#   2. calculate the shortest Manhattan distance to another location called port


class Point(object):
    '''Simple point representation.'''
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "x: " + str(self.x) + " y: " + str(self.y)


    # TODO: Refine this to construct an overloaded constructor in Python
    @classmethod
    def from_arguments(cls, args):
        if isinstance(args, int):
            return cls(*args)
        elif isinstance(args, Point):
            return args
        else:
            raise ValueError("Invalid arguments. Should be int or Point.")


origin = 10000

# Load paths
file = open('./3.txt', 'r')

paths = list()

for line in file:
    paths.append(line.split(','))


# Draw paths on grid
# Use a pen which is drawing on some kind of surface
grid = [[0 for x in range(origin*2)] for y in range(origin*2)]
edges = list()

for cur_path in paths:
    # Good start for small testcase 3test1
    pos = Point(origin, origin)

    for directive in cur_path:

        direction = directive[0]
        stride = int(directive[1:])

        start = Point(pos.x, pos.y)

        # Go right
        if direction == 'R':
            for x in range(pos.x, pos.x + stride):
                grid[x][pos.y] += 1
            pos.x = pos.x + stride

        # Go left
        if direction == 'L':
            for x in range(pos.x - stride + 1, pos.x + 1):
                grid[x][pos.y] += 1
            pos.x = pos.x - stride

        # Go up
        if direction == 'U':
            for y in range(pos.y, pos.y + stride):
                grid[pos.x][y] += 1
            pos.y = pos.y + stride

        # Go down
        if direction == 'D':
            for y in range(pos.y - stride + 1, pos.y + 1):
                grid[pos.x][y] += 1
            pos.y = pos.y - stride

        end = Point(pos.x, pos.y)
        edges.append([start, end])



# Get a feeling of what we are doing here:


def print_birdseyeview(view_grid=True):
    '''Visualize what we have drawn here'''
    if view_grid:
        for row in grid:
            print(row)
    else:
        for edge in edges:
            print(edge)


# Debug code
#print_birdseyeview()
#print_birdseyeview(view_grid=False)


# Find intersections


def find_intersections():
    '''Identify all intersections. Using Manhattan distance.'''
    for x, row in enumerate(grid):
        for y, pos in enumerate(row):
            if pos not in {0, 1}:
                print(f"x: {x}, y: {y} = {abs(x - origin) + abs(y -origin)}")


find_intersections()


# tests:

# R75,D30,R83,U83,L12,D49,R71,U7,L72
# U62,R66,U55,R34,D71,R55,D58,R83
# d: 159

# R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
# U98,R91,D20,R16,D67,R40,U7,R15,U6,R7
# d: 135
