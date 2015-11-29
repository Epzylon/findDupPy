'''
Created on 26/11/2015

@author: epzylon
'''
import argparse
from filecmp import cmp
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
        self.duplicate = []
    
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
        #The current file and size beeing analized
        c_file = ""
        c_size = 0
        
        #The previous file and size
        p_file = ""
        p_size = ""
        
        #The duplicate file list
        dup_list = []
        
        #set of duplicated files
        file_set = []
        
        for current in self.dirlist:
            #Firs round
            if p_file == "" and p_size == "":
                p_file = current[self.f_pos]
                p_size = current[self.s_pos]
            #next ones
            else:
                c_file = current[self.f_pos]
                c_size = current[self.s_pos]
                
                #Compare sizes
                if p_size == c_size:
                    #If size are equals, compare the file byte by byte
                    if cmp(p_file,c_file):
                        #If are equals, adds the files to the set
                        if not p_file in file_set:
                            file_set.append(p_file)
                        file_set.append(c_file)
                    else:
                        #Otherwise add the set to dup list
                        #and reset the file set
                        if file_set != []:
                            dup_list.append(file_set)
                            file_set = []
                            p_file = c_file
                            p_size = c_size                      
                else:
                    #If the size are differents
                    # and the set is not empty, adds the set
                    # and reset the set
                    p_file = c_file
                    p_size = c_size
                    if file_set != []:
                        dup_list.append(file_set)
                        file_set = []
                    
        self.duplicate = dup_list
        return dup_list
                         
            


if __name__ == '__main__':
    
    desc = '''
    Search and delete/move duplicated files
    '''
    
    parser = argparse.ArgumentParser(description=desc,prog="finddupy.py")
    parser.add_argument("-l","--list",default=None,
                        help="List all the files the will be processed")
    parser.add_argument("-f", "--folders",default=".",nargs='*',
                        help="Folders to be processed")
    
    args = parser.parse_args()
    
    

    
    
    