import datetime
import glob
import os
import shutil
import unittest

import cythonbuilder
import cythonbuilder as cybuilder
from dataclasses import dataclass

# def do():
#     cybuilder.init()
#     cybuilder.build(targetfilenames=["gigya"], debugmode=False)
#
#     from ext import gigya
#
#     gigya.vld_gigya_types('test')




@dataclass
class AppConfig:
    appname:str = "CythonBuilder"
    appcmd:str = os.path.splitext(os.path.basename(__file__))[0]

@dataclass
class LoggingConfig:
    logginName:str = 'cybuilderlogger'

@dataclass
class DirectoryConfig:
    dirname_extensions:str = "ext"
    dirname_pyxfiles:str = "pyxfiles"
    dirname_annotations:str = "annotations"

    path_root_dir:str = os.path.realpath(os.curdir)
    path_extensions_dir:str = os.path.join(path_root_dir, dirname_extensions)
    path_pyx_dir:str = os.path.join(path_extensions_dir, dirname_pyxfiles)
    path_annotations_dir:str = os.path.join(path_extensions_dir, dirname_annotations)
    path_setuppy_build_dir:str = os.path.join(path_root_dir, 'build')


class TestCyBuilder(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCyBuilder, self).__init__(*args, **kwargs)


    def test_a_init(self):
        """ Test init beschrijving """

        # Arrange; remove ext folder
        try:
            shutil.rmtree(DirectoryConfig.path_extensions_dir)
        except:
            pass

        # Act - init to create all required folders
        cythonbuilder.init()

        # Assert - All folders created?
        ext_folder = os.path.isdir(DirectoryConfig.path_extensions_dir)
        pyx_folder = os.path.isdir(DirectoryConfig.path_pyx_dir)
        anno_folder = os.path.isdir(DirectoryConfig.path_annotations_dir)
        self.assertTrue(ext_folder)
        self.assertTrue(pyx_folder)
        self.assertTrue(anno_folder)

    def test_b_build_numpy_not_required(self):
        """ Build succeeds when numpy is not required """

        # Arrange - write a file that we are going to try to build
        # Arrange - write a file that we are going to try to build
        try:
            shutil.rmtree(DirectoryConfig.path_extensions_dir)
        except:
            pass
        cythonbuilder.init()
        file_name = 'test_no_np'
        src_testfile = os.path.join(DirectoryConfig.path_root_dir, 'files_for_testing', f"{file_name}.pyx")
        dst_testfile = os.path.join(DirectoryConfig.path_pyx_dir, f"{file_name}.pyx")
        shutil.copyfile(src_testfile, dst_testfile)

        # Act - build the file
        cythonbuilder.build(numpy_required=False)

        # Assert - Have we built the file?
        found_file = filefinder(directory=DirectoryConfig.path_root_dir, pattern=f'{file_name}*.pyd')
        self.assertIsNotNone(found_file)

    def test_c_build_numpy_required(self):
        """ Build succeeds when numpy is required """

        # Arrange - write a file that we are going to try to build
        try:
            shutil.rmtree(DirectoryConfig.path_extensions_dir)
        except:
            pass
        cythonbuilder.init()
        file_name = 'test_np_needed'
        src_testfile = os.path.join(DirectoryConfig.path_root_dir, 'files_for_testing', f"{file_name}.pyx")
        dst_testfile = os.path.join(DirectoryConfig.path_pyx_dir, f"{file_name}.pyx")
        shutil.copyfile(src_testfile, dst_testfile)

        # Act - build the file
        cythonbuilder.build()

        # Assert - Have we built the file?
        found_file = filefinder(directory=DirectoryConfig.path_root_dir, pattern=f'{file_name}*.pyd')
        self.assertIsNotNone(found_file)

    def test_d_cleanup_moves_pyd_files(self):
        """ Makes sure that cleanup moves pyd files from the root folder to the ext folder """

        # Arrange - write a file that we are going to try to build
        try:
            shutil.rmtree(DirectoryConfig.path_extensions_dir)
        except:
            pass
        cythonbuilder.init()
        file_name = 'built_file_root'
        src_testfile = os.path.join(DirectoryConfig.path_root_dir, 'files_for_testing', f"{file_name}.pyd")
        dst_testfile = os.path.join(DirectoryConfig.path_root_dir, f"{file_name}.pyd")
        shutil.copyfile(src_testfile, dst_testfile)

        # Act
        cythonbuilder.clean()

        # Assert
        # pyd is gone from the root
        found_file_in_root = filefinder(directory=DirectoryConfig.path_root_dir, pattern=f'{file_name}*.pyd')
        self.assertIsNone(found_file_in_root)
        # pyd is present in /ext
        found_file_in_ext = filefinder(directory=DirectoryConfig.path_extensions_dir, pattern=f'{file_name}*.pyd')
        self.assertIsNotNone(found_file_in_ext)

    def test_e_cleanup_moves_html_in_pyx(self):
        """ Makes sure that cleanup moves html files from the ext/pyx folder to the ext/annotations folder """

        # Arrange - write a file that we are going to try to build
        try:
            shutil.rmtree(DirectoryConfig.path_extensions_dir)
        except:
            pass
        cythonbuilder.init()
        file_name = 'annotation'
        file_ext = 'html'
        src_testfile = os.path.join(DirectoryConfig.path_root_dir, 'files_for_testing', f"{file_name}.{file_ext}")
        dst_testfile = os.path.join(DirectoryConfig.path_pyx_dir, f"{file_name}.{file_ext}")
        shutil.copyfile(src_testfile, dst_testfile)

        # Act
        cythonbuilder.clean()

        # Assert
        # html is gone from the pyx folder
        found_file_in_pyx = filefinder(directory=DirectoryConfig.path_pyx_dir, pattern=f'{file_name}*.{file_ext}')
        self.assertIsNone(found_file_in_pyx)
        # pyd is present in /ext/annotations
        found_file_in_anno = filefinder(directory=DirectoryConfig.path_annotations_dir, pattern=f'{file_name}*.{file_ext}')

        self.assertIsNotNone(found_file_in_anno)

    def test_f_cleanup_doesnt_moves_html_above_pyx(self):
        """ Makes sure that cleanup doesnt move html files outside of the ext/pyx folder """

        # Arrange - write a file that we are going to try to build
        try:
            shutil.rmtree(DirectoryConfig.path_extensions_dir)
        except:
            pass
        cythonbuilder.init()
        file_name = 'annotation'
        file_ext = 'html'
        src_testfile = os.path.join(DirectoryConfig.path_root_dir, 'files_for_testing', f"{file_name}.{file_ext}")
        dst_testfile = os.path.join(DirectoryConfig.path_extensions_dir, f"{file_name}.{file_ext}")
        shutil.copyfile(src_testfile, dst_testfile)

        # Act
        cythonbuilder.clean()

        # Assert
        # html still exists in ext dir
        self.assertTrue(os.path.isfile(dst_testfile))
        # html is not found in annotations
        self.assertFalse(os.path.isfile(os.path.join(DirectoryConfig.path_annotations_dir, f"{file_name}.{file_ext}")))

    def test_g_cleanup_dont_keep_annotations(self):
        """ Makes sure that cleanup removes all annotation html files in the ext/pyx folder """

        # Arrange - write a file that we are going to try to build
        try:
            shutil.rmtree(DirectoryConfig.path_extensions_dir)
        except:
            pass
        cythonbuilder.init()
        file_name = 'annotation'
        file_ext = 'html'
        src_testfile = os.path.join(DirectoryConfig.path_root_dir, 'files_for_testing', f"{file_name}.{file_ext}")
        dst_testfile = os.path.join(DirectoryConfig.path_pyx_dir, f"{file_name}.{file_ext}")
        shutil.copyfile(src_testfile, dst_testfile)

        # Act
        cythonbuilder.clean(keep_annotation_files=False)

        # Assert html is not found in annotations
        file_in_annotations = os.path.isfile(os.path.join(DirectoryConfig.path_annotations_dir, f"{file_name}.{file_ext}"))
        self.assertFalse(file_in_annotations)
        # html file not found in pyx folder
        found_html_in_pyx = filefinder(DirectoryConfig.path_pyx_dir, f"{file_name}.{file_ext}")
        self.assertFalse(found_html_in_pyx)

    def test_h_cleanup_keep_c_files(self):
        """ Makes sure that cleanup does not remove the intermediate c files """

        # Arrange - write a file that we are going to try to build
        try:
            shutil.rmtree(DirectoryConfig.path_extensions_dir)
        except:
            pass
        cythonbuilder.init()
        file_name = 'built_c_file'
        file_ext = 'c'
        src_testfile = os.path.join(DirectoryConfig.path_root_dir, 'files_for_testing', f"{file_name}.{file_ext}")
        dst_testfile = os.path.join(DirectoryConfig.path_pyx_dir, f"{file_name}.{file_ext}")
        shutil.copyfile(src_testfile, dst_testfile)

        # Act
        cythonbuilder.clean(keep_c_files=True)

        # Assert c-file is present in pyx folder
        self.assertTrue(os.path.isfile(dst_testfile))


    def test_zzz_cleanup_testing_folder(self):
        """ Called last, to clean up the test folder """
        try:
            shutil.rmtree(DirectoryConfig.path_extensions_dir)
        except:
            pass

def filefinder(directory:str, pattern:str):
    """ Finds a file in a directory. returns either the full path or None"""
    found_files = glob.glob(os.path.join(directory, pattern))
    if (len(found_files) > 1):
        raise ValueError("Found more than 1 file that adheres to the provided pattern")
    if (len(found_files) == 0):
        return None
    else:
        return found_files[0]



if __name__ == '__main__':
    unittest.main()
