import shutil
import sys

def zip_directory(dirName):
    """
    Creates a compressed copy of the given directory.

    :param dirName: (str) the name of the directory to zip
    :returns: none, makes a zipped directory file
    """
    shutil.make_archive(f'zips/{dirName}', 'zip', dirName)


if __name__ == '__main__':
    # get year and month from sys args
    year_month = sys.argv[1]

    zip_directory(year_month)
