import re


# Check if current line has a tag
def is_tag_line(line):
    return re.match('@[a-z]+', line)


def is_namespace_line(line):
    return re.match('(<\?php\s)?namespace\s([a-zA-Z]+[\\\\]?)+', line)


def is_var_line(line):
    return re.match('[$][a-zA-Z_][\w]*', line)


def is_global_var_line(line):
    return re.match('[$]GLOBALS\[\'[a-zA-Z_][\w]*\'\]', line)


def is_define_line(line):
    return re.match('define\(.*\)', line)


def is_const_line(line):
    return re.match('const\s[a-zA-Z_][\w]*', line)


def is_function_line(line):
    return re.match('function\s[a-zA-Z_][\w]*\(.*\)', line)


def is_class_line(line):
    return re.match('class\s[a-zA-Z_][\w]*', line)


def is_interface_line(line):
    return re.match('interface\s[a-zA-Z_][\w]*', line)


def is_trait_line(line):
    return re.match('trait\s[a-zA-Z_][\w]*', line)


def is_property_var_line(line):
    return re.match('((public\s)|(protected\s)|(private\s))?(static\s)?[$][a-zA-Z_][\w]*', line)


def is_property_const_line(line):
    return re.match('((public\s)|(protected\s)|(private\s))?const\s[a-zA-Z_][\w]*', line)


def is_method_line(line):
    return re.match('((public\s)|(protected\s)|(private\s))?(static\s)?function\s[a-zA-Z_][\w]*', line)