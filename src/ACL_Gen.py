import argparse
import textfsm
import re

def parse_defines(defines_path, fsm_template_path):
    """Parses the given values from a define file and a FSM template file.
    
    Keyword Arguments:
    defines_path -- path to the defines file
    fsm_template_path -- path to the fsm template file
    """
    # load the FSM template
    with open(fsm_template_path) as tmpl:
        fsm = textfsm.TextFSM(tmpl)
    
    # read raw defines file and parse said file
    with open(defines_path) as fh:
        raw = fh.read()
    parsed = fsm.ParseText(raw)
    
    # build dict: { DefineName: [value1, value2, …] }
    variables = {}
    for name, value in parsed:
        variables.update({name:value})

    return variables

def load_template_lines(template_path):
    """Loads the given template as a list with each line as its own string.
    
    Keywords Arguments:
    template_path -- path to the template file
    """
    with open(template_path) as fh:
        # strips any newline characters from each line 
        return [line.rstrip('\n') for line in fh]

def generate_acl(variables, template):
    """Generates the ACL from the given variables and the template.
    
    Keyword Arguments:
    variables -- dict organized as { DefineName: [value1, value2, …] }
    template -- list of each line of a template file
    """
    var_pattern = re.compile(r"\{(\w+)\}")
    output = []

    for line in template:
        # try to get all variables for substitution in given line
        keys = var_pattern.findall(line)
        # if there’s nothing to substitute, add line to the output and move on
        if not keys:
            output.append(line)
            continue

        # start with the original line, then expand one key at a time
        lines_to_expand = [line]
        for key in keys:
            new_lines = []
            for l in lines_to_expand:
                # for each possible value of this key
                for val in variables.get(key, []):
                    # replace all occurrences of {key} in that intermediate line
                    new_lines.append(
                        re.sub(r"\{" + re.escape(key) + r"\}", val, l)
                    )
            lines_to_expand = new_lines

        # collect all the fully‐expanded lines
        output.extend(lines_to_expand)
    return "\n".join(output)
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a Dell ACL from a defines file + template using TextFSM"
    )
    parser.add_argument('defines', help='Path to variable definitions file')
    parser.add_argument('template', help='Path to ACL template file')
    parser.add_argument('fsm', help='Path to TextFSM template (define_parser.textfsm)')
    parser.add_argument('output', help='Path to write the generated ACL')
    args = parser.parse_args()

    values = parse_defines(args.defines, args.fsm)
    template = load_template_lines(args.template)
    acl_text = generate_acl(values, template)

    with open(args.output, 'w') as out_fh:
        out_fh.write(acl_text)