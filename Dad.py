# from pprint import pprint
import argparse

parser = argparse.ArgumentParser(description='Turns a a definition file and a template file into settings')
parser.add_argument('input1', metavar='input1', type=str, help='The definition file')
parser.add_argument('input2', metavar='input2', type=str, help='The template file')
parser.add_argument('output', metavar='output', type=str, help='The output file')
args = parser.parse_args()

# create a function that takes a file object and returns a list of lines
def filetolist(file):
    tempinput = open(file, "r")
    input = tempinput.readlines()
    input = [x.strip() for x in input]
    tempinput.close()
    return input

input1 = filetolist(args.input1)
input2 = filetolist(args.input2)

# create a dictionary of variables
variables = {}
state = 0
for x in input1:
    if x == "":
        state = 0
    elif state == 0:
        if x.startswith("define "):
            name = x.split("define ")[1]
            state = 1
            variables[name] = []
    elif state == 1:
        variables[name].append(x)

# go through every line in input2 that has a bracket in it. Then go through every variable and see if it is in the line. If it is, print line with the variable replacing the bracketed text
output = []
for x in input2:
    tempoutput = []
    if "{" in x and "}" in x:
        for y in variables:
            for z in variables[y]:
                if y in x:
                    # print(x.replace("{" + y + "}", z))
                    tempoutput.append(x.replace("{" + y + "}", z))
    else:
        output.append(x)
    
    if tempoutput != []:
        for y in tempoutput:
            if "{" in y and "}" in y:
                for z in variables:
                    for a in variables[z]:
                        if z in y:
                            if y.replace("{" + z + "}", a) not in output:
                                output.append(y.replace("{" + z + "}", a))
            else:
                output.append(y)

# turn output into a string
output = "\n".join(output)

# write output to file
fileoutput = open(args.output, "w")
fileoutput.write(output)
fileoutput.close()