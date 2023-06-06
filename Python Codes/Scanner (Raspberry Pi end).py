from NetworkService import NetworkService
from FileModel import FileModel
from MotorModel import MotorModel
from WebService import ChromiumService
from picamera import PiCamera
import RPi.GPIO as GPIO
import pynput
from pynput import keyboard
from time import sleep

#Initialize camera positions (in steps) as global variables
verticalPos = 0
horizontalPos = 0

#Reset camera position to minimum vertically and horizontally from object
def Reset(motors):
    fileModel = FileModel()
    #If cache file exists
    if (fileModel.CheckForFile('motors.txt')):
        positions = fileModel.ReadFromFile('motors.txt')
        #positions[0] = horizontal position of camera (motor 1 (motors[0]))
        #positions[1] = vertical position of camera (motor 2)
        motors[1].Reset(positions[1])
        motors[0].Reset(positions[0])
    
def OnRelease(key, motors):
    global horizontalPos
    global verticalPos
    if key == keyboard.Key.up:
        # Call Motor Control for motor 2 (vertical control)
        # Direction clockwise (False)
        motors[1].MotorControl(direction = False)
        verticalPos+=200
    elif key == keyboard.Key.down:
        # Call Motor Control for motor 2 (vertical control)
        # Direction counter clockwise (True)
        motors[1].MotorControl(direction = True)
        verticalPos-=200
    elif key == keyboard.Key.right:
        # Call Motor Control for motor 1 (horizontal control)
        # Direction clockwise (False)
        motors[0].MotorControl(direction = False)
        horizontalPos+=200
    elif key == keyboard.Key.left:
        # Call Motor Control for motor 2 (vertical control)
        # Direction counter clockwise (True)
        motors[0].MotorControl(direction = True)
        horizontalPos-=200
    elif key == keyboard.Key.enter:
        return False #Stop listener

def main():

    #Establish connection with Computer
    
    network = NetworkService(50000, 0) # Initialize new network object
    
    #Wait for message 'Connecting' to establish new connection or 'VNC Connected' to connect using previoulsy established connection
    message, computerAddr = network.Listen() #Listen for message from Computer
    if(message == 'Connecting' or message == 'VNC Connected'):
        if(message == 'Connecting'):
            sleep(20) # Wait to make sure Computer broadcast is done
            network.Broadcast('Connecting', 20) #Broadcast 'Connecting' message for 20 seconds
            message, computerAddr = network.ListenFor('VNC Connected') #Wait until VNC Connection is established
    
    # File Model
    fileModel = FileModel() # Initialize new file model object
    
    fileModel.OpenFolder('/home/pi/Desktop/Images') #Call function to create images folder
    
    #Initialize camera and motors
    
    #Create camera object
    camera = PiCamera()
    #Flip camera view
    camera.vflip = True
    #Start camera feed
    camera.start_preview()

    ''' 3 Motors:
    - Motor 1: Moves camera horizontally (right and left keys)
    - Motor 2: Moves camera vertically (up and down keys)
    - Motor 3: Rotates turntable
    '''

    '''
    Create motors Pins array with GPIO pins of each as tuple
    Example: Motor 1:
    Direction pin: 13
    Step pin: 16
    Enable pin: 6 (LOW to enable)
    '''
    motorsPins = [(13,16,6), (22,23,24), (27,18,4)]
    # Create motor array
    motors = []
    for i in range(len(motorsPins)):
        motors.append(MotorModel(motorsPins[i]))
    
    #Reset motor positions
    Reset(motors)
    
    #Allow user to position camera as desired
    with keyboard.Listener(on_release=lambda event: OnRelease(event, motors)) as listener:
        listener.join()
        
    #Scan
    Scanning(motors, camera)
    #End camera feed
    camera.stop_preview()    
    #Close camera to be able to use camera in next scan
    camera.close()
    
    #When done save motor positions in cache for next scan
    Cache(fileModel)
    
    GPIO.cleanup() # Clear GPIO allocations after run
    
    #Send to computer using wamp
    fileModel.ZipFolder('/home/pi/Desktop/Images') #Zip Images Folder
    Upload(computerAddr) #Upload Zipped Folder
    sleep(10) #Wait for 10 seconds in case upload is not done
    
    #Broadcast again to start photogrammetry process on Computer
    network.Broadcast('Scanning Done', 20)
    
def Scanning(motors, camera):
    global verticalPos
    
    pics = 0 #Number of pics to use as index while naming files
    
    for i in range(2):
        # For 360 degrees(200 steps), take 10 pictures
        # => Increment steps by 200/10 = 20
        for i in range(10):
            pic = '/home/pi/Desktop/Images/img'+str(pics)+'.jpg'
            sleep(2) #Make sure camera is stable and not moving
            camera.capture(pic)
            pics+=1
            
            #Turn table clockwise (motor 3)
            motors[2].MotorControl(direction = False, steps = 20, stepDelay = 0.01)
        
        #Camera goes down 3 steps and take pictures again
        motors[1].MotorControl(direction = True, steps =  600)
        verticalPos += 600
            
def Cache(fileModel):
    global horizontalPos
    global verticalPos

    path = 'cache.txt'
    content = (str(horizontalPos) + "\n" + str(verticalPos))
    fileModel.WriteToFile(path, content) #Create or overwrite Cache text file with horizontal and vertical position on separate lines

def Upload(computerAddr):
    chromium = ChromiumService("/usr/lib/chromium-browser/chromedriver") #Initialize new WebService Object with Chromium driver
    # Launch URL
    computerAddr = eval(computerAddr)
    url = "http://" + computerAddr + "/Scanner"
    chromium.Open(url)
    chromium.Upload("/home/pi/Desktop/Images.zip") #Upload Zipped Images Folder
    sleep(2) #Make sure images are uploaded
    chromium.Close()

while(1):    
    main() #Continuously repeat after scan is done

