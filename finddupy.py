'''
Created on 26/11/2015

@author: epzylon
'''
import argparse
from os import listdir
from os.path import isfile, isdir, join, getsize

#TODO: catch Permission denied exception


class filelist(object):
    """
    This object recieve all the folders which will be proccessed
    and will return all the files on it with ther respective size
    """
    #File position on the file/size tup
    f_pos = 0
    #Size position on the file/size tup
    s_pos = 1
    
    def __init__(self):
        self.dirlist = []
        self.current = 0
    
    def __iter__(self):
        return self
    
    def add_folder(self,folder):
        """
        This method recieve a full path folder and add the files contained
        on it to the file list
        """
        if isdir(folder):
            for f in listdir(folder):
                file = join(folder,f)
                if isdir(file):
                    self.add_folder(file)
                elif isfile(file):
                    self.dirlist.append([file,getsize(file)])
        self.dirlist.sort(key=lambda x: x[self.s_pos])
    
    def get_dup_list(self):  
        """
        Return a list with the files with their respective duplicates
        like [ [file_orig,file_dup1,file_dup2,...],[file_orig2...]
        """
        #The current file beeing analized
        current_file = ""
        #The size of the current file
        size = 0
        
        for file_and_size in self.dirlist:
            
            #First loop
            if file_and_size[self.f_pos] == "" and size == 0:
                #Save the first file name and their size
                current_file = file_and_size[self.f_pos]
                size = file_and_size[self.s_pos]
                continue
            #Followings loops
            else:
                #Do not compare if the file path is the same
                if file_and_size[self.f_pos] == current_file:
                    continue
                #Skip empty files
                elif file_and_size[self.s_pos] == 0:
                    continue
                else:
                    #Otherwise if the size is the same
                    if size == file_and_size[self.s_pos]:
                        #Read firs bytes
                        pass
                        
            
            
            
            


if __name__ == '__main__':
    
    desc = '''
    Search and delete/move duplicated files
    '''
    
    parser = argparse.ArgumentParser(description=desc,prog="finddupy.py")
    parser.add_argument("-l","--list",default=None,
                        help="List all the files the will be processed")
    parser.add_argument("-f", "--folders",default=".",nargs='*',
                        help="Folders to be processed")
    

    
    
    