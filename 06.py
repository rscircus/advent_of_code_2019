from collections import defaultdict
# The task today is

# input: map of local orbits

# things orbit each other except the CenterOfMass
# if BBB orbits AAA it is written like `AAA)BBB`
# to verify maps, orbit count checksums are used: the total no of direct orbits and indirect orbits
#
# direct orbits: an object O orbiting directly another one A
# indirect orbits: an object O orbiting all the stuff A is orbiting
#


#lines = open('./6test.txt').read().splitlines()
lines = open('./6.txt').read().splitlines()

# create orbit pairs
orbit_pairs = [s.split(')') for s in lines]

# TODO: There is an efficient function for this: from operator import methodcaller.
#
# Debug:
# print(orbit_pairs)


def create_adjacency_list(orbit_pairs):
    """Returns a graph from orbit pairs based on the root COM."""
    tree = defaultdict(list)
    for pair in orbit_pairs:
        tree[pair[0]].append(pair[1])
    return tree

data = create_adjacency_list(orbit_pairs)
#print(data)

def get_parent(tree, node):
    """returns the parent of a given node or False."""
    for parent, children in tree.items():
        if node in children:
            return parent
    return False

def count_orbits(tree):
    """Counts direct and indirect orbits."""
    direct = 0
    indirect = 0

    # get all direct orbits
    for _, children in tree.items():
        direct += len(children)

        # get all indirect orbits
        for child in children:
            parent = get_parent(tree, _)
            while parent:
                indirect += 1
                parent = get_parent(tree, parent)

    return direct + indirect

# Debug
# adj_list = create_adjacency_list(orbit_pairs)
# print(count_orbits(adj_list))

def count_orbits_jumps(tree):
    """Count the number of orbit jumps needed to reach Santa."""

    # get all direct orbits
    for _, children in tree.items():

        # create my list of ancestors
        if 'YOU' in children:
            you_parents = []
            parent = get_parent(tree, _)
            while parent:
                you_parents.append(parent)
                parent = get_parent(tree, parent)

        # create santas list of ancestors
        elif 'SAN' in children:
            san_parents = []
            parent = get_parent(tree, _)
            while parent:
                san_parents.append(parent)
                parent = get_parent(tree, parent)

    # find lowest common ancestor
    for i, p in enumerate(you_parents):
        if p in san_parents:
            return i + san_parents.index(p) + 2 # add two extra orbits

# part 1
print(count_orbits(data))

# part 2
print(count_orbits_jumps(data))


