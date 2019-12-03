import re
import sys
from entities import *


class State(enum.Enum):
    OUT_OF_PHP = 1
    IN_FUNCTION = 2
    IN_CLASS = 3
    IN_TRAIT = 4
    IN_INTERFACE = 5
    IN_DOCBLOCK = 6
    IN_GLOBAL = 7


def parse(filename):
    root_namespace = Namespace("\\", filename=filename)
    cur_token = root_namespace
    print(root_namespace)
    print(cur_token)
    state = State.OUT_OF_PHP
    prev_state = state
    braces_diff = 0
    is_first_level_docblock = True
    is_prev_docblock = False
    docblock = []
    line_num = 0
    file = []
    f = open(filename, "r", encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        line = re.sub(' +', ' ', line)
        line = line.strip()
        if line:
            file.append(line)
    for line in file:
        line_num += 1
        if state == State.OUT_OF_PHP:
            if line.find("<?php") == 0:
                prev_state = state
                state = State.IN_GLOBAL
            else:
                sys.exit(-1)
        elif state == State.IN_GLOBAL:
            if line == "?>":  # end of namespace
                state = State.OUT_OF_PHP
            elif line == "/**":
                prev_state = state
                state = State.IN_DOCBLOCK
            elif re.search(r'namespace [a-zA-Z_][a-zA-Z0-9.]*', line):
                is_first_level_docblock = False
                cur_token = root_namespace.add_namespace(line)
            elif re.search(r'function\s[a-zA-Z_][\w0-9_]*', line):
                is_first_level_docblock = False
                # cur_function = parser_function(line)
                # cur_namespace.add_function(cur_function)
                cur_token = cur_token.add_tokens(line, token_type=Type.FUNCTION)
                braces_diff = len(re.findall(r'{', line))
                if is_prev_docblock:
                    set_docblock(cur_token)
                    is_prev_docblock = False
                prev_state = state
                state = State.IN_FUNCTION
            elif re.search( r'[$]GLOBALS\[\'[a-zA-Z_][\w]*\'\]', line):
                is_first_level_docblock = False
                root_namespace.add_tokens(line)
            elif re.search(r'[$][a-zA-Z_][\w]*', line):
                is_first_level_docblock = False
                cur_token.add_tokens(line)
            elif re.search(r'define\(.*\)', line):
                is_first_level_docblock = False
                cur_token.add_tokens(line)
            elif re.search(r'const\s[a-zA-Z0-9_][\w]*', line):
                is_first_level_docblock = False
                cur_token.add_tokens(line)
            elif re.search(r"class [a-zA-Z_][a-zA-Z0-9_]*", line):
                is_first_level_docblock = False
                # cur_class = parser_class(line)
                # cur_namespace.add_class(cur_class)
                cur_token = cur_token.add_tokens(line, token_type=Type.CLASS)
                braces_diff = len(re.findall(r'{', line))
                if is_prev_docblock:
                    set_docblock(cur_token)
                    is_prev_docblock = False
                state = State.IN_CLASS
            elif re.search( r'interface [a-zA-Z_][a-zA-Z0-9_]*', line):
                is_first_level_docblock = False
                # cur_interface = parser_interface(line)
                # cur_namespace.add_interface(cur_interface)
                cur_token = cur_token.add_tokens(line, token_type=Type.INTERFACE)
                braces_diff = len(re.findall(r'{', line))
                if is_prev_docblock:
                    set_docblock(cur_token)
                    is_prev_docblock = False
                state = State.IN_INTERFACE
            elif re.search(r'trait\s[a-zA-Z0-9_][\w]*', line):
                is_first_level_docblock = False
                # cur_trait = parser_trait(line)
                # cur_namespace.add_trait(cur_trait)
                cur_token = cur_token.add_tokens(line, token_type=Type.TRAIT)
                braces_diff = len(re.findall(r'{', line))
                if is_prev_docblock:
                    set_docblock(cur_token)
                    is_prev_docblock = False
                state = State.IN_TRAIT
        elif state == State.IN_DOCBLOCK:
            if line == "*/":
                if is_first_level_docblock and prev_state == State.IN_GLOBAL and is_prev_docblock:
                    root_namespace.root_docblock = root_namespace.next_docblock
                    root_namespace.next_docblock = ""
                    is_first_level_docblock = False
                state = prev_state
                cur_token.next_docblock = docblock
                docblock = []
                is_prev_docblock = True
            else:
                docblock.append(line)
        elif state == state.IN_FUNCTION:
            if line[0] == '{':
                braces_diff += 1
            elif line[0] == '}':
                braces_diff -= 1
            else:
                pass
            if braces_diff == 0:
                state = prev_state
                cur_token = cur_token.parent_token
            else:
                if re.search(r'[$]GLOBALS\[\'[a-zA-Z_][\w]*\'\]', line):
                    root_namespace.add_tokens(line)
        elif state == state.IN_CLASS:
            if line[0] == '}':
                state = State.IN_GLOBAL
                cur_token = cur_token.parent_token
                is_prev_docblock = False
            elif line == "/**":
                prev_state = state
                state = State.IN_DOCBLOCK
            elif re.match('((public\s)|(protected\s)|(private\s))?(static\s)?[$][a-zA-Z_][\w0-9]*', line):
                cur_token.add_tokens(line)
                if is_prev_docblock:
                    set_docblock(cur_token)
                    is_prev_docblock = False
            elif re.match('((public\s)|(protected\s)|(private\s))?const\s[a-zA-Z_][\w0-9_]*', line):
                cur_token.add_tokens(line)
                if is_prev_docblock:
                    set_docblock(cur_token)
                    is_prev_docblock = False
            elif re.match('((public\s)|(protected\s)|(private\s))?(static\s)?function\s[a-zA-Z_][\w0-9_]*', line):
                if is_prev_docblock:
                    set_docblock(cur_token)
                    is_prev_docblock = False
                prev_state = state
                state = state.IN_FUNCTION
                cur_token = cur_token.add_tokens(line, token_type=Type.FUNCTION)
                braces_diff = len(re.findall(r'{', line))
        elif state == state.IN_INTERFACE:
            if line[0] == '}':
                state = state.IN_GLOBAL
                is_prev_docblock = False
                cur_token = cur_token.parent_token
            elif line == "/**":
                prev_state = state
                state = State.IN_DOCBLOCK
            elif re.match('((public\s)|(protected\s)|(private\s))?const\s[a-zA-Z_][\w0-9_]*', line):
                cur_token.add_tokens(line)
                if is_prev_docblock:
                    set_docblock(cur_token)
                    is_prev_docblock = False
            elif re.match('((public\s)|(protected\s)|(private\s))?(static\s)?function\s[a-zA-Z_][\w0-9_]*', line):
                if is_prev_docblock:
                    set_docblock(cur_token)
                    is_prev_docblock = False
                prev_state = state
                state = state.IN_FUNCTION
                cur_token = cur_token.add_tokens(line, token_type=Type.FUNCTION)
                braces_diff = len(re.findall(r'{', line))
        elif state == state.IN_TRAIT:
            if line[0] == '}':
                state = state.IN_GLOBAL
                is_prev_docblock = False
                cur_token = cur_token.parent_token
            elif line == "/**":
                prev_state = state
                state = State.IN_DOCBLOCK
            elif re.match('((public\s)|(protected\s)|(private\s))?(static\s)?[$][a-zA-Z_][\w0-9_]*', line):
                cur_token.add_tokens(line)
                if is_prev_docblock:
                    set_docblock(cur_token)
                    is_prev_docblock = False
            elif re.match('((public\s)|(protected\s)|(private\s))?(static\s)?function\s[a-zA-Z_][\w0-9_]*', line):
                if is_prev_docblock:
                    set_docblock(cur_token)
                    is_prev_docblock = False
                prev_state = state
                state = state.IN_FUNCTION
                cur_token = cur_token.add_tokens(line, token_type=Type.FUNCTION)
                braces_diff = len(re.findall(r'{', line))

    print(root_namespace)
    return root_namespace


def set_docblock(cur_token):
    cur_token.docblock = cur_token.parent_token.next_docblock
    cur_token.parent_token.next_docblock = ""

