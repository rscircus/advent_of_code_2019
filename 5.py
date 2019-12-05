# The task today is to extend the Intcode computer from day 2, let's copy it over
#
# The task is to write a simple ALU/CPU here.

# It can take 3 instructions:
# 1: (1,v1,v2,v3): add v1 + v2 = v3
# 2: (2,v1,v2,v3): multiply v1 * v2 = v3
# 99:(99): halt
#
# # New from day 5
#
# 3: (3,v1): saves some kind of input and stores it to address v1
# 4: (4,v1): outputs the value at address v1
# -further we need some kind of input routine
#
# Then we need to implement `parameter modes`
# - parameter mode 0: parameters are interpreted as position
# - parameter mode 1: parameter is interpreted as value
#
# 0 is called position mode
# 1 is called immediate mode
# Further requirements:
# - Parameters that an instruction writes to will never be in immediate mode.

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

def compute(memory, input=1):
    """My small tiny sweet little computer."""

    instruction_pointer = 0

    # execute instructions
    while(memory[instruction_pointer] != 99):

        opcode, p1mode, p2mode, p3mode = explode(memory, instruction_pointer)
        print(f"IP: {instruction_pointer} \t instruction: {memory[instruction_pointer]} \t opcode: {opcode}")

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
            memory[save_location] = input
            instruction_pointer += 2

        # output
        if opcode == 4:
            print_output = memory[memory[instruction_pointer + 1]] if p1mode == 0 else memory[instruction_pointer + 1]
            print(f"Output: {print_output} in mode: {p1mode}")
            instruction_pointer += 2

        # go to next instruction

compute(test_program)


# Tests:
#print(compute(gravity_assist_dirty))
#print(compute(test_mul))



