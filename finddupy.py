'''
Created on 26/11/2015

@author: epzylon
'''
import argparse
from filecmp import cmp
from os import listdir
from os.path import isfile, isdir, join, getsize, islink, split
from shutil import move, copy2


#TODO: catch Permission denied exception
#TODO: Check if links points to upper level directories
#TODO: Avoid wrong codification name files



class fileList(object):
    """
    This class recieve all the folders which will be proccessed
    and will return all the files on it with their respective size
    """
    #Size position on the file/size tup
    __s_pos = 1
    
    def __init__(self):
        self.dirlist = []
        self.verbose = False
    
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
                if self.verbose == True:
                    print("Adding " + file + "\n")
                if isdir(file) and not islink(file):
                    self.add_folder(file)
                elif isfile(file) and not islink(file):
                    self.dirlist.append([file,getsize(file)])
        if self.verbose == True:
            print("Sorting\n")
        self.dirlist.sort(key=lambda x: x[self.__s_pos])
        if self.verbose == True:
            print("End sort\n")
    
class dupFinder(object):
    """
    This class finds duplicated files on a sorted list of file and size list
    like [[file,size],...] and returns a list of equal files list
    """
    #File position on the file/size tup
    __f_pos = 0
    #Size position on the file/size tup
    __s_pos = 1
    def __init__(self,dirlist):
        self.dirlist = dirlist
        self.verbose = False
        
    def search_duplicates(self):  
        """
        Return a list with the files with their respective duplicates
        like [ [file_orig,file_dup1,file_dup2,...],[file_orig2...]
        """
        #The current file and size beeing analized
        _c_file = ""
        _c_size = 0
        
        #The previous file and size
        _p_file = ""
        _p_size = ""
        
        #The duplicate file list
        dup_list = []
        
        #set of duplicated files
        _file_set = []
        
        for current in self.dirlist:
            if self.verbose == True:
                print("Searching dup for " + str(current) + "\n")
            #Firs round
            if _p_file == "" and _p_size == "":
                _p_file = current[self.__f_pos]
                _p_size = current[self.__s_pos]
            #next ones
            else:
                _c_file = current[self.__f_pos]
                _c_size = current[self.__s_pos]
                
                #Compare sizes
                if _p_size == _c_size:
                    #If size are equals, compare the file byte by byte
                    if cmp(_p_file,_c_file):
                        #If are equals, adds the files to the set
                        if not _p_file in _file_set:
                            _file_set.append(_p_file)
                        _file_set.append(_c_file)
                    else:
                        #Otherwise add the set to dup list
                        #and reset the file set
                        if _file_set != []:
                            dup_list.append(_file_set)
                            _file_set = []
                            _p_file = _c_file
                            _p_size = _c_size                      
                else:
                    #If the size are differents
                    # and the set is not empty, adds the set
                    # and reset the set
                    _p_file = _c_file
                    _p_size = _c_size
                    if _file_set != []:
                        dup_list.append(_file_set)
                        _file_set = []
                    
        self.duplicate = dup_list
        return self.duplicate

class makeOrder(object):
    """
    This object excecute the action required with the duplicates files,
    like move, delete or rename.
    """
    #Action to excecute with th dups files
    move = True
    rename = False
    delete = False
    print_dups = False
    
    #On move action, if one file have several duplicates,
    #would you like to move one copy and delete the others?
    delete_others = True
    
    
    rename_prefix = "dup_"
    move_folder = "/tmp/dup"
    
    
    
    def __init__(self,duplist):
        if duplist != []:
            self.duplist = duplist
        else:
            raise Exception()
        
    def move_dups(self):
        for fileset in self.duplist:
            c_counter = 0
            for dupfile in fileset:
                if c_counter == 0:
                    c_counter += 1
                    continue
                else:
                    move(dupfile, self.move_folder)
                    c_counter += 1
                    
    
    def rename_dups(self):
        for fileset in self.duplist:
            c_counter = 0
            for dupfile in fileset:
                if c_counter == 0:
                    c_counter += 1
                    continue
                else:
                    c_counter += 1
                    file_path,file_name = split(dupfile)
                    new_name = file_path + "/" + self.rename_prefix + file_name
                    print(new_name)
                    copy2(dupfile,new_name)
                    
            
        
    
        
            



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
    
    

    
    
    