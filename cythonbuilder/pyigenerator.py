import re
from dataclasses import dataclass

from cythonbuilder.services import logger

class LineConverter:

    in_class_body:bool=False
    in_func_body:bool=False

    def __init__(self, line:str, file_spaces_for_one_tab:int=4):
        self.pyx_line = line
        self.file_spaces_for_one_tab = file_spaces_for_one_tab

    # Indentation
    @property
    def indent_spacecount(self) -> int:
        """ How many spaces is the provided line indented? """
        spaces: int = 0
        if (len(self.pyx_line) > 0):
            if (self.pyx_line[0] == ' '):
                for letter_idx in range(len(self.pyx_line)):
                    if (self.pyx_line[letter_idx + 1] != ' '):
                        spaces = letter_idx + 1
                        break
        return spaces
    @property
    def indent_tabs(self) -> int:
        """ How many spaces is the provided line indented? """
        spaces = get_line_indentation_spacecount(line=self.pyx_line)
        return int(spaces / self.file_spaces_for_one_tab)

    # Definitions
    @property
    def is_import(self) -> bool:
        """ """
        line = self.pyx_line.strip()
        word_array = line.split(" ")
        first_word_is_import = word_array[0] in ['import', 'cimport']
        line_contains_from_import = word_array[0] == 'from' and 'import' in word_array
        return any([first_word_is_import, line_contains_from_import])
    @property
    def is_class_def(self) -> bool:
        """ """
        return self.pyx_line[-1] == ":" and "class " in self.pyx_line
    @property
    def is_func_def(self) -> bool:
        """ Is C or PY function """
        line = self.pyx_line.strip(' ')
        word_array = line.split()
        endswith_colon = line[-1] == ':'
        contains_def = len(set(word_array).intersection({'cdef', 'def', 'cpdef'})) > 0
        is_no_class = not self.is_class_def
        return all([endswith_colon, contains_def, is_no_class])
    @property
    def is_c_func_def(self) -> bool:
        """ Is function but also a C function """
        is_c_function = False
        if (self.is_func_def):
            line_parts_set = set(self.pyx_line.split(" "))
            cfunction_defs = {'cpdef', 'cdef'}
            if (len(line_parts_set.intersection(cfunction_defs)) > 0):
                is_c_function = True
        return is_c_function
    @property
    def is_property(self) -> bool:
        line = self.pyx_line.strip()
        is_property = line[0] == '@'
        is_not_cython_property = '@cython.' not in line
        return all([is_property, is_not_cython_property])
    @property
    def is_define_line(self) -> bool:
        """ This line is not an import, function, property or class def"""
        return any([self.is_import, self.is_class_def, self.is_func_def, self.is_property])

    # translate
    @property
    def py_line(self) -> str:

        # Strip and remove double spaces
        py_line = self.pyx_line.strip()
        py_line = " ".join(py_line.split("  "))
        if (self.is_import):
            py_line = py_line.replace("cimport", "import")
        if (self.is_class_def):
            py_line = " ".join([w for w in py_line.split(" ") if (w not in ['cdef', 'cpdef'])])
        if (self.is_func_def):

            # replace definition
            py_line = py_line.replace('cdef', 'def')
            py_line = py_line.replace('cpdef', 'def')

            # Handle return function types
            py_return_type = None
            if ('->' in py_line):
                py_return_type = py_line.split('->')[1].strip().replace(":", "")
                py_line = f"{py_line.split('->')[0].strip()}:"

            array_between_brackets = re.findall('\(.*?\)', py_line)
            logger.error(py_line)
            for brackets in array_between_brackets:
                # Replace C return type to -> returntype
                func_part_one_old = py_line.replace(f"{brackets}:", "")
                func_sig_parts = func_part_one_old.split(" ")

                if (len(func_sig_parts) == 3):
                    py_return_type = self.convert_type_cy_to_py(cy_type=func_sig_parts[1])
                func_part_one_new = " ".join([func_sig_parts[0], func_sig_parts[-1]])
                py_line = py_line.replace(func_part_one_old, func_part_one_new)
                for argument in brackets.split(","):

                    # Strip away parentheses and spaces
                    argument = argument.strip("() ")
                    logger.debug(f"{argument=}")


                    # Rework arguments of c-function to py-style
                    if (self.is_c_func_def):
                        # C types are like (int age)
                        arg_name_py:str = None
                        arg_type_py:str = None
                        arg_default_value_py:str = None
                        # take out arg name and type if they are so specified
                        if (' ' in argument):
                            arg_name_py = argument.split(' ')[1]
                            arg_type_py = self.convert_type_cy_to_py(argument.split(' ')[0])
                        else:
                            arg_name_py = argument

                        # Get default value
                        if ('=' in argument):
                            arg_default_value_py = argument.split("=")[1].strip()

                        # make sure default value is not part of name
                        if (arg_name_py != None and "=" in arg_name_py):
                            arg_name_py = arg_name_py.split("=")[0]
                        arg_type_py = f":{arg_type_py}" if (arg_type_py != None) else ''
                        arg_default_value_py = f"={arg_default_value_py}" if (arg_default_value_py != None) else ''
                        newArg = f"{arg_name_py}{arg_type_py}{arg_default_value_py}"
                        py_line = py_line.replace(argument, newArg)
            # Add python return type
            if (py_return_type != None):
                py_line = py_line.strip(":") + f' -> {py_return_type}:'

            # Add ... to function content
            py_line = py_line + f"\n{self.file_spaces_for_one_tab * (self.indent_tabs + 1) * ' '}..."
        # return indentation * spaces_for_one_tab * ' ' + line

        # add original indentation back
        py_line = f"{self.file_spaces_for_one_tab * self.indent_tabs * ' '}" + py_line

        return py_line


    def convert_type_cy_to_py(self, cy_type:str):
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
        elif (cy_type in ['void']):
            return 'None'
        else:
            # non-built-in type like np.ndarray
            return cy_type




def read_write_pyx_to_pyi(target_pyx_path: str, target_pyi_path:str):
    """ Reads all content from a pyx file, convers and writes a pyi """

    # 1. Read pyx file
    pyx_lines: [str] = []
    with open(target_pyx_path, 'r') as open_pyx:
        pyx_lines.extend(open_pyx.readlines())

    # 2. Strip away any content after a #
    pyx_lines = list(map(lambda l: l.split("#")[0].rstrip() if "#" in l else l, pyx_lines))

    # 3. Skip empty lines
    pyx_lines = [l.strip("\n") for l in pyx_lines]
    pyx_lines = [l for l in pyx_lines if (len(l) > 0)]

    # 4. Determine file indentation
    all_indentations = [get_line_indentation_spacecount(line=l) for l in pyx_lines]
    all_indentations = [i for i in all_indentations if (i > 0)]
    spaces_for_one_tab = min(all_indentations)
    # Extra check: test wheter all are divisible by the space_for_one_tab
    for indent in all_indentations:
        if (indent % spaces_for_one_tab != 0):
            raise ValueError(f"Found invalid indentation: {indent} not divisible by {spaces_for_one_tab}")


    # 5. Convert lines to py
    py_lines:[str] = []
    prev_line:LineConverter = None
    for line_idx in range(len(pyx_lines)):
        pyxline = pyx_lines[line_idx]

        ld = LineConverter(line=pyxline, file_spaces_for_one_tab=spaces_for_one_tab)

        if (prev_line != None):
            # Classes
            if (prev_line.is_class_def):
                ld.in_class_body = True
            elif (prev_line.in_class_body and not ld.is_class_def):
                ld.in_class_body = True

            # Functions
            if (prev_line.is_func_def):
                ld.in_func_body = True
            elif (prev_line.in_func_body and (not ld.is_class_def and not ld.is_func_def)):
                ld.in_func_body = True

            # if current line defines anything
            if (ld.is_define_line):
                ld.in_func_body = False
                ld.in_class_body = False

            # kep define lines an any lines that are in a class_body
            if (not ld.in_class_body and not ld.is_define_line):
                # logger.error(msg=f"{prev_line.indent_tabs},{ld.indent_tabs} - {l_is_class}{l_is_func}-{'C' if ld.in_class_body else 'X'}{'F' if ld.in_func_body else 'X'}, {ld.is_property} {pyxline}")
                continue
            # else:
            # logger.debug(msg=f"{prev_line.indent_tabs},{ld.indent_tabs} - {l_is_class}{l_is_func}-{'C' if ld.in_class_body else 'X'}{'F' if ld.in_func_body else 'X'}, {ld.is_property} {pyxline}")

            # logger.warning(msg=f"{ld.pyx_line}")
            # logger.debug(msg=f"{ld.py_line}")


        prev_line = ld
        py_lines.append(ld.py_line)

    # 6. Save
    with open(target_pyi_path, 'w') as pyi_out:
        pyi_out.writelines([f"{line}\n" for line in py_lines])
        # for line in py_lines:
        #     print(line+'\n')
        #     pyi_out.write(line)





def get_line_indentation_spacecount(line: str) -> int:
    """ How many spaces is the provided line indented? """
    spaces: int = 0
    if (len(line) > 0):
        if (line[0] == ' '):
            for letter_idx in range(len(line)):
                if (line[letter_idx + 1] != ' '):
                    spaces = letter_idx + 1
                    break
    return spaces
def get_line_indentation(line: str, file_spaces_for_one_tab:int) -> int:
    """ How many spaces is the provided line indented? """
    spaces = get_line_indentation_spacecount(line=line)
    return int(spaces / file_spaces_for_one_tab)