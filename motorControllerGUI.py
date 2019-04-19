# Coded by Manuel L.
import tkinter         #import everything from the tkinter class
from tkinter import messagebox
import ue9
import LabJackPython      # The python program should be in the same folder of the modules
import time

# GUI Elements
myWindow = tkinter.Tk()  # Create the window form
myWindow.configure(bg = '#88324f')
myWindow.title("Team F Motor Control")  # Change the title of the window form

topFrame = tkinter.Frame(myWindow, bg = "#88324f")  # Create a frame
topFrame.grid(row = 0)                  # Show the frame and assign it position

middleFrame = tkinter.Frame(myWindow, bg = "#88324f")               # Create a frame
middleFrame.grid(row = 1)               # Show the frame and assign it position

bottomFrame = tkinter.Frame(myWindow, bg = "#88324f", height = 300) # Create a frame
bottomFrame.grid(row = 2)                   # Show the frame and assign it position

# Functions
def resetMotor ():
    def getCredentials():
        global emergencyPressed
        global motorState
        global ipAddUE9
        global myUE9

        username = usernameBox.get()    # Get username from textbox
        password = passwordBox.get()    # Get password from textbox
        
        if username == "etd" and password == "123":
            direction["text"] = "Direction: RIGHT"
            state['text'] = "Motor: ON   "
            speedScale.set(50)  # Set Scale to 50 % when motor is turned ON
            
            ipAddUE9 = ue9IpBox.get()   # Get the Ip address from textbox

            myUE9 = ue9.UE9(ethernet = True, ipAddress = ue9IpBox.get())  # Connect to UE9 by its IP address
           
            # Right Direction
            myUE9.singleIO(1, 1, Dir = 1, State = 1)["FIO1 State"]
            myUE9.singleIO(1, 2, Dir = 1, State = 1)["FIO2 State"]
            myUE9.singleIO(1, 3, Dir = 1, State = 0)["FIO3 State"]
                   
            # Set timer value to 50% by using 32768 in Timer0Value
            myUE9.timerCounter(TimerClockBase = 1, TimerClockDivisor = 29, Timer0Mode = 0, NumTimersEnabled = 1, UpdateConfig = 1, Timer0Value = 32768)

            # Clear the logging elements
            credentials.destroy()
            usernameBox.destroy()
            passwordBox.destroy()
            login.destroy()
            invalid["fg"] = "#88324f"       # keep "Invalid" message hidden
            motorState = 1
            emergencyPressed = 0

        else:
            invalid["fg"] = "light red"     # Reveal "Invalid" message hidden
    
    credentials = tkinter.Label(topFrame, text="Enter Credentials: ", bg="#88324f", fg="white", font=("Bold Courier", 10))
    usernameBox = tkinter.Entry(topFrame)
    passwordBox = tkinter.Entry(topFrame, show="*")
    login = tkinter.Button(topFrame, text="Login", command = getCredentials)
    invalid = tkinter.Label(topFrame, text="Invalid Creddentials!", bg="#88324f", fg = "#88324f", font=("Bold Courier", 10))
                
    credentials.grid(row = 1, column = 0, sticky = tkinter.W)
    usernameBox.grid(row = 2, column = 0, sticky = tkinter.W)
    passwordBox.grid(row = 3, column = 0, sticky = tkinter.W)
    login.grid(row = 4, column = 0, sticky = tkinter.W)
    invalid.grid(row = 5, column = 0, sticky = tkinter.W)
    

def shutDown():      # This Function will set the input pins LOW and Open Popup window
    global myUE9
    global confirmation  
    global motorState
    global timer_Value
    
    confirmation = 0
    motorState = 0
    direction["text"] = "Direction:      "
    state['text'] = "Motor: OFF  "

    # Stop Motor
    myUE9.singleIO(1, 2, Dir = 1, State = 0)["FIO2 State"]
    myUE9.singleIO(1, 3, Dir = 1, State = 0)["FIO3 State"]
    
    # Create a PopUp window for Turning Motor ON    
    confirmation = messagebox.askyesno("Confimation Message", "The Motor was STOP due Emergency! Would like to Turn it back ON?")
    if confirmation == 1:
        resetMotor()            # Calls resetMotor function to turn motor ON

def powerOn():
    global myUE9
    global motorState
    global emergencyPressed
    
    if emergencyPressed == 1:   # Calls ShutDown function to create popup window
        shutDown()     
        
    elif motorState == 0:       # Calls resetMotor function to turn motor ON
        resetMotor()
    
def dirLeft(event):
    
    global myUE9
    global motorState
    global timer_Value
    
    if motorState == 1:
        direction["text"] = "Direction: LEFT "
        
        # Stop Motor for few milli second 
        myUE9.singleIO(1, 2, Dir = 1, State = 0)["FIO2 State"]
        myUE9.singleIO(1, 3, Dir = 1, State = 0)["FIO3 State"]
        time.sleep(0.1)
        
        # Change motor dirention to the Left
        myUE9.singleIO(1, 2, Dir = 1, State = 0)["FIO2 State"]
        myUE9.singleIO(1, 3, Dir = 1, State = 1)["FIO3 State"]

    
def dirRight(event):
    
    global myUE9
    global motorState
    global timer_Value
    
    if motorState == 1:
        direction["text"] = "Direction: RIGHT"
        
        # Stop Motor for few milli second 
        myUE9.singleIO(1, 2, Dir = 1, State = 0)["FIO2 State"]
        myUE9.singleIO(1, 3, Dir = 1, State = 0)["FIO3 State"]
        time.sleep(0.1)
        
        # Change motor dirention to the Right
        myUE9.singleIO(1, 2, Dir = 1, State = 1)["FIO2 State"]
        myUE9.singleIO(1, 3, Dir = 1, State = 0)["FIO3 State"]

def pushButtonCheck():      # This funtion will check for input pins states
    
    global myUE9
    global emergencyPressed # Represent input pins change of state
    global confirmation     # Popup window response
    global motorState       # Motor State
    
    stopPushButton =  myUE9.singleIO(1, 5, Dir = 0, State = 1)["FIO5 State"]  
    time.sleep(0.05)
    resetPushButton =  myUE9.singleIO(1, 4, Dir = 0, State = 1)["FIO4 State"]
    sensor = myUE9.singleIO(1, 1, Dir = 0, State = 1)["FIO1 State"]
        
    if stopPushButton == 1 or sensor == 0:    # Stop motor if Stop Button or sensor are trigged
        myUE9.singleIO(1, 2, Dir = 1, State = 0)["FIO2 State"]
        myUE9.singleIO(1, 3, Dir = 1, State = 0)["FIO3 State"]
        
        direction["text"] = "Direction:      "
        state['text'] = "Motor: OFF  "
        confirmation = 0
        motorState = 0
        emergencyPressed = 1
        
    elif resetPushButton == 1 and emergencyPressed == 1:
        shutDown()     # Call shuDown to generate popup window

    myWindow.after(100, pushButtonCheck)  # Callback the same function after 100ms

def upKeyPress(event):                      # This Function Increases the Slider value
    speedScale.set(speedScale.get() + 5)
    
def downKeyPress(event):                    # This Function Decreases the Slider value
    speedScale.set(speedScale.get() - 5)
    
def motorSpeed (percentage):     # This Function change the PWM D.C.
   
    global myUE9
    global timer_Value    
    percentageInv = 100 - int(percentage)  # Invert speed slider value
    
    # Parameter for PWM freq.
    # TimerClockBase (0 = 750kHz Base Clock Freq. 1 = 48MHz Base Clock Freq)
    # The TimerClockDivisor value (1 - 256)
    # TimerMode (0 => 16-bit resolution Timer Mode Value = 65,536; 1 => 8-bit = 256)

    # Small TimerValue corresponds to a large D.C., and a large TimerValue corresponds to a small D.C.
    # Duty Cycle = D.C. = 100% * (65,536 - TimerValue) / 65, 536
      
    timer_Value = round(-(((percentageInv/100)*65536)-65536))

    if percentage == "100":
        timer_Value = 65534
    
    # PWM Freq set to 195.31 Hz (750K/15/256)
    myUE9.timerCounter(TimerClockBase = 0, TimerClockDivisor = 15, Timer0Mode = 1, NumTimersEnabled = 1, UpdateConfig = 1, Timer0Value = timer_Value)
        
# Top frame elements
header = tkinter.Label(topFrame, text="          Motor Remote Control          ", bg="#88324f", fg= "white", font=("Bold Courier", 24))
ue9IpLabel = tkinter.Label(topFrame, text="Enter UE9 IP:", bg = "#88324f", fg = "white", font=("Bold Courier", 13))
ue9IpBox = tkinter.Entry(topFrame)
direction = tkinter.Label(topFrame, text="Direction:      ", bg = "#88324f", fg = "white", font=("Bold Courier", 13))
state = tkinter.Label(topFrame, text="Motor: OFF  ", bg = "#88324f", fg = "white", font=("Bold Courier", 13))

header.grid(row = 0, columnspan = 2)                        # Show the label and assign it position
ue9IpLabel.grid(row = 2, column = 0, sticky = tkinter.E)    # Sticky will keep label on the righ
ue9IpBox.grid(row = 2, column = 1, sticky = tkinter.E)      # Sticky will keep textbox on the righ
direction.grid(row = 3, sticky = tkinter.E)                 # Sticky will keep label on the righ
state.grid(row = 4, sticky = tkinter.E)                     # Sticky will keep label on the right

# Middle frame elements
speedLabel = tkinter.Label(middleFrame, text="Speed Percentage", bg = "#88324f", fg = "white", font=("Bold Courier", 13))
speedScale = tkinter.Scale(middleFrame, from_ = 1, to = 100, font=("Bold Courier", 13), orient = tkinter.HORIZONTAL, bg = "#88324f", fg="white", length = 400, width = 30, command = motorSpeed) 
turnLeft = tkinter.Button(middleFrame, text="Turn Left", bg = "blue", fg="white", font=("Bold Courier", 14)) 
turnRight = tkinter.Button(middleFrame, text="Turn Right", bg = "blue", fg="white", font=("Bold Courier", 14)) 
speedLabel.grid(row = 0, columnspan = 2, column = 0)        # Show the label and assign it position
speedScale.grid(row = 1, columnspan = 2, padx=5, pady=5)    # Show the label and assign it position
turnLeft.grid(row = 2, column = 0, padx=5, pady=5)          # Show the button and assign it position
turnRight.grid(row = 2, column = 1, padx=5, pady=5)         # Show the button and assign it position
# columnspan will assign 2 cells spance to the width 
# padx=10, pady=10 will add padding to the outer side of the button

# Bottom frame elements
start = tkinter.Button(bottomFrame, text="Turn ON", bg="green", fg="white", font=("Bold Courier", 14), command = powerOn) 
forceStop = tkinter.Button(bottomFrame, text="Emergency Stop", bg="red", fg="white", font=("Bold Courier", 14), command = shutDown) 
bottomLabel = tkinter.Label(bottomFrame, text="      Team F: Abdullah Al-Faraj, Armani Araujo, Manuel Leung Chen      ", fg="white", bg = "#88324f", font=("Bold Courier", 14))
start.grid(row = 0, column = 0, padx=5, pady=5)             # Show the button and assign it position
forceStop.grid(row = 0, column = 1, padx=5, pady=5)         # Show the button and assign it position
bottomLabel.grid(row = 1, columnspan = 2)                   # Show the label and assign it position

# Events with keypress
myWindow.bind("<Left>", dirLeft)  # Call dirLeft method with Left Arrow press
myWindow.bind("<Right>", dirRight)  # Call direRight method with Right Arrow press
myWindow.bind("<Up>", upKeyPress) # Call upKeyPress method with Up Arrow press
myWindow.bind("<Down>", downKeyPress) # Call downKeyPress method with Down Arrow press

# Events with mouese click
turnLeft.bind("<Button-1>", dirLeft)
turnRight.bind("<Button-1>", dirRight)

# GUI Functionalities
    
# Global Variables 
global timer_Value
global confirmation   # Popup window response
global motorState
global fio_state
global myUE9

confirmation = 1
motorState = 0
emergencyPressed = 0

myUE9 = ue9.UE9(ethernet = True, ipAddress = "10.32.89.101")  # Connect to UE9 by its IP address

# Note of FIO pins used on UE9 (FIO-6 = Sensor, FIO-5 = Reset, FIO-4 = Stop, FIOFIO-3 = pinIn1, FIO-2 = pinIn2, FIO-0 = Speed)

myWindow.after(100, pushButtonCheck) # Call pushButtonCheck method as soon as the mainloop starts.

myWindow.mainloop()  # Keep the window form in a loop so it will be open until the X button is press

#Reset the UE9 pins back to OFF after the X button is press   
myUE9.singleIO(1, 2, Dir = 1, State = 0)["FIO2 State"]
myUE9.singleIO(1, 3, Dir = 1, State = 0)["FIO3 State"]
