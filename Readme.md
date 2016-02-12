FindDupPy
=========

Find DupPy it's a simple program to search duplicated files and deal with them.
Using 'FindDupPy' you can list, move, rename or delete the duplicated files found very quickly, because its doesn't make a checksum of each file, instead
compares the file size first and then compares byte by byte till find (or not) a difference

## **Syntax**

```python
python3 finduppy.py [-f FOLDERS] [-v] [-a [list|rename|move|delete]] [-m MOVE-FOLDER] [-s] [-c] [-n] [-r RENAME-SUFFIX]
```
## **Samples of usage**
- List duplicated files on the current folder
```python
python findduppy.py -v -a list
```
- List duplicated files on several folders
```python
python findduppy.py -v -a list -f /var/www /home/web
```
- List duplicated files using CSV output format
```python
python findduppy.py -a list -f /var/www -c
```
- Rename duplicated files found (default suffix is dup_)
```python
python finddppy.py -a rename -f /home -v
```
- Rename duplicated files found specifing a suffix
```python
python findduppy.py -a rename -f /home -r duplicated_ -v
```
- Rename duplicated files skiping the first found
```python
python findduppy.py -a rename -s -f /home -r duplicated_ -v
```
- Delete duplicated files skiping the first found
```python
python findduppy.py -a delete -s -f /opt /var/tmp -v
```
- Delete all duplicated files
```python
python findduppy.py -a delete -f /root -v
```
- Move all the duplicated files
```python
python findduppy.py -a move -m /tmp/dupfiles -f /var/tmp /tmp
```

- Move duplicated files (once per file)
```python
python findduppy.py -a move -m /tmp/dupfiles -f /var/tmp /tmp -x
```