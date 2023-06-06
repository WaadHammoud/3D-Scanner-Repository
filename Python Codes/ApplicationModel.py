from FileModel import FileModel
import subprocess

class ApplicationModel:
    def __init__(self, app):
        self.app = app #App to run (Example: 'Meshroom.exe')
    
    def GetPath(self, app):
        fileModel = FileModel()
        drive = fileModel.Drive()
        path = fileModel.FindFiles(app, drive + "\\")
        return path
    
    # Open Application and continue with code
    def Open(self, batchPath):
        subprocess.Popen([batchPath])
    
    #Run Application and wait until process is done bedore continuing with code
    def Run(self, batchPath):
        subprocess.call([batchPath])


