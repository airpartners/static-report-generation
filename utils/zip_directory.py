import shutil
import sys

def zip_directory(dirName):
    """
    Creates a compressed copy of the given directory.

    Args:
        dirName: (str) the name of the directory to zip. 
    """
    shutil.make_archive(f'zips/{dirName}', 'zip', dirName)


if __name__ == '__main__':
    # get year and month from sys args
    year_month = sys.argv[1]

    zip_directory(year_month)
