import glob
import os
import shutil
import unittest

import cythonbuilder
from cythonbuilder.config import AppConfig, LoggingConfig, DirConfig
from dataclasses import dataclass

@dataclass
class TestConfig:
    dir_testfiles = "testfiles"

class TestInit(unittest.TestCase):

    def test_init(self):
        """ Test init beschrijving """

        # Arrange; remove ext folder
        clean_test_folder()

        # Act - init to create all required folders
        cythonbuilder.init()

        # Assert - All folders created?
        ext_folder = os.path.isdir(DirConfig.ext)
        pyx_folder = os.path.isdir(DirConfig.pyx)
        anno_folder = os.path.isdir(DirConfig.anno)
        self.assertTrue(ext_folder)
        self.assertTrue(pyx_folder)
        self.assertTrue(anno_folder)

class TestBuild(unittest.TestCase):
    def test_b_build_numpy_not_required(self):
        """ Build succeeds when numpy is not required """

        # Arrange - write a file that we are going to try to build
        clean_test_folder()
        cythonbuilder.init()
        file_name = 'test_no_np'
        src_testfile = os.path.join(DirConfig.root, TestConfig.dir_testfiles, f"{file_name}.pyx")
        dst_testfile = os.path.join(DirConfig.pyx, f"{file_name}.pyx")
        shutil.copyfile(src_testfile, dst_testfile)

        # Act - build the file
        cythonbuilder.just_build(numpy_required=False)

        # Assert - Have we built the file?
        found_file = filefinder(directory=DirConfig.root, pattern=f'{file_name}*.pyd')
        self.assertIsNotNone(found_file)

    def test_ba_build_spec_file_numpy_not_required(self):
        """ Build succeeds for one specific file """

        # Arrange - write a file that we are going to try to build
        # Arrange - write a file that we are going to try to build
        clean_test_folder()
        cythonbuilder.init()
        # Copy targ file
        file_name_targ = 'test_no_np'
        src_targfile = os.path.join(DirConfig.root, TestConfig.dir_testfiles, f"{file_name_targ}.pyx")
        dst_targfile = os.path.join(DirConfig.pyx, f"{file_name_targ}.pyx")
        shutil.copyfile(src_targfile, dst_targfile)
        # Copy other file
        file_name_other = 'different_file'
        src_otherfile = os.path.join(DirConfig.root, TestConfig.dir_testfiles, f"{file_name_other}.pyx")
        dst_otherfile = os.path.join(DirConfig.pyx, f"{file_name_other}.pyx")
        shutil.copyfile(src_otherfile, dst_otherfile)

        # Act - build the file
        cythonbuilder.build(targetfilenames=[file_name_targ])

        # Assert - Have we built the file?
        targ_file_path = filefinder(directory=DirConfig.ext, pattern=f'{file_name_targ}*.pyd')
        other_file_path = filefinder(directory=DirConfig.ext, pattern=f'{file_name_other}*.pyd')
        self.assertIsNotNone(targ_file_path)
        self.assertIsNone(other_file_path)

    def test_c_build_numpy_required(self):
        """ Build succeeds when numpy is required """

        # Arrange - write a file that we are going to try to build
        clean_test_folder()
        cythonbuilder.init()
        file_name = 'test_np_needed'
        src_testfile = os.path.join(DirConfig.root, TestConfig.dir_testfiles, f"{file_name}.pyx")
        dst_testfile = os.path.join(DirConfig.pyx, f"{file_name}.pyx")
        shutil.copyfile(src_testfile, dst_testfile)

        # Act - build the file
        cythonbuilder.just_build(numpy_required=True, debugmode=True, targetfilenames=[file_name])

        # Assert - Have we built the file?
        found_file = filefinder(directory=DirConfig.root, pattern=f'{file_name}*.pyd')
        self.assertIsNotNone(found_file)

        # # Arrange - write a file that we are going to try to build
        # clean_test_folder()
        # cythonbuilder.init()
        #
        # # Copy targ file
        # file_name = 'test_np_needed'
        # src_testfile = os.path.join(DirConfig.root, TestConfig.dir_testfiles, f"{file_name}.pyx")
        # self.assertTrue(os.path.isfile(src_testfile))
        # dst_testfile = os.path.join(DirConfig.pyx, f"{file_name}.pyx")
        # shutil.copyfile(src_testfile, dst_testfile)
        #
        # # Act - build the file
        # cythonbuilder.just_build(numpy_required=True)  # default true
        #
        # # Assert - Have we built the file?
        # found_file = filefinder(directory=DirConfig.root, pattern=f'{file_name}*.pyd')
        # self.assertIsNotNone(found_file)

class TestClean(unittest.TestCase):
    def test_d_cleanup_moves_pyd_files(self):
        """ Makes sure that cleanup moves pyd files from the root folder to the ext folder """

        # Arrange - write a file that we are going to try to build
        clean_test_folder()
        cythonbuilder.init()

        file_name = 'built_file_root'
        src_testfile = os.path.join(DirConfig.root, TestConfig.dir_testfiles, f"{file_name}.pyd")
        dst_testfile = os.path.join(DirConfig.root, f"{file_name}.pyd")
        shutil.copyfile(src_testfile, dst_testfile)

        # Act
        cythonbuilder.clean()

        # Assert
        # pyd is gone from the root
        found_file_in_root = filefinder(directory=DirConfig.root, pattern=f'{file_name}*.pyd')
        self.assertIsNone(found_file_in_root)
        # pyd is present in /ext
        found_file_in_ext = filefinder(directory=DirConfig.ext, pattern=f'{file_name}*.pyd')
        self.assertIsNotNone(found_file_in_ext)

    def test_e_cleanup_moves_html_in_pyx(self):
        """ Makes sure that cleanup moves html files from the ext/pyx folder to the ext/annotations folder """

        # Arrange - write a file that we are going to try to build
        clean_test_folder()
        cythonbuilder.init()

        file_name = 'annotation'
        file_ext = 'html'
        src_testfile = os.path.join(DirConfig.root, TestConfig.dir_testfiles, f"{file_name}.{file_ext}")
        dst_testfile = os.path.join(DirConfig.pyx, f"{file_name}.{file_ext}")
        shutil.copyfile(src_testfile, dst_testfile)

        # Act
        cythonbuilder.clean()

        # Assert
        # html is gone from the pyx folder
        found_file_in_pyx = filefinder(directory=DirConfig.pyx, pattern=f'{file_name}*.{file_ext}')
        self.assertIsNone(found_file_in_pyx)
        # pyd is present in /ext/annotations
        found_file_in_anno = filefinder(directory=DirConfig.anno, pattern=f'{file_name}*.{file_ext}')

        self.assertIsNotNone(found_file_in_anno)

    def test_f_cleanup_doesnt_moves_html_above_pyx(self):
        """ Makes sure that cleanup doesnt move html files outside of the ext/pyx folder """

        # Arrange - write a file that we are going to try to build
        clean_test_folder()
        cythonbuilder.init()

        file_name = 'annotation'
        file_ext = 'html'
        src_testfile = os.path.join(DirConfig.root, TestConfig.dir_testfiles, f"{file_name}.{file_ext}")
        dst_testfile = os.path.join(DirConfig.ext, f"{file_name}.{file_ext}")
        shutil.copyfile(src_testfile, dst_testfile)

        # Act
        cythonbuilder.clean()

        # Assert
        # html still exists in ext dir
        self.assertTrue(os.path.isfile(dst_testfile))
        # html is not found in annotations
        self.assertFalse(os.path.isfile(os.path.join(DirConfig.anno, f"{file_name}.{file_ext}")))

    def test_g_cleanup_dont_keep_annotations(self):
        """ Makes sure that cleanup removes all annotation html files in the ext/pyx folder """

        # Arrange - write a file that we are going to try to build
        clean_test_folder()
        cythonbuilder.init()

        file_name = 'annotation'
        file_ext = 'html'
        src_testfile = os.path.join(DirConfig.root, TestConfig.dir_testfiles, f"{file_name}.{file_ext}")
        dst_testfile = os.path.join(DirConfig.pyx, f"{file_name}.{file_ext}")
        shutil.copyfile(src_testfile, dst_testfile)

        # Act
        cythonbuilder.clean(keep_annotation_files=False)

        # Assert html is not found in annotations
        file_in_annotations = os.path.isfile(os.path.join(DirConfig.anno, f"{file_name}.{file_ext}"))
        self.assertFalse(file_in_annotations)
        # html file not found in pyx folder
        found_html_in_pyx = filefinder(DirConfig.pyx, f"{file_name}.{file_ext}")
        self.assertFalse(found_html_in_pyx)

    def test_h_cleanup_keep_c_files(self):
        """ Makes sure that cleanup does not remove the intermediate c files """

        # Arrange - write a file that we are going to try to build
        clean_test_folder()
        cythonbuilder.init()

        file_name = 'built_c_file'
        file_ext = 'c'
        src_testfile = os.path.join(DirConfig.root, TestConfig.dir_testfiles, f"{file_name}.{file_ext}")
        dst_testfile = os.path.join(DirConfig.pyx, f"{file_name}.{file_ext}")
        shutil.copyfile(src_testfile, dst_testfile)

        # Act
        cythonbuilder.clean(keep_c_files=True)

        # Assert c-file is present in pyx folder
        self.assertTrue(os.path.isfile(dst_testfile))

    def test_i_cleanup_removes_build_folder(self):
        """ Makes sure that cleanup does not remove the intermediate c files """

        # Arrange - write a file that we are going to try to build
        clean_test_folder()
        cythonbuilder.init()
        file_name = 'test_no_np'
        src_testfile = os.path.join(DirConfig.root, TestConfig.dir_testfiles, f"{file_name}.pyx")
        dst_testfile = os.path.join(DirConfig.pyx, f"{file_name}.pyx")
        shutil.copyfile(src_testfile, dst_testfile)
        cythonbuilder.just_build()

        # Act - build the file
        build_folder_exists = os.path.isdir(DirConfig.build)
        cythonbuilder.clean()
        build_folder_exists_after = os.path.isdir(DirConfig.build)

        # Assert c-file is present in pyx folder
        self.assertNotEqual(build_folder_exists, build_folder_exists_after)


def filefinder(directory:str, pattern:str):
    """ Finds a file in a directory. returns either the full path or None"""
    found_files = glob.glob(os.path.join(directory, pattern))
    if (len(found_files) > 1):
        raise ValueError("Found more than 1 file that adheres to the provided pattern")
    if (len(found_files) == 0):
        return None
    else:
        return found_files[0]
def clean_test_folder():
    """ removes ext dir and pyd files frm the test folder """
    try:
        shutil.rmtree(DirConfig.ext)
    except:
        pass

    pydfiles_in_root = [f for f in os.listdir(DirConfig.root) if (".pyd" in f)]
    [os.remove(f) for f in pydfiles_in_root]


if __name__ == '__main__':
    unittest.main()

