'''
Created on 26/11/2015

@author: Gustavo Rodriguez

'''
import argparse
from filecmp import cmp
from os import listdir, remove, mkdir, replace
from os.path import isfile, isdir, exists, join, getsize, islink, split
from shutil import move
from shutil import Error as shError
import sys



#TODO: Check if links points to upper level directories
#TODO: Avoid wrong codification name files
#TODO: Add replace_with_link function
#TODO: Ignore hiden files

class PermError(Exception):
    """
    Permissions errors with files
    """
    def __init___(self,file,err_type):
        self.file = file
        self.err_type = err_type
        print("The file " + self.file + " is not accesible, error: " + err_type,
              file=sys.stderr)

class NoDupFiles(Exception):
    pass

class IsntAFolder(Exception):
    pass

    
 
class dupFinder(object):
    """
    This class finds duplicated files on a sorted list of file and size list
    like [[file,size],...] and returns a list of equal files list
    """

    
    def __init__(self):
        self.verbose = False
        self.avoid_empties = True
        self.dirlist = []
        self.nonrecursive = False
        self.duplicate = []
        #File position on the file/size tup
        self.__f_pos = 0
        #Size position on the file/size tup
        self.__s_pos = 1

    def add_folder(self,folder):
        """
        This method recieve a full path folder and add the files contained
        on it to the file list
        """
        try:
            if isdir(folder):
                file_list = listdir(folder)
                if self.verbose == True:
                    print("Adding " + folder)
            else:
                raise IsntAFolder
            
        except PermissionError:
            if args.verbose == True:
                print("Can't read content on folder " + folder,file=sys.stderr)
            return
            
        #Searching on the folder
        for f in file_list:
            file = join(folder,f)
                
            #If there is a subfolder:
            if isdir(file) and not islink(file):
                #And non-recursive option is not activated
                if self.nonrecursive == False:
                    #then we add the folder to be analized
                    self.add_folder(file)
            #if it is a file
            elif isfile(file) and not islink(file):
                #avoid to analize empties files
                if self.avoid_empties == True:
                    if getsize(file) != 0:
                        self.dirlist.append([file,getsize(file)])
                else:
                    #we add even if it is a empty
                    self.dirlist.append([file,getsize(file)])
        #Sorting by size
        self.dirlist.sort(key=lambda x: x[self.__s_pos])
        
    def search_duplicates(self):  
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
            if self.verbose == True:
                print("Searching dup for " + str(current[0]))
            #Firs round
            if p_file == "" and p_size == "":
                p_file = current[self.__f_pos]
                p_size = current[self.__s_pos]
            #next ones
            else:
                c_file = current[self.__f_pos]
                c_size = current[self.__s_pos]
                
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
            raise NoDupFiles()
        
        
    def move_dups(self):
        #seek on the duplist
        for fileset in self.duplist:
            c_counter = 0
            dup_counter = 1
            #seek in each file of the dup-filesegt
            for dupfile in fileset:
                #if we want to avoid to remove the first one
                if self.skipe_first == True:
                    if c_counter == 0:
                        c_counter += 1
                        #then do nothing with the first one
                        continue
                else:
                    #If we already has copied othe dup, delete others
                    if self.delete_others == True:
                        try:
                            remove(dupfile)
                        except:
                            raise PermError(dupfile,"Can't Delete")
                    else:
                        #Check whether the move folder exists or not
                        if not exists(self.move_folder):
                            #If doesn't we create
                            mkdir(self.move_folder)
                        elif isfile(self.move_folder):
                            #if already exists a file with the rename folder
                            #we raise an exception
                            raise PermError(self.move_folder,
                                            "There is a file called " +
                                            self.move_folder)
                        try:
                            file_path,file_name = split(dupfile)
                            if exists(join(self.move_folder,file_name)):
                                new_f_name = file_name + "." + str(dup_counter)
                                dup_counter += 1
                                dest = join(self.move_folder, new_f_name)
                            else:
                                dest = join(self.move_folder, file_name)     
                                         
                            move(dupfile,dest)
                            if args.verbose == True:
                                print("Moving " + dupfile + " to " + dest)                           
                        except:
                            raise PermError(dupfile,"Can't move")
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
                    #Coping with the same attributes as the original
                    replace(dupfile,new_name)

                    
            
    def remove_dups(self):
        for fileset in self.duplist:
            c_counter = 0
            for dupfile in fileset:
                if c_counter == 0 and self.skipe_first == True:
                    if self.verbose == True:
                        print("The following file will not be deleted: " + 
                              dupfile)
                    c_counter += 1
                    continue
                else:
                    c_counter += 1
                    if self.verbose == True:
                        print("Removing: " + dupfile)
                    try:
                        remove(dupfile)
                    except:
                        raise PermError(dupfile,"Can't delete " + dupfile)
    
        
if __name__ == '__main__':
    
    prog_name="finddupy.py"
    
    desc = '''
    Search and delete/move/rename duplicated files
    '''
        
    epilog = "Samples on README.md"
    
    parser = argparse.ArgumentParser(description=desc,
                                     epilog=epilog,prog=prog_name)
    
    parser.add_argument("-f", "--folders",default=".",nargs='*',
                        help="Folders to be processed,"
                        "current folder by default")
    
    parser.add_argument("-a","--action",
                        choices=['list','move','rename','delete'],
                        help="Action to be taken with the dup-files")
    
    parser.add_argument("-m","--move-folder",action='store',
                        help="Folder where to move the duplicated files",
                        dest="mfolder")
    
    parser.add_argument("-s", "--skip-first",action='store_true',
                        dest='skip_first',
                        help='On Move, Delete and Rename actions' +
                        ' skip the first found and move/delete/rename the'+
                        ' other copies found. It saves the first file found')
    
    parser.add_argument("-c","--csv-list", action='store_true',
                        dest="csv",help='List in CSV format')
    
    parser.add_argument("-n","--no-recursive",action='store_true',
                        dest='nonrecursive',
                        help="Don't analize recursively sub folders")
    
    parser.add_argument("-x","--delete-on-move",action='store_true',
                        dest="delete_others",
                        help="Move one file and delete others")
    
    parser.add_argument("-r","--rename-suffix",action='store',
                        help="Rename duplicated files with the prefix provided"+
                        "by default dup_",
                        dest="rsuffix")
    
    parser.add_argument("-v","--verbose",action='store_true',
                        help="Verbose mode")
    
    args = parser.parse_args()
    
    #Create the object to search duplicated files
    dup = dupFinder()
    
    #Set on verbose mode if was required
    dup.verbose = args.verbose 
    #Set on Non Recursive if was required       
    dup.nonrecursive = args.nonrecursive
    
    folders_count = 0
    for folder in args.folders:
        try:
            dup.add_folder(folder)
        except IsntAFolder:
            print(folder + " is not a folder or doens't exists",file=sys.stderr) 
        else:
            dup.search_duplicates()
            folders_count += 1
            
    #If duplicated list is empty ther is nothing more todo
    if dup.duplicate == []:
        print("There is no duplicated files")
        exit(0)
    
    if args.action == 'list':
        for file_set in dup.duplicate:
            if args.verbose == True:
                print("The following files are equals: ")
            if args.csv == True:
                line = ""
                for file in file_set:
                    line = line + file + ","
                line = line[0:-1]
                print(line)
            else:
                for file in file_set:
                    print(file)
            print("")
            
    elif args.action == 'move':
        morder = makeOrder(dup.duplicate)
        if args.mfolder != None:
            morder.move_folder = args.mfolder
        morder.delete_others = args.delete_others
        morder.skipe_first = args.skip_first

        try:
            morder.move_dups()
        except PermError as pE:
            if args.verbose == True:
                print("Can't remove file: " + pE.file)
            else:
                print("Can't remove file: " + pE.file, file=sys.stderr)
        
    elif args.action == 'rename':
        if hasattr(args, 'rsuffix') == True:
            morder = makeOrder(dup.duplicate)
            if args.rsuffix != None:
                morder.rename_prefix = args.rsuffix
            morder.skipe_first = args.skip_first
            morder.rename_dups()
        else:
            print("To rename files you must to select an Rename suffix with -r")
            exit(1)
    elif args.action == 'delete':
        morder = makeOrder(dup.duplicate)
        morder.skipe_first = args.skip_first
        morder.verbose = args.verbose
        morder.remove_dups()