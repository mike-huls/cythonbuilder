import re


# from cythonbuilder import logger


def read_write_pyx_to_pyi(target_pyx_path: str, target_pyi_path:str):
    """ Reads all content from a pyx file, convers and writes a pyi """

    # 1. Read pyx file
    pyx_lines: [str] = []
    with open(target_pyx_path, 'r') as open_pyx:
        pyx_lines.extend(open_pyx.readlines())

    # 2. Skip empty lines
    pyx_lines = [l.strip("\n") for l in pyx_lines]
    pyx_lines = [l for l in pyx_lines if (len(l) > 0)]

    # 2. Determine file indentation
    all_indentations = [__get_line_indentation_spacecount(line=l) for l in pyx_lines]
    all_indentations = [i for i in all_indentations if (i > 0)]
    spaces_for_one_tab = min(all_indentations)
    # Extra check: test wheter all are divisible by the space_for_one_tab
    for indent in all_indentations:
        if (indent % spaces_for_one_tab != 0):
            raise ValueError(f"Found invalid indentation: {indent} not divisible by {spaces_for_one_tab}")

    # Convert lines to py
    py_lines:[str] = []
    # todo only keep lines when the next line has a greater indentation
    for line_idx in range(len(pyx_lines)):
        if (line_idx == len(pyx_lines) - 1):
            print("breaking")
            break


        current_indentation = __get_line_indentation_spacecount(line=pyx_lines[line_idx])
        nextline_indentation = __get_line_indentation_spacecount(line=pyx_lines[line_idx + 1])
        if (nextline_indentation <= current_indentation):
            continue

        pyx_line = pyx_lines[line_idx]
        py_line = pyx_line_to_pyi(line=pyx_line.strip("\n"), spaces_for_one_tab=spaces_for_one_tab)
        if (py_line != None):
            py_lines.append(py_line)

    with open(target_pyi_path, 'w') as pyi_out:
        pyi_out.writelines([f"{line}\n" for line in py_lines])
        # for line in py_lines:
        #     print(line+'\n')
        #     pyi_out.write(line)

def __get_line_indentation_spacecount(line: str) -> int:
    """ How many spaces is the provided line indented? """
    spaces: int = 0
    if (len(line) > 0):
        if (line[0] == ' '):
            for letter_idx in range(len(line)):
                if (line[letter_idx + 1] != ' '):
                    spaces = letter_idx + 1
                    break
    return spaces

def pyx_line_to_pyi(line: str, spaces_for_one_tab: int):
    """ Interprets a line and converts pyx to pyi
        :arg spaces_for_one_tab       how many spaces equals one level of indentation
    """


    # 1. Calculate indentation level
    spacecount = __get_line_indentation_spacecount(line=line)
    indentation:int = int(spacecount / spaces_for_one_tab) if (spacecount > 0) else spacecount

    # 2. Remove unrequired characters
    line = line.strip(' ')

    # 3. Keep only lines that start with def, cpdef or cdef
    begin_words = ['def', 'cdef', 'cpdef']
    if not any([line[:len(w)] == w for w in begin_words]):
        return

    # take out classes
    if (line.split(" ")[1] == 'class'):
        line = " ".join(line.split(" ")[1:])

    # 4. Start replacing lines
    line_parts = line.split(" ")
    for word in ['cpdef', 'cdef']:
        if word in line_parts:
            word_idx = line_parts.index(word)
            line_parts[word_idx] = 'def'
    line = " ".join(line_parts)

    # line = line.replace("cpdef", "def")
    # line = line.replace("cdef", "def")

    # 5. Handle function types
    if (line[-1] == ":"):
        array_between_brakcets = re.findall('\(.*?\)',line)
        for brackets in array_between_brakcets:
            for argument in brackets.split(","):
                argument = argument.strip("()")
                arg_array = [a for a in argument.split(" ") if (len(a) > 0)]
                if (len(arg_array) <= 1):
                    continue
                var_ctype = arg_array[0]
                var_name = arg_array[1]
                py_type = convert_type_cy_to_py(cy_type=var_ctype)
                line = line.replace(argument, f'{var_name}:{py_type}')
        spaces = " " * spaces_for_one_tab * (indentation + 1)
        line = line + f"\n{spaces}..."
    return indentation * spaces_for_one_tab * ' ' + line

def convert_type_cy_to_py(cy_type:str):
    """ """
    # todo continue https://stackoverflow.com/questions/55451545/what-are-all-the-types-available-in-cython
    cy_type = cy_type.lower()

    if (cy_type in ['bint', 'bool']):
        return 'bool'
    elif (cy_type in ['char', 'short', 'int', 'long', 'long long']):
        return 'int'
    elif (cy_type in ['float', 'double', 'long double']):
        return 'float'
    elif (cy_type in ['float complex', 'double complex', 'complex']):
        return 'complex'
    elif (cy_type in ['char*', 'std::string', 'str']):
        return 'str'
    # print(f"{indentation * spaces_for_one_tab * ' '}{line}")