# The task here is two-fold:
#   1. find the intersections of two paths on a 2D-grid
#   2. find the few fewest combined steps the wires must take to reach an intersection

# Basically the first brute force visual solution doesn't work for the correct input data which is way too big. And the first solution also needed a manual inspection to identify the nearest intersection. Hence, I'm trying another approach here using sets.


class Point(object):
    '''Simple point representation.'''
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "x: " + str(self.x) + " y: " + str(self.y)


# Load paths
file = open('./3.txt', 'r')

paths = list()

for line in file:
    paths.append(line.split(','))

wiresets = list()

# Create a set of points covered by each line
for cur_path in paths:

    pos = Point(0, 0)
    wirelength = 0
    wireset = dict()

    for directive in cur_path:
        direction = directive[0]
        stride = int(directive[1:])

        # up or down
        if direction == 'U':
            for y in range(stride):
                pos.y = pos.y + 1
                wirelength += 1
                if (pos.x, pos.y) not in wireset:
                    wireset[(pos.x, pos.y)] = wirelength

        if direction == 'D':
            for y in range(stride):
                pos.y = pos.y - 1
                wirelength += 1
                if (pos.x, pos.y) not in wireset:
                    wireset[(pos.x, pos.y)] = wirelength

        # left or right
        if direction == 'L':
            for x in range(stride):
                pos.x = pos.x - 1
                wirelength += 1
                if (pos.x, pos.y) not in wireset:
                    wireset[(pos.x, pos.y)] = wirelength

        if direction == 'R':
            for x in range(stride):
                pos.x = pos.x + 1
                wirelength += 1
                if (pos.x, pos.y) not in wireset:
                    wireset[(pos.x, pos.y)] = wirelength

    wiresets.append(wireset)

# Check for sizes of these
#print(len(wiresets))
#print(len(wiresets[0]))
#print(len(wiresets[1]))

# This is the intersection of both wires in a Venn style using :
intersections = set(wiresets[0].keys() & wiresets[1].keys())

print(len(intersections))

# Closest intersection
min_intersection = min(abs(x) + abs(y) for (x, y) in intersections)
print(min_intersection) # this is actually an easy way for the first part... :)

# Shortest path to intersections as sum of both wires
min_wirelength = min(wiresets[0][pnt] + wiresets[1][pnt] for pnt in intersections)
print(min_wirelength)