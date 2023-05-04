import io
import typing
import unittest

from cythonbuilder import pyigenerator
from cythonbuilder.pyigenerator import LineConverter


# from config import app_config

def load_io_text(lines:str) -> typing.TextIO:
    """ Loads a string into a TextIO object """
    text_io = io.StringIO()  # Create a TextIO object with an empty string buffer
    text_io.write(lines)
    text_io.seek(0)  # Move the file pointer to the beginning of the
    return text_io


class TestPyiGenerator(unittest.TestCase):

    def setUp(self) -> None:
        # app_config.load_env()
        pass

    def test_line_indentation(self):
        self.assertEqual(pyigenerator.get_line_indentation_spacecount(line="  def test():"), 2)
        self.assertEqual(pyigenerator.get_line_indentation_spacecount(line="    a = 'hello'"), 4)
    def test_get_line_indentation_spacecount(self):
        pyd_line = """    test:str"""
        lc:LineConverter = LineConverter(line=pyd_line)
        self.assertEqual(4, lc.indent_spacecount)

    def test_doublecheck_indentation_spacecount(self):
        pyd_line = """
    good_indentation:str
     bad_indentation:str"""
        with self.assertRaises(Exception):
            res = pyigenerator.pyx_to_pyi(open_pyx=load_io_text(lines=pyd_line))

    def test_can_convert_cimport_to_import(self):
        # 1. Converts regular function: c-type arg types. return type
        pyd_import_lines = """
cimport pandas
import normal_thing
# some other things
    """
        pyi_lines:[str] = pyigenerator.pyx_to_pyi(open_pyx=load_io_text(lines=pyd_import_lines))
        expeced_pyi_lines:[str] = ['import pandas\n', 'import normal_thing\n']
        self.assertTrue(expeced_pyi_lines, pyi_lines)
        self.assertTrue("#" not in "".join(pyi_lines))

    def test_can_convert_class(self):
        # 1. Converts cython class with methods
        pyd_class_regular = """
cdef class MyClass(object):
    test:str
    cdef test_def(self, int num) -> int:
        return num * num

    cpdef test_cdef(self, long num) -> float:
        return num * num

    def test_cpdef(self, long num) -> float:
        return num * num
    """
        res: [str] = pyigenerator.pyx_to_pyi(open_pyx=load_io_text(lines=pyd_class_regular))
        expected: [str] = ['class MyClass(object):\n', '    test:str\n', '    def test_def(self, num:int) -> int:\n        ...\n',
                           '    def test_def(self, num:int) -> float:\n        ...\n', '    def test_def(self, long num) -> float:\n        ...\n']
        self.assertEqual(expected, res)

        # 2. Converts Python class with methods
        pyd_class_regular = """
class MyClass(object):
    test:str
    def test_def(self, num:int) -> int:
        return num * num

    def test_nohint(self, num):
        return num * num
    """
        res: [str] = pyigenerator.pyx_to_pyi(open_pyx=load_io_text(lines=pyd_class_regular))
        expected: [str] = ['class MyClass(object):\n', '    test:str\n', '    def test_def(self, num:int) -> int:\n        ...\n', '    def test_nohint(self, num):\n        ...\n']
        self.assertEqual(expected, res)

    def test_converts_types(self):
        pyd_function_regular = """
cpdef void c_types(bint a_bool, double a_float, complex a_comples, char* a_str):
    pass
        """
        pyi_lines: [str] = pyigenerator.pyx_to_pyi(open_pyx=load_io_text(lines=pyd_function_regular))
        expected_pyi_lines: [str] = ['def c_types(a_bool:bool, a_float:float, a_comples:complex, a_str:str) -> None:\n    ...\n']
        self.assertTrue(expected_pyi_lines, pyi_lines)

    def test_converts_funcs_with_default_args(self):
        pyd_function_regular = """
cpdef void c_types(double a_float=0.0):
    pass
        """
        pyi_lines: [str] = pyigenerator.pyx_to_pyi(open_pyx=load_io_text(lines=pyd_function_regular))
        print(pyi_lines)
        expected_pyi_lines: [str] = ['def c_types(a_float:float=0.0) -> None:\n    ...\n']
        self.assertTrue(expected_pyi_lines, pyi_lines)

    def test_converts_func_in_func(self):
        pyd_function_regular = """
cpdef void xxx(double a_float=0.0):
    cdef void xxz(double b_float):
        return double * 2
    return test(double) * test(double)

cpdef void yyy(double a_float=0.0):
    return double * 2
        """
        pyi_lines: [str] = pyigenerator.pyx_to_pyi(open_pyx=load_io_text(lines=pyd_function_regular))
        expected_pyi_lines: [str] = ['def xxx(a_float:float=0.0) -> None:\n    ...\n', '    def xxz(b_float:float) -> None:\n        ...\n', 'def yyy(a_float:float=0.0) -> None:\n    ...\n']
        self.assertTrue(expected_pyi_lines, pyi_lines)

    def test_can_convert_function(self):
        # 1. Converts regular function: c-type arg types. return type
        pyd_function_regular = """
cpdef int c_types(int: limit, float: height):
    # Count primes - Added Cython types and compiler directives
    pass
        """
        res = pyigenerator.pyx_to_pyi(open_pyx=load_io_text(lines=pyd_function_regular))
        self.assertTrue("def c_types(limit:int:, height:float:) -> int:\n" in "".join(res))
        self.assertTrue("    ..." in "".join(res))


        # 2. Converts regular function py-type arg types and return type
        pyd_function_no_arg_type = """
def no_arg_type(argument, age:int) -> int:
    print(f'my age is {age}')
    return age * 2
        """
        res = pyigenerator.pyx_to_pyi(open_pyx=load_io_text(lines=pyd_function_no_arg_type))
        self.assertTrue("def no_arg_type(argument, age:int) -> int:\n    ...\n" in "".join(res))
        self.assertTrue("    ..." in "".join(res))

        def test_can_convert_enum(self):
            # 1. Converts regular function: c-type arg types. return type
            pyd_function_regular = """
    cpdef enum PluginType:
        RED='RED'
        BLUE='BLUE'
        GREEN='GREEN'
"""
            res = pyigenerator.pyx_to_pyi(open_pyx=load_io_text(lines=pyd_function_regular))
            expected: [str] = ['from enum import Enum\n\n', 'class PluginType(Enum):\n', "        RED='RED'\n", "        BLUE='BLUE'\n", "        GREEN='GREEN'\n"]
            self.assertEqual(expected, res)
            self.assertTrue("RED" in "".join(res))

    def test_doesnt_convert_name_main(self):
        # 1. Converts regular function: c-type arg types. return type
        pyd_function_regular = """
cpdef enum PluginType:
    RED='RED'
    BLUE='BLUE'
    GREEN='GREEN'

if __name__ == "__main__":
    print("ok")
"""
        res = pyigenerator.pyx_to_pyi(open_pyx=load_io_text(lines=pyd_function_regular))
        expected:[str] = ['from enum import Enum\n\n', 'class PluginType(Enum):\n', "        RED='RED'\n", "        BLUE='BLUE'\n", "        GREEN='GREEN'\n", '       \n']
        self.assertEqual(expected, res)
        self.assertTrue("RED" in "".join(res))
        self.assertTrue("main" not in "".join(res))
        self.assertTrue("name" not in "".join(res))


#         # 2. Converts regular function py-type arg types and return type
#         pyd_function_no_arg_type = """
# cpdef enum PluginType:
#     print(f'my age is {age}')
#     return age * 2
#         """
#         res = pyigenerator.pyx_to_pyi(open_pyx=load_io_text(lines=pyd_function_no_arg_type))
#         self.assertTrue("def no_arg_type(argument, age:int) -> int:\n    ...\n" in "".join(res))
#         self.assertTrue("    ..." in "".join(res))

if __name__ == '__main__':
    unittest.main()
