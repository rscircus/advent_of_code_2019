import math

# Load 1.txt
arr = list()
file = open("./1.txt","r")

for line in file:
    if line:
        arr.append(float(line))

# Debug:
# for idx, line in enumerate(arr):
#     print(str(idx) + ": " + str(line))

# For each line in 1

sum = 0
for mass in arr:
    mass = int(math.floor(mass / 3.0) - 2)
    sum += mass

print(sum)

# # Convert to float
# # Divide by 3
# # Floor
# # Subtract 2
# # Sum to previous sum
# Return sum
