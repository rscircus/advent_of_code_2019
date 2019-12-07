from itertools import permutations, chain

# Amplification Circuit
#
# The task today is to extend the Intcode computer from day 5, let's copy it over.
#
# The task is to write a simple ALU/CPU here.

# New from day 07:
#
# Try all input combination in the range [0,4] for a set of computers to
# maximize the output of 5 connected 'amplifiers'.
#
# The computer now receives two inputs:
# - the known input
# - a phase setting
#
# Each amplifier receives a phase setting from the combination and an input
# from its previous amplifier's output. Except the first amplifier, which
# receives a 0 in the example.
#

# Test case amplifier:
# Max thruster signal 43210 (from phase setting sequence 4,3,2,1,0):
test_amp_simple = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]

# Tests:
#
# 1,0,0,0,99 becomes 2,0,0,0,99 (1 + 1 = 2).
# 2,3,0,3,99 becomes 2,3,0,6,99 (3 * 2 = 6).
# 2,4,4,5,99,0 becomes 2,4,4,5,99,9801 (99 * 99 = 9801).
# 1,1,1,4,99,5,6,0,99 becomes 30,1,1,4,2,5,6,0,99.

test_add = [1,1,1,4,99,5,6,0,99]
test_mul = [2,4,4,5,99,0]
test_mul_result = [2,4,4,5,99,9801]
test_add_result = [30,1,1,4,2,5,6,0,99]

# Task memory
gravity_assist_clear = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,9,1,19,1,19,5,23,1,23,6,27,2,9,27,31,1,5,31,35,1,35,10,39,1,39,10,43,2,43,9,47,1,6,47,51,2,51,6,55,1,5,55,59,2,59,10,63,1,9,63,67,1,9,67,71,2,71,6,75,1,5,75,79,1,5,79,83,1,9,83,87,2,87,10,91,2,10,91,95,1,95,9,99,2,99,9,103,2,10,103,107,2,9,107,111,1,111,5,115,1,115,2,119,1,119,6,0,99,2,0,14,0]
gravity_assist_dirty = [1,12,2,3,1,1,2,3,1,3,4,3,1,5,0,3,2,9,1,19,1,19,5,23,1,23,6,27,2,9,27,31,1,5,31,35,1,35,10,39,1,39,10,43,2,43,9,47,1,6,47,51,2,51,6,55,1,5,55,59,2,59,10,63,1,9,63,67,1,9,67,71,2,71,6,75,1,5,75,79,1,5,79,83,1,9,83,87,2,87,10,91,2,10,91,95,1,95,9,99,2,99,9,103,2,10,103,107,2,9,107,111,1,111,5,115,1,115,2,119,1,119,6,0,99,2,0,14,0]
test_program = [3,225,1,225,6,6,1100,1,238,225,104,0,1102,46,47,225,2,122,130,224,101,-1998,224,224,4,224,1002,223,8,223,1001,224,6,224,1,224,223,223,1102,61,51,225,102,32,92,224,101,-800,224,224,4,224,1002,223,8,223,1001,224,1,224,1,223,224,223,1101,61,64,225,1001,118,25,224,101,-106,224,224,4,224,1002,223,8,223,101,1,224,224,1,224,223,223,1102,33,25,225,1102,73,67,224,101,-4891,224,224,4,224,1002,223,8,223,1001,224,4,224,1,224,223,223,1101,14,81,225,1102,17,74,225,1102,52,67,225,1101,94,27,225,101,71,39,224,101,-132,224,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,1002,14,38,224,101,-1786,224,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1,65,126,224,1001,224,-128,224,4,224,1002,223,8,223,101,6,224,224,1,224,223,223,1101,81,40,224,1001,224,-121,224,4,224,102,8,223,223,101,4,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,226,224,1002,223,2,223,1005,224,329,1001,223,1,223,107,677,677,224,102,2,223,223,1005,224,344,101,1,223,223,1107,677,677,224,102,2,223,223,1005,224,359,1001,223,1,223,1108,226,226,224,1002,223,2,223,1006,224,374,101,1,223,223,107,226,226,224,1002,223,2,223,1005,224,389,1001,223,1,223,108,226,226,224,1002,223,2,223,1005,224,404,1001,223,1,223,1008,677,677,224,1002,223,2,223,1006,224,419,1001,223,1,223,1107,677,226,224,102,2,223,223,1005,224,434,1001,223,1,223,108,226,677,224,102,2,223,223,1006,224,449,1001,223,1,223,8,677,226,224,102,2,223,223,1006,224,464,1001,223,1,223,1007,677,226,224,1002,223,2,223,1006,224,479,1001,223,1,223,1007,677,677,224,1002,223,2,223,1005,224,494,1001,223,1,223,1107,226,677,224,1002,223,2,223,1006,224,509,101,1,223,223,1108,226,677,224,102,2,223,223,1005,224,524,1001,223,1,223,7,226,226,224,102,2,223,223,1005,224,539,1001,223,1,223,8,677,677,224,1002,223,2,223,1005,224,554,101,1,223,223,107,677,226,224,102,2,223,223,1006,224,569,1001,223,1,223,7,226,677,224,1002,223,2,223,1005,224,584,1001,223,1,223,1008,226,226,224,1002,223,2,223,1006,224,599,101,1,223,223,1108,677,226,224,102,2,223,223,1006,224,614,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,629,1001,223,1,223,8,226,677,224,1002,223,2,223,1006,224,644,101,1,223,223,1007,226,226,224,102,2,223,223,1005,224,659,101,1,223,223,108,677,677,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226]

def digits(number):
    """Returns a list of digits in number."""
    for digit in str(number):
        yield digit

def explode(memory, pointer):
    """Returns 4 values extracted from the instruction in memory in the following order: opcode, p1mode, p2mode, p3mode"""

    instruction = memory[pointer]

    # Get list of digits from instruction
    digit_list = list(map(int, digits(instruction)))

    # Create full instruction if leading zeroes are missing
    digit_list = [0]*(5 - len(digit_list)) + digit_list

    # Get opcode
    opcode = digit_list[-1] if digit_list[-2] == 0 else digit_list[-2]*10 + digit_list[-1]

    # Get parameters
    p1mode = digit_list[-3]
    p2mode = digit_list[-4]
    p3mode = digit_list[-5]

    return opcode, p1mode, p2mode, p3mode

def compute(memory, input):
    """My small tiny sweet little computer."""

    instruction_pointer = 0

    output = None

    # execute instructions
    while(memory[instruction_pointer] != 99):

        opcode, p1mode, p2mode, p3mode = explode(memory, instruction_pointer)
        # Debug:
        # print(f"IP: {instruction_pointer} \t instruction: {memory[instruction_pointer]} \t opcode: {opcode}")

        # add
        if opcode == 1:
            left_hand = memory[memory[instruction_pointer + 1]] if p1mode == 0 else memory[instruction_pointer + 1]
            right_hand = memory[memory[instruction_pointer + 2]] if p2mode == 0 else memory[instruction_pointer + 2]
            memory[memory[instruction_pointer + 3]] = left_hand + right_hand
            instruction_pointer += 4

        # multiply
        if opcode == 2:
            left_hand = memory[memory[instruction_pointer + 1]] if p1mode == 0 else memory[instruction_pointer + 1]
            right_hand = memory[memory[instruction_pointer + 2]] if p2mode == 0 else memory[instruction_pointer + 2]
            memory[memory[instruction_pointer + 3]] = left_hand * right_hand
            instruction_pointer += 4

        # input
        if opcode == 3:
            save_location = memory[instruction_pointer + 1]
            instruction_pointer += 2
            # fetch next element in iterator input
            memory[save_location] = next(input)

        # output
        if opcode == 4:
            output = memory[memory[instruction_pointer + 1]] if p1mode == 0 else memory[instruction_pointer + 1]
            instruction_pointer += 2
            # generate an intermediate result and halt
            yield output

        # jump if true
        # if 1st param is non-zero it sets instruction_pointer to the value of the 2nd param
        if opcode == 5:
            left_hand = memory[memory[instruction_pointer + 1]] if p1mode == 0 else memory[instruction_pointer + 1]
            right_hand = memory[memory[instruction_pointer + 2]] if p2mode == 0 else memory[instruction_pointer + 2]
            if left_hand != 0:
                instruction_pointer = right_hand
            else:
                instruction_pointer += 3

        # jump if false
        # if 1st param is zero it sets instruction_pointer to the value of the 2nd param
        if opcode == 6:
            left_hand = memory[memory[instruction_pointer + 1]] if p1mode == 0 else memory[instruction_pointer + 1]
            right_hand = memory[memory[instruction_pointer + 2]] if p2mode == 0 else memory[instruction_pointer + 2]
            if left_hand == 0:
                instruction_pointer = right_hand
            else:
                instruction_pointer += 3

        # jump if less
        # if 1st param is less then 2nd param it stores 1 in position of 3rd param, else 0
        if opcode == 7:
            left_hand = memory[memory[instruction_pointer + 1]] if p1mode == 0 else memory[instruction_pointer + 1]
            right_hand = memory[memory[instruction_pointer + 2]] if p2mode == 0 else memory[instruction_pointer + 2]
            if left_hand < right_hand:
                memory[memory[instruction_pointer + 3]] = 1
            else:
                memory[memory[instruction_pointer + 3]] = 0
            instruction_pointer += 4

        # equals
        # if 1st param is equal to the 2nd param it stores 1 in position of 3rd param, else 0
        if opcode == 8:
            left_hand = memory[memory[instruction_pointer + 1]] if p1mode == 0 else memory[instruction_pointer + 1]
            right_hand = memory[memory[instruction_pointer + 2]] if p2mode == 0 else memory[instruction_pointer + 2]
            if left_hand == right_hand:
                memory[memory[instruction_pointer + 3]] = 1
            else:
                memory[memory[instruction_pointer + 3]] = 0
            instruction_pointer += 4

        # go to next instruction

#compute(test_program, 5)

def amplification(memory):
    """Returns the max thruster signal we can find."""

    # Feedback loop using yield to take intermediate outputs into account
    # part 1:
    #perms = permutations([0,1,2,3,4])

    # part 2:
    perms = permutations([5,6,7,8,9])

    max_thrust = -1

    # walk through permutations
    # quick explanation: chain() is needed to deliver an iterator, which first exhausts the perm[x] (and 0) and then the one from the other compute()
    for perm in perms:
        def ampA():
            yield from compute(memory.copy(), chain(iter([perm[0], 0]), ampE()))
        def ampB():
            yield from compute(memory.copy(), chain(iter([perm[1]]), ampA()))
        def ampC():
            yield from compute(memory.copy(), chain(iter([perm[2]]), ampB()))
        def ampD():
            yield from compute(memory.copy(), chain(iter([perm[3]]), ampC()))
        def ampE():
            yield from compute(memory.copy(), chain(iter([perm[4]]), ampD()))

        print(f"perm: {perm}")
        # part 1
        # Try each permutation of amplifiers
        # for phase in perm:
        #     if carrybit == None:
        #         carrybit = compute(memory, 0, phase)
        #     else:
        #         carrybit = compute(memory, carrybit, phase)

        # part 2
        # feedback loop - terminal condition: a halt from any computer
        results = list(ampE())
        print(results)

        # memorize biggest thrust
        max_thrust = max(max_thrust, results[-1])

    return max_thrust

#print(amplification(test_amp_simple))

amplifiers = [3,8,1001,8,10,8,105,1,0,0,21,30,55,76,97,114,195,276,357,438,99999,3,9,102,3,9,9,4,9,99,3,9,1002,9,3,9,1001,9,5,9,1002,9,2,9,1001,9,2,9,102,2,9,9,4,9,99,3,9,1002,9,5,9,1001,9,2,9,102,5,9,9,1001,9,4,9,4,9,99,3,9,1001,9,4,9,102,5,9,9,101,4,9,9,1002,9,4,9,4,9,99,3,9,101,2,9,9,102,4,9,9,1001,9,5,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,99]
print(amplification(amplifiers))

# part 2
#test_amp_feedback = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
#print(amplification(test_amp_feedback))




# Tests:
#
# compares
#compute([3,9,8,9,10,9,4,9,99,-1,8], 8)
#compute([3,9,7,9,10,9,4,9,99,-1,8], 7)
#compute([3,3,1108,-1,8,3,4,3,99], 8)

# jumps
#compute([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 12345)
#compute([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 3)

# all-in-all test
#compute([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 8)

#print(compute(gravity_assist_dirty))
#print(compute(test_mul))



