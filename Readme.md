FindDupPy
=========

Find DupPy it's a simple program to search duplicated files and deal with them.
Using 'FindDupPy' you can list, move, rename or delete the duplicated files found very quickly, because its doesn't make a checksum of each file, instead
compares the file size first and then compares byte by byte till find (or not) a difference

## **Syntax

'''python
python3 finduppy.py [-f FOLDERS] [-v] [-a [list|rename|move|delete]] [-m MOVE-FOLDER] [-s] [-c] [-n] [-r RENAME-SUFFIX]

end
'''
## **Samples of usage
- List duplicated files on the current folder
python finddupy.py -v -a list
