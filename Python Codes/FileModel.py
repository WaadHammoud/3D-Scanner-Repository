import os
import shutil
import pathlib

class FileModel:
    def __init__(self):
        self.drive = pathlib.Path.home().drive # Get the name of local drive (Example: C:)
    
    #Check if file exists
    def CheckForFile(self, path):
        if os.path.isfile(path):
            return True
        return False
    
    #Delete Folder
    def DeleteFolder(self, path):
        # Check if folder already exists
        if os.path.isdir(path):
            #If it does delete the directory and all of its contents
            shutil.rmtree(path)
            
    #Open folder
    def OpenFolder(self, path):
        #Delete old folder if it exists
        self.DeleteFolder(path)
        #Create a new folder
        os.mkdir(path)
    
    #Unzip images folder
    def UnzipFolder(self, path):
        #Delete old folder if it exists
        self.DeleteFolder(path)
        #Unzip images folder
        shutil.unpack_archive(path + ".zip", path)
    
    def FindFiles(self, fileName, searchPath):
        results = []

        # Walking top-down from the root
        for root, dir, files in os.walk(searchPath):
           if fileName in files:
                results.append(os.path.join(root, fileName))
        for result in results:
            if '$Recycle.Bin' in result:
                results.pop(results.index(result))
        if len(results)<1:
            return "File not found."
        else: #If downloaded in more than one directory, only return 1
            return results[0]
    
    def WriteToFile(self, path, content): #Pass content as single string     
        #Create or overwrite file
        file = open(path, "w")
        #Write to file
        file.write(content)
        file.close()
        
    def WriteLinesToFile(self, path, content): #Pass contnent as array of strings      
        #Create or overwrite file
        file = open(path, "w")
        #Write to file
        file.writelines(content)
        file.close()
 
    def ReadFromFile(self, path):
        with open(path) as file:
            lines = file.readlines()
        return lines
    
    def ZipFolder(self, path):
        shutil.make_archive(path, 'zip', path)
