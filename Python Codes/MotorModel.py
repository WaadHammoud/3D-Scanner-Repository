import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

class MotorModel:
    def __init__(self, motorPins): #motorPins given as tuple (Direction pin, Step pin, Enable pin)
        self.motorPins = motorPins
        # Declare motor object with GPIO pins numbers and motor type
        self.motor = (RpiMotorLib.A4988Nema(motorPins[0], motorPins[1], (21,21,21),"DRV8825"))
        GPIO.setup(motorPins[2],GPIO.OUT) # Set enable pin as output
        
    def MotorControl(self, direction, stepType = "Full", steps =200, stepDelay = 0.0005, initialDelay = 0.0005):
        # Pull enable pin to low to enable motor
        GPIO.output(self.motorPins[2],GPIO.LOW)
        '''
        Argumnets:
        - Direction = False for Clockwise, True for Counter Clockwise
        - Step type can be (Full,Half,1/4,1/8,1/16,1/32)
        - Number of steps (for 360 degrees (Full step type) = 200 steps)
        - Step Delay in seconds
        - Set to true to print verbose output
        - Initial delay in seconds
        '''
        #Default steps = 200 => Move motor 200 stepa (360 degrees)
        self.motor.motor_go(direction,"Full", steps ,stepDelay, False, initialDelay)
        #time.sleep(0.5)
    
    #Reset motor given its current position (in steps)
    def Reset(self, position):
        if position>0:
        #Motor needs to move counter clockwise to reach reset point
            self.MotorControl(direction = True, steps = abs(position))
        elif position<0:
        #Motor needs to move clockwise to reach reset point
            self.MotorControl(direction = False, steps = abs(position))
    
        
