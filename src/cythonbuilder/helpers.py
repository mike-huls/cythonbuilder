import os
import shutil

from .definitions import PACKAGE_ROOT
from .services import logger


class FilesAndFolders:

    @staticmethod
    def create_folder(folderpath: str) -> None:
        if (os.path.exists(folderpath)):
            logger.debug(msg=f"{FilesAndFolders.create_folder.__name__}] - provided folder already exists: '{folderpath}', skipping..")
            return
        os.mkdir(path=folderpath)
        logger.debug(msg=f"{FilesAndFolders.create_folder.__name__}] - created folder")

    @staticmethod
    def remove_folder(folderpath: str) -> None:
        if (not os.path.isdir(folderpath)):
            logger.debug(msg=f"{FilesAndFolders.remove_folder.__name__}] - provided folder cannot be removed: it does not exist: '{folderpath}', skipping..")
            return
        shutil.rmtree(folderpath)
        logger.debug(msg=f"{FilesAndFolders.remove_folder.__name__}] - Removed folder {folderpath}")

    @staticmethod
    def create_empty_file(filepath: str, overwrite: bool = False) -> None:
        """ Creates an empty file if not exists """
        if (not overwrite):
            if (os.path.isfile(filepath)):
                logger.debug(msg=f"{FilesAndFolders.create_empty_file.__name__}] - provided filepath already exists '{filepath}', skipping..")
                return
        with open(filepath, 'w') as file:
            file.write("")

    @staticmethod
    def replace_in_file(targetfilepath: str, replace_this_text: str, replacment_text: str) -> None:
        """ Replaces a text with the replacement text in a text file """

        # Validate
        if (not os.path.isfile(targetfilepath)):
            raise ValueError(f"{FilesAndFolders.replace_in_file.__name__}] - provided filepath invalid; does not exist: {targetfilepath}")

        # Open target, replace string and write again
        with open(targetfilepath, 'r') as file:
            filedata = file.read()
        filedata = filedata.replace(replace_this_text, replacment_text)
        with open(targetfilepath, 'w') as file:
            file.write(filedata)

    @staticmethod
    def copy_file(targetfilename: str, destinationpath:str, overwrite: bool = False) -> None:
        """ download a file from a url to the given file path """

        source = os.path.join(PACKAGE_ROOT, 'files', targetfilename)
        if (not os.path.isfile(source)):
            raise ValueError(f"{FilesAndFolders.copy_file.__name__}] - provided filename invalid; source file does not exist: {source}")
        if (not os.path.isdir(os.path.dirname(destinationpath))):
            raise ValueError(f"{FilesAndFolders.copy_file.__name__}] - provided destination invalid; target folder does not exist: {os.path.dirname(destinationpath)}")

        # Overwrite?
        if (not overwrite):
            if (os.path.isfile(destinationpath)):
                logger.debug(msg=f"[{FilesAndFolders.copy_file.__name__}] - File {targetfilename} already exists. Skipping..")
                return

        # Copy
        logger.debug(f"copying {source} to {destinationpath}")
        with open(destinationpath, 'w') as dst:
            with open(source, 'r') as src:
                dst.write(src.read())

    @staticmethod
    def remove_file(targetfilename:str) -> None:
        """ Remove specified file """
        if (not os.path.isfile(targetfilename)):
            raise ValueError(f"{FilesAndFolders.remove_file.__name__}] - provided filename invalid; target file does not exist: {targetfilename}")
        os.remove(targetfilename)

    @staticmethod
    def move_file(srcfilename: str, dstfilename:str, overwrite: bool = False) -> None:
        """ download a file from a url to the given file path """

        if (not os.path.isfile(srcfilename)):
            raise ValueError(f"{FilesAndFolders.move_file.__name__}] - provided source filename invalid; source file does not exist: {srcfilename}")
        if (not os.path.isdir(os.path.dirname(dstfilename))):
            raise ValueError(f"{FilesAndFolders.move_file.__name__}] - provided destination folder invalid; does not exist: {os.path.isdir(os.path.dirname(dstfilename))}")

        if (os.path.isfile(dstfilename) and not overwrite):
            raise ValueError(f"{FilesAndFolders.move_file.__name__}] - cannot move file; target file already exists: {os.path.isdir(os.path.dirname(dstfilename))}")

        # Copy
        logger.debug(f"moving {srcfilename} to {dstfilename}")
        shutil.move(src=srcfilename, dst=dstfilename)


class CliTools:
    @staticmethod
    def pop_arg_or_exit(arglist: [str], errormessage: str):
        """ Tries to pop an arg from the list. If this is not possible: display errormessage and exit """
        if (len(arglist) <= 0):
            logger.error(msg=errormessage)
            quit()
        return arglist.pop(0).lower()


def package_is_installed(package_import_name:str=None) -> bool:
    """ Returns t/f depending on whether a package is installed in this project
        :arg package_import_name   str     name of the package you're checking
    """

    if (package_import_name == None or package_import_name == 'venv'):
        return False
    _package_installed = False
    try:
        exec(f"import {package_import_name}")
        _package_installed = True
    except ImportError:
        pass
    except Exception as e:
        raise e
    return _package_installed
