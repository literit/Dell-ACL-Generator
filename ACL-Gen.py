# from pprint import pprint
import argparse

parser = argparse.ArgumentParser(description='Turns a a definition file and a template file into settings')
parser.add_argument('defines', metavar='defines', type=str, help='The definition file')
parser.add_argument('template', metavar='template', type=str, help='The template file')
parser.add_argument('output', metavar='output', type=str, help='The output file')
args = parser.parse_args()

# create a function that takes a file object and returns a list of lines
def filetolist(file):
    tempinput = open(file, "r")
    input = tempinput.readlines()
    input = [x.strip() for x in input]
    tempinput.close()
    return input

def varlist(input):
    variables = {}
    state = 0
    for x in input:
        if x == "":
            state = 0
        elif state == 0:
            if x.startswith("define "):
                name = x.split("define ")[1]
                state = 1
                variables[name] = []
            elif x.startswith("Define "):
                name = x.split("Define ")[1]
                state = 1
                variables[name] = []
        elif state == 1:
            variables[name].append(x)
    return variables

# go through every line in template that has a bracket in it. Then go through every variable and see if it is in the line. If it is, print line with the variable replacing the bracketed text
def createoutput(variables, template):
    output = []
    for x in template:
        tempoutput = []
        if "{" in x and "}" in x:
            for y in variables:
                for z in variables[y]:
                    if y in x:
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
    return output

def outputfile(output, file):
    fileoutput = open(file, "w")
    fileoutput.write(output)
    fileoutput.close()

if __name__ == "__main__":
    defines = filetolist(args.defines)
    template = filetolist(args.template)
    variables = varlist(defines)
    output = createoutput(variables, template)
    outputfile(output, args.output)
