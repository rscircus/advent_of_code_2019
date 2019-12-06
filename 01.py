import math

def calc_fuel(mass):
    """Calculate rocket fuel recursively"""

    # rocket fuel equation
    fuel = int(math.floor(mass / 3.0) - 2)

    # base cases in recursive approach
    if fuel > 0:
        return fuel + calc_fuel(fuel)
    else:
        return 0

def get_fuel_requirements():
    """Return fuel requirements of multiple masses."""
    arr = list()

    # read in file
    file = open("./1.txt","r")
    for line in file:
        if line:
            arr.append(float(line))

    # calculate fuel requirements
    sum = 0
    for mass in arr:
        sum += calc_fuel(mass)

    print(sum)

get_fuel_requirements()
