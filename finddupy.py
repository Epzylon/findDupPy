'''
Created on 26/11/2015

@author: epzylon
'''
import argparse
from filecmp import cmp
from os import listdir, remove, mkdir
from os.path import isfile, isdir, exists, join, getsize, islink, split
from shutil import move, copy2


#TODO: catch Permission denied exception
#TODO: catch FileNotFoundError
#TODO: Check if links points to upper level directories
#TODO: Avoid wrong codification name files
#TODO: Add replace_with_link function
 
class dupFinder(object):
    """
    This class finds duplicated files on a sorted list of file and size list
    like [[file,size],...] and returns a list of equal files list
    """

    
    def __init__(self):
        self.verbose = False
        self.avoid_empties = True
        self.dirlist = []
        
        #File position on the file/size tup
        self.__f_pos = 0
        #Size position on the file/size tup
        self.__s_pos = 1

    def add_folder(self,folder):
        """
        This method recieve a full path folder and add the files contained
        on it to the file list
        """
        if isdir(folder):
            if self.verbose == True:
                    print("Adding " + folder)
            for f in listdir(folder):
                file = join(folder,f)
                if isdir(file) and not islink(file):
                    self.add_folder(file)
                elif isfile(file) and not islink(file):
                    if self.avoid_empties == True:
                        if getsize(file) != 0:
                            self.dirlist.append([file,getsize(file)])
                    else:
                        self.dirlist.append([file,getsize(file)])
                    #Sorting
                    self.dirlist.sort(key=lambda x: x[self.__s_pos])
        
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
                print("Searching dup for " + str(current[0]))
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
    
    def __init__(self,duplist):
        #On move action, if one file have several duplicates,
        #would you like to move one copy and delete the others?
        self.delete_others = False
    
        self.rename_prefix = "dup_"
        self.move_folder = "/tmp/dups"
        self.skipe_first = False
        self.verbose = False
        
        if duplist != []:
            self.duplist = duplist
        else:
            raise Exception()
        
    def move_dups(self):
        for fileset in self.duplist:
            c_counter = 0
            for dupfile in fileset:
                if self.skipe_first == True:
                    if c_counter == 0:
                        c_counter += 1
                        continue
                else:
                    #If we already has copied othe dup, delete others
                    if self.delete_others == True:
                        remove(dupfile)
                    else:
                        if not exists(self.move_folder):
                            mkdir(self.move_folder)
                        elif isfile(self.move_folder):
                            raise Exception()
                                             
                        move(dupfile, self.move_folder)
                        if args.verbose == True:
                            print("Moving " + dupfile + " to " +
                                  self.move_folder)
                    c_counter += 1
                     
    
    def rename_dups(self):
        #Lets go trhoght the list of duplicateds files
        for fileset in self.duplist:
            c_counter = 0
            #Each file can have several duplicateds files (alls in fileset)
            for dupfile in fileset:
                #If skipe_first is set True
                if c_counter == 0 and self.skipe_first == True:
                    c_counter += 1
                    continue
                    #then do nothing with the first one
                else:
                    c_counter += 1
                    #os.path.split filepath and filename
                    file_path,file_name = split(dupfile)
                    #The new name of the file
                    new_name = file_path + "/" + self.rename_prefix + file_name
                    if args.verbose == True:
                        print('Renamed ' + new_name )
                    copy2(dupfile,new_name)
                    #Removeing the old named file
                    remove(dupfile)
                    
            
    def remove_dups(self):
        for fileset in self.duplist:
            c_counter = 0
            for dupfile in fileset:
                if c_counter == 0:
                    c_counter += 1
                    continue
                else:
                    c_counter += 1
                    remove(dupfile)
    
        
if __name__ == '__main__':
    
    prog_name="finddupy.py"
    
    desc = '''
    Search and delete/move duplicated files
    '''
        
    epilog = "Visit our blog at blog.netsecure.com.ar"
    
    parser = argparse.ArgumentParser(description=desc,
                                     epilog=epilog,prog=prog_name)
    
    parser.add_argument("-f", "--folders",default=".",nargs='*',
                        help="Folders to be processed,"
                        "current folder by default")
    
    parser.add_argument("-a","--action",
                        choices=['list','move','rename','delete'],
                        help="Action to take with the dup files")
    
    parser.add_argument("-m","--move-folder",action='store',
                        help="Folder where to move the duplicated files",
                        dest="mfolder")
    
    parser.add_argument("-s", "--skip-first",action='store_true',
                        dest='skip_first',
                        help='On Move, Delete and Rename actions' +
                        'skip the first found and move/delete/rename the'+
                        ' other copies found. It saves the first file found')
    
    parser.add_argument("-x","--delete-on-move",action='store_true',
                        dest="delete_others",
                        help="Move one file and delete others")
    
    parser.add_argument("-r","--rename-suffix",action='store',
                        help="Rename duplicated files with the prefix provided",
                        dest="rsuffix")
    
    parser.add_argument("-v","--verbose",action='store_true',
                        help="Verbose mode")
    
    args = parser.parse_args()
    dup = dupFinder()
    
    if args.verbose == True:
        dup.verbose = True
        
    for folder in args.folders:
        dup.add_folder(folder)
        
    dup.search_duplicates()
    
    if args.action == 'list':
        for file_set in dup.duplicate:
            if args.verbose == True:
                print("Los siguientes archivos son iguales:")
            for file in file_set:
                print(file)
            print("")
            
    elif args.action == 'move':
        morder = makeOrder(dup.duplicate)
        if args.delete_others == True:
            morder.delete_others = True
            morder.skipe_first = args.skip_first
        morder.move_dups()
        
    elif args.action == 'rename':
        if hasattr(args, 'rsuffix') == True:
            morder = makeOrder(dup.duplicate)
            morder.rename_prefix = args.rsuffix
            morder.skipe_first = args.skip_first
            morder.rename_dups()
        else:
            print("To rename files you must to select an Rename suffix with -r")
            exit(1)
    elif args.action == 'delete':
        morder = makeOrder(dup.duplicate)
        morder.skipe_first = args.skip_first
        morder.remove_dups()
        
        
        

    


    
               

    
            
    
    
    
        
    
    
        
    
    

    
    
    