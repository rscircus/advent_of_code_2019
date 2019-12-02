import math

def get_fuel_requirements():
    arr = list()

    # read in file
    file = open("./1.txt","r")
    for line in file:
        if line:
            arr.append(float(line))

    # calculate fuel requirements
    sum = 0
    for mass in arr:
        mass = int(math.floor(mass / 3.0) - 2)
        sum += mass

    print(sum)

get_fuel_requirements()
