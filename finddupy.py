'''
Created on 26/11/2015

@author: epzylon
'''
import argparse

if __name__ == '__main__':
    
    desc = '''
    Search and delete/move duplicated files
    '''
    
    parser = argparse.ArgumentParser(description=desc,prog="finddupy.py")
    parser.add_argument("-l","--list",default=None,
                        help="List all the files the will be processed")
    parser.add_argument("-f", "--folders",default=".",nargs='*',
                        help="Folders to be processed"
    