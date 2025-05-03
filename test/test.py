from src.ACL_Gen import *
import unittest

# hardcode file locations
DEFINES_FILE = "test/inputs/test.def"
TEMPLATE_FILE = "test/inputs/test.template"
FSM_TEMPLATE_FILE = "test/inputs/defines.tmpl"
TEST_OUTPUT_FILE = "test/inputs/output.txt"

# make sure to run as a module, so first go to root directory and then use "python -m unittest test.test"
class ACLTest(unittest.TestCase):
    def test_parse_defines(self):
        output = parse_defines(DEFINES_FILE, FSM_TEMPLATE_FILE)
        self.assertEqual(output, {'var1': ['Value1', 'Value2'], 'var2': ['Value1', 'Value2']})
    
    def test_load_template(self):
        template = load_template_lines(TEMPLATE_FILE)
        self.assertEqual(template, ['input {var1} output {var2}', 'output {var2} input {var1}'])
    
    def test_generate_acl(self):
        values = parse_defines(DEFINES_FILE, FSM_TEMPLATE_FILE)
        template = load_template_lines(TEMPLATE_FILE)
        acl = generate_acl(values, template)
        with open(TEST_OUTPUT_FILE, 'r') as file:
            lines = file.readlines()
            test_file_content = ''.join(lines)
        self.assertEqual(acl, test_file_content)

if __name__ == "__main__":
    unittest.main()