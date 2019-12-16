# We are close to jupiter
# round trip signals to Earth take 5 hours and signal quality is bad
# FFT - Flawed Frequency Transmission algo

# phase
# : len(output) = len(input)
# use the random walky base_pattern = [0, 1, 0, - 1]
# repeat it all the time as the right hand side
# for each output position we create some kind of scalar product, which looks roughly like this:

# test input for phase algo
#input = list("19617804207202209144916044189917")
#input = list("80871224585914546619083218645595")
input = list("59728839950345262750652573835965979939888018102191625099946787791682326347549309844135638586166731548034760365897189592233753445638181247676324660686068855684292956604998590827637221627543512414238407861211421936232231340691500214827820904991045564597324533808990098343557895760522104140762068572528148690396033860391137697751034053950225418906057288850192115676834742394553585487838826710005579833289943702498162546384263561449255093278108677331969126402467573596116021040898708023407842928838817237736084235431065576909382323833184591099600309974914741618495832080930442596854495321267401706790270027803358798899922938307821234896434934824289476011")
input = list(map(int, input))

def scalar_prod(lhs, rhs):
    """Multiplies the vector lhs to the vector rhs. Assuming len(rhs) == len(lhs)."""

    output = list()
    for i in range(len(lhs)):
        output.append(lhs[i]*rhs[i])

    return sum(output)

# Make create_phase_vector more efficient
phase_vector_memo = {}

def create_phase_vector(index, size):
    """Returns a rhs to the scalar_prod and saves it for a given position."""

    if index in phase_vector_memo:
        return phase_vector_memo[index]

    position = index + 1

    rhs = list()

    forward = True
    clock = 0

    # clock is shifted after entry in rhs for correct tail
    while len(rhs) < size + 1:

        expr = [clock] * position
        rhs.extend(expr)

        # TODO: simplify this
        if forward:
            if clock == 1:
                forward = False
                clock = 0
            else:
                clock += 1
        else:
            if clock == -1:
                forward = True
                clock = 0
            else:
                clock -= 1

    # pop most left item
    rhs.pop(0)

    # trim right
    del rhs[size:]

    phase_vector_memo[index] = rhs

    return rhs

def calc_phases(input, count):
    """Calculates output after count phases."""

    size = len(input)

    cur_input = input
    cur_output = [0]*size

    for phase in range(count):

        # overwrite if not first try
        if phase != 0:
            cur_input = cur_output

        for index in range(size):
            rhs = create_phase_vector(index, size)
            cur_output[index] = abs(scalar_prod(cur_input, rhs)) % 10

    return cur_output

#input = list(map(int, list("12345678")))
#print(input)
#print(calc_phases(input, 100))

# Tests
#print(scalar_prod([1,2,3],[4,5,6]))
#scalar_prod([1,2,3],[4,5,6,7])

#rhs = create_phase_vector(0, 15)
#print(rhs)
#print(len(rhs))

# Part 2
#input = input*10000
#print(input)
#print(calc_phases(input, 100))
# stuff is getting sloooooww....
# even though my memo is nice. :)

# Switching to stack overflow based numpy here...
# The key insight is, that this huge offset becomes simply a sum, as a 0 as
# rhs would cancel out everything and the sign is truncated either way.
import numpy as np
input_np = np.array([int(i) for i in input]*10000)
offset = int(''.join(map(str,input[0:7])))
print(offset)

def calc_phases_huge(input_, count):
    """Calculates output after count phases."""

    for i in range(count):
        # Cumulative sum of reversed string
        input_ = np.cumsum(input_[::-1]) % 10
        input_ = input_[::-1]

    # we're interested in the first 8 digits only
    return input_[0:8]

print(calc_phases_huge(input_np[offset:], 100))
