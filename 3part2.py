# The task here is two-fold:
#   1. find the intersections of two paths on a 2D-grid
#   2. find the few fewest combined steps the wires must take to reach an intersection

# Basically the first brute force visual solution doesn't work for the correct input data which is way too big. And the first solution also needed a manual inspection to identify the nearest intersection. Hence, I'm trying another approach here using sets.

# Load paths
file = open('./3.txt', 'r')

paths = list()

for line in file:
    paths.append(line.split(','))

# Create a set of points covered by each line

# Collect a dictionary containing all intersections and the lengths of the wires up to that point

# Identify the minimum
