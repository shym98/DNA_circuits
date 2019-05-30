strands = ['TCTGAC', 'AGACTG', 'GCTATT', 'CGATAA', 'GTAACA', 'CATTGT', 'GACTTA', 'CTGAAT']
nand_operator_strand = 'GCTATTGACTTAGCTATTGTAACATCTGACGACTTAAGACTGCATTGT'


def create_input_strand(first_input_val, second_input_val):
    if not first_input_val and not second_input_val:
        return strands[3] + strands[7]
    elif not first_input_val and second_input_val:
        return strands[3] + strands[5]
    elif first_input_val and not second_input_val:
        return strands[1] + strands[7]
    else:
        return strands[1] + strands[5]


def complement_strand(strand):
    output = ''
    for i in range(len(strand)):
        if strand[i] == 'A':
            output += 'T'
        elif strand[i] == 'T':
            output += 'A'
        elif strand[i] == 'C':
            output += 'G'
        else:
            output += 'C'
    return output


def hybridization(operator_strand, input_strand):
    return (True, False)[operator_strand.find(complement_strand(input_strand)) == -1]


def generate_output(first_input, second_input):
    input_strand = create_input_strand(first_input, second_input)
    return hybridization(nand_operator_strand, input_strand)


print(create_input_strand(0, 0))
print(create_input_strand(0, 1))
print(create_input_strand(1, 0))
print(create_input_strand(1, 1))
