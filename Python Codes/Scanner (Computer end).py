from NetworkService import NetworkService
from FileModel import FileModel
from ApplicationModel import ApplicationModel
from time import sleep

# Establish correct IP addresses
def NetworkConnection(network):
    network.Broadcast('Connecting', 20) # Broadcast 'Connecting' message for 20 seconds
    message, piAddr = network.ListenFor('Connecting') # Listen for 'Connecting' message from Pi
    piAddr = eval(piAddr) # Remove quotes
    return piAddr

def main():
    
    sleep(60) # Wait 10 seconds to make sure Pi is booted and connected to the internet

    # File Model
    fileModel = FileModel() # Initialize new file model object
    drive = fileModel.drive # Get the name of local drive (Example: C:)
    
    #Network
    network = NetworkService(0, 50000) # Initialize new network object
    
    #VNC Connection
    vncViewer = ApplicationModel('vncviewer.exe')
    
    vncConnect = drive + "\wamp64\www\Scanner\connect.bat" # Path of bat file that will run VNC Viewer
    vncConnection = drive + "\wamp64\www\Scanner\connection.vnc" #Path of config file that contains host info (username, pass...)
    vncDisconnect = drive + "\wamp64\www\Scanner\disconnect.bat" #Path of bat file that will disconnect VNC Viewer

    #If VNC Bat file does not exist, create it
    if (fileModel.CheckForFile(vncConnect) == False):
        vncPath = drive + "\Program Files\RealVNC\VNC Viewer\\vncviewer.exe" # VNC Viewer Path is the same on all computer
        if(fileModel.CheckForFile(vncPath) == False):
            print("Please download and install VNC Viewer.")
        vncPath = "\"" + vncPath + "\"" # Add quotations to execute in command line later
        
        piAddr = NetworkConnection(network) # Establish network connection between computer and Pi
        lines = fileModel.ReadFromFile(vncConnection)
        lines[1] = "Host=" + piAddr + "\n" # Change Host address to current IP address
        fileModel.WriteLinesToFile(vncConnection, lines)
        
        vncConnection ="\"" + vncConnection + "\"" #Add quotes
        command = vncPath + " " + vncConnection #Command to be executed in command prompt
        fileModel.WriteToFile(vncConnect, command) #Save command in batch file to be executed
    
    vncViewer.Open(vncConnect) #Make the connection
    sleep(2) #Allow some time to establish connection
    
    network.Broadcast('VNC Connected', 4) #Tell Pi that VNC connection is established and to start scanning

    #Wait until Pi is done image preparation and upload before running Meshroom
    message, address = network.ListenFor('Scanning Done')
        
    #Close VNC Connection
    
    #If Disconnect Bat File doesn't exist, create it
    if (fileModel.CheckForFile(vncDisconnect) == False):
        command = "taskkill /IM \"vncviewer.exe\"" #Kill VNC Viewer
        fileModel.WriteToFile(vncDisconnect, command)

    vncViewer.Run(vncDisconnect) # Kill VNC connection

    # Run Meshroom
    
    meshroom = ApplicationModel("meshroom_batch.exe")
    meshroomBat = drive + "\wamp64\www\Scanner\meshroom.bat" #Path of bat file that will run Mehsroom
    imagesPath =  drive + "\wamp64\www\Scanner\Images" #Path of Images folder after unzip
    outputFolder = drive + "\wamp64\www\Scanner\Mesh" #Path of folder to save mesh in
    outputPath = "\"" + drive + "\wamp64\www\Scanner\Mesh\mesh.mg" + "\"" #Path of output Mesh
    
    fileModel.UnzipFolder(imagesPath) # Unzip images folder
    fileModel.OpenFolder(outputFolder) #Open Mesh folder
    
    imagesPath = "\"" + imagesPath + "\"" #Add quotes
    
    #If meshroom Batch file does not exist, create it
    if (fileModel.CheckForFile(meshroomBat) == False):
        meshroomPath = fileModel.FindFiles(meshroom.app, drive + "\\") # Find meshroom_batch.exe application on computer
        if(meshroomPath == 'File Not Found.'):
            print("Please download and install Meshroom.")
        meshroomPath = "\"" + meshroomPath + "\"" # Add quotations to execute in command line later
        
        #Command line should execute the line: meshroom_batch file path -i images folder path --save output folder path with file name --toNode Texturing

        command = meshroomPath + " -i " + imagesPath + " --save " + outputPath + " --toNode Texturing" #Command to be executed in command prompt
        
        fileModel.WriteToFile(meshroomBat, command) #Save command in batch file to be executed
        
    meshroom.Run(meshroomBat) # Run Meshroom
    #Open Textured Mesh in Meshlab
    
    meshlab = ApplicationModel("meshlab.exe")
    
    #texturedMesh.obj file is saved in Meshroom Cache, its enclosing folder is generated with different names each time
    # -> Search for .obj file starting from Meshroom Cache folder
    rootdir = drive + "\wamp64\www\Scanner\Mesh\MeshroomCache"
    texturedMesh = fileModel.FindFiles('texturedMesh.obj', rootdir)
    texturedMesh = "\"" + texturedMesh + "\"" #Add quotes
    
    meshlabBat = drive + "\wamp64\www\Scanner\meshlab.bat" #Path of bat file that will run Meshlab

    #If meshlab Batch file does not exist, create it
    if (fileModel.CheckForFile(meshlabBat) == False):
        meshlabPath = drive + "\Program Files\VCG\MeshLab\meshlab.exe" # Meshlab Path is the same on all computer
        if(fileModel.CheckForFile(meshlabPath) == False):
            print("Please download and install Meshlab to view output or open Mesh.mg using Meshroom.")
        meshlabPath = "\"" + meshlabPath + "\"" # Add quotations to execute in command line later
        
        command = meshlabPath + " " + texturedMesh #command to execute in command line
        
        fileModel.WriteToFile(meshlabBat, command) #Save command in batch file to be executed
        
    meshlab.Open(meshlabBat) # Open Textured mesh in Meshlab

main()
