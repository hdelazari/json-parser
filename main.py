import json
from enum import Enum

jason = '''
{ "name": "bob",
  "age": 27,
  "is_handsome": false,
  "hobbies": [ "eat", "pray", "love" ],
  "bank_acc": {
    "BB": 67360,
    "Nu": null 
  }
}
'''

out = json.loads(jason)

print(out)

class Symbols(Enum):
    OSB = '['
    CSB = ']'
    OCB = '{'
    CCB = '}'
    COLON = ':'
    COMMA = ','

def tokenize_string(a):
    #Doesn't account for escapes
    out = ''
    while True:
        c = next(a, None)
        if c is None:
            raise Exception("String not finished")
        if c == '"':
            return out
        out += c


def tokenize_number(c, a):
    #Only ints
    out = c
    while True:
        c = next(a, None)
        if c is None:
            break
        if c in "0123456789":
            out += c
        else:
            break
    return int(out), c

def tokenize_keyword(c,a):
    #What happens if 'truefully'
    out = c
    if out == 't':
        while out in 'true':
            c = next(a, None)
            if c is None:
                if out == 'true':
                    return True
                else:
                    raise Exception()
            out += c
            if out == 'true':
                return True
    if out == 'f':
        while out in 'false':
            c = next(a, None)
            if c is None:
                if out == 'false':
                    return False
                else:
                    raise Exception()
            out += c
            if out == 'false':
                return False
    if out == 'n':
        while out in 'null':
            c = next(a, None)
            if c is None:
                if out == 'null':
                    return None
                else:
                    raise Exception()
            out += c
            if out == 'null':
                return None
    raise Exception()


def tokenizer(file):
    out = []
    a = iter(file)
    while True:
        c = next(a, None)
        if c is None:
            break
        elif c in '{}[]:,':
            out.append(Symbols(c))
        elif c == '"':
            out.append(tokenize_string(a))
        elif c in "0123456789":
            token, last = tokenize_number(c,a)
            out.append(token)
            if last is not None and last in '}],':
                out.append(Symbols(last))
        elif c in 'tfn':
            out.append(tokenize_keyword(c,a))
    return out

print(tokenizer(jason))

def parse_member(t, a):
    if not isinstance(t, str):
        raise Exception(t)
    key = t
    t = next(a)
    if t is not Symbols.COLON:
        raise Exception(t)
    t = next(a)
    value = parse_value(t, a)
    return key, value

def parse_dict(a):
    out = {}
    t = next(a)
    while t is not Symbols.CCB:
        key, value = parse_member(t, a)
        out[key] = value
        t = next(a)
        if t is Symbols.COMMA:
            t = next(a)
        elif t is not Symbols.CCB:
            raise Exception(t)
    return out

def parse_list(a):
    out = []
    t = next(a)
    while t is not Symbols.CSB:
        value = parse_value(t, a)
        out.append(value)
        t = next(a)
        if t is Symbols.COMMA:
            t = next(a)
        elif t is not Symbols.CSB:
            raise Exception(t)
    return out

def parse_value(t, a):
    if not isinstance(t, Symbols):
        return t
    if t is Symbols.OCB:
        return parse_dict(a)
    if t is Symbols.CCB:
        raise Exception()
    if t is Symbols.OSB:
        return parse_list(a)
    if t is Symbols.CSB:
        raise Exception()
    if t is Symbols.COMMA:
        raise Exception()
    if t is Symbols.COLON:
        raise Exception()

def parser(tokens):
    a = iter(tokens)
    t = next(a)
    return parse_value(t, a)

print(json.loads(jason) == parser(tokenizer(jason)))
