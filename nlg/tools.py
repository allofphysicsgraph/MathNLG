import json
import difflib

from colorama import Back, Style

def colordiff(str1, str2) :
    seqm = difflib.SequenceMatcher(None, str1, str2)
    output1 = ''
    output2 = ''
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output1 += Back.GREEN + str(seqm.a[a0:a1]) + Style.RESET_ALL
            output2 += Back.GREEN + str(seqm.a[a0:a1]) + Style.RESET_ALL
        elif opcode == 'insert':
            output2 += Back.YELLOW + str(seqm.b[b0:b1]) + Style.RESET_ALL
        elif opcode == 'delete':
            output1 += Back.YELLOW + str(seqm.a[a0:a1]) + Style.RESET_ALL
        elif opcode == 'replace':
            output1 += Back.RED + str(seqm.a[a0:a1]) + Style.RESET_ALL
            output2 += Back.RED + str(seqm.b[b0:b1]) + Style.RESET_ALL
        else:
            raise RuntimeError("unexpected opcode")
    return output1, output2

def diffFormat(label1, label2, str1, str2) :
    d1, d2 = colordiff(str1, str2)
    return '\n\n%s:\n\n%s\n\n%s:\n\n%s\n' % (label1, d1, label2, d2)

def skipTest(test) :
    if 'disabled' in test.keys() :
        return test['disabled']

def assertEqual(self, output, expected) :
    self.assertEqual(output, expected, diffFormat('output', 'expected', output, expected))

def parse(text) :
    try:
        return json.loads(text)
    except ValueError as e:
        raise ValueError('invalid json: %s' % (e))

def load(file) :
    data = {}
    with open(file, 'r') as file :
        raw = file.read()
        data = parse(raw)
    return data
