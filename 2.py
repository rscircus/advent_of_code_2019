# The task is to write a simple ALU/CPU here.

# It can take 3 instructions:
# 1: (1,v1,v2,v3): add v1 + v2 = v3
# 2: (2,v1,v2,v3): multiply v1 * v2 = v3
# 99: halt

# Tests:
#
# 1,0,0,0,99 becomes 2,0,0,0,99 (1 + 1 = 2).
# 2,3,0,3,99 becomes 2,3,0,6,99 (3 * 2 = 6).
# 2,4,4,5,99,0 becomes 2,4,4,5,99,9801 (99 * 99 = 9801).
# 1,1,1,4,99,5,6,0,99 becomes 30,1,1,4,2,5,6,0,99.

test_main = [1,1,1,4,99,5,6,0,99]
test_result = [30,1,1,4,2,5,6,0,99]

# Task program
gravity_assist_clear = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,9,1,19,1,19,5,23,1,23,6,27,2,9,27,31,1,5,31,35,1,35,10,39,1,39,10,43,2,43,9,47,1,6,47,51,2,51,6,55,1,5,55,59,2,59,10,63,1,9,63,67,1,9,67,71,2,71,6,75,1,5,75,79,1,5,79,83,1,9,83,87,2,87,10,91,2,10,91,95,1,95,9,99,2,99,9,103,2,10,103,107,2,9,107,111,1,111,5,115,1,115,2,119,1,119,6,0,99,2,0,14,0]

def compute(program):
    allowed = {1, 2, 99}
    cur_pos = 0

    # execute instructions
    while(program[cur_pos] in allowed and program[cur_pos] != 99):
        print("Cur position: " + str(program[cur_pos]))

        # add
        if program[cur_pos] == 1:
            program[program[cur_pos + 3]] = program[program[cur_pos + 1]] + program[program[cur_pos + 2]]

        # multiply
        if program[cur_pos] == 1:
            program[program[cur_pos + 3]] = program[program[cur_pos + 1]] * program[program[cur_pos + 2]]

        # go to next instruction
        cur_pos += 4

    return program

print(compute(test_main))



