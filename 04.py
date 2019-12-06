# The task here is that the Elves forgot their password but remember a few bits about it:
#
# - It is a six-digit number.
# - The value is within the range given in your puzzle input.
# - Two adjacent digits are the same (like 22 in 122345).
# - Going from left to right, the digits never decrease; they only ever increase or
#   stay the same (like 111123 or 135679).
#
# Further the number of passwords have to be counted in a given range: 128392-643281 (it is for me)

# Answer:
#
# The brute force approach would be to try out all combinations and then count
# the elements in the subset being compliant with the rules above.
#

def numbers_increase(number):
    str_number = str(number)
    for n in range(1, len(str_number)):
        if int(str_number[n-1]) > int(str_number[n]):
            return False

    return True


def no_number_multiples(number):
    str_number = str(number)
    if any([str_number.count(_) == 2 for _ in set(str_number)]):
        return True

    return False


def two_adjecents_are_same(number):
    str_number = str(number)
    for n in range(1, len(str_number)):
        if str_number[n] == str_number[n-1]:
            return True

    return False

# Brute force algo

sum_valid = 0

for _ in range(128392, 643281 + 1):
#    if two_adjecents_are_same(_) and numbers_increase(_):
#        sum_valid += 1
    if numbers_increase(_) and no_number_multiples(_):
        sum_valid += 1

print(sum_valid)

# Test no_number_multiples()
#
#print(no_number_multiples(123456))
#print(no_number_multiples(12223456))
#print(no_number_multiples(12233456))

# Test numbers_increase()
#
#print(numbers_increase(123456))
#print(numbers_increase(12223456))
#print(numbers_increase(12823456))

# Test two_adjecents_are_same()
#
#print(two_adjecents_are_same(1234566))
#print(two_adjecents_are_same(123456))
