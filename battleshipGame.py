
# Student name: Manuel Leung Chen
# Student number: 117-586-156
# Section: NAAL
# Due Date: October 15, 2018
#Instructor name: Danny Abesdris
#Purpose: Create a Battleships Game 

# STUDENT OATH:
# -------------
#
# "I declare that the attached project is wholly my own work in accordance
# with Seneca Academic Policy. No part of this project has been copied
# manually or electronically from any other source (including web sites) or
# distributed to other students."
#
# Name: Manuel Leung Chen  Student ID: 117-586-156

#Assigment #1. Python Battleship...
import random 
import time

#playBattleship
#+ Calls all other functions below
def playBattleship():
    
    missilesAway = 0
    missilesLeft = 50
    Score = 0
    result = 0
    hitCount = 0
    
    initGame(missilesLeft, missilesAway, Score, "00")  #This will call drawGame and loadShips  
    playMode = ""   
    while playMode != "n" and playMode != "y":
        playMode = input("Would you like the PC to auto-play?[Y/N]").lower()
       
    while Score < 160 and missilesLeft > 0:  #Keep playing until Win or Lose 
        #Automated Play MODE
        if playMode == "y":
            #input('Press enter to continue: ')
            time.sleep(2)      # 2 seconds delay
            if result == 0:
                playerMove = randomPCmove()  
            else:                #Check for first hit on a Ship
                
                        # Convert Left Coordinate back to an int                
                leftNextmove = alphaNumToInt(playerMove[0])
                        
                        # Convert Right Coordinate back to an int
                rightNextmove = alphaNumToInt(playerMove[1])
                
                if board[leftNextmove][rightNextmove] == "[":
                    # Keep hitting to the Right                 
                    if hitCount != 0:
                        rightNextmove += hitCount + 1
                        hitCount = 0
                    else:
                        rightNextmove += 1
                    
                    newLeft = alphaNumConversion(leftNextmove)
                    newRight = alphaNumConversion(rightNextmove)                               
                    playerMove = str(newLeft + newRight)                      
                
                elif board[leftNextmove][rightNextmove] == ">":
                    # Check if it is last segment of ship 
                    try:              
                        LeftHitChecker = alphaNumConversion(leftNextmove)
                        RightHitChecker = alphaNumConversion(rightNextmove - 1)
                        hitRecord[LeftHitChecker + RightHitChecker]  
                        # Select another random Num
                        playerMove = randomPCmove()                
                        leftNextmove = alphaNumToInt (playerMove[0])
                        rightNextmove = alphaNumToInt (playerMove[1])  
                        print("tet")
                        
                    # Keep hitting to the Left     
                    except KeyError:
                        rightNextmove -= 1
                                                                
                    newLeft = alphaNumConversion(leftNextmove)
                    newRight = alphaNumConversion(rightNextmove)
                                
                    playerMove = str(newLeft + newRight)
                    
                else:
                    # Keep hitting to the Right                    
                    try:
                        LeftHitChecker = alphaNumConversion(leftNextmove)
                        RightHitChecker = alphaNumConversion(rightNextmove - 1)
                        hitRecord[LeftHitChecker + RightHitChecker]                      
                        rightNextmove += 1
                    # Keep hitting to the Left     
                    except KeyError:
                        rightNextmove -= 1
                        hitCount += 1
                      
                    newLeft = alphaNumConversion(leftNextmove)
                    newRight = alphaNumConversion(rightNextmove)

                    playerMove = str(newLeft + newRight)           
                  
        # Manual MODE
        else:
            playerMove = input("Enter Target Coordinates-->  ").upper()
    
        target = checkMove(playerMove) 
    
        if target == 0:
            print("The coordinates you ented are not on the board.")
            print("Please try another move.")
        else:
            result = UpdateData(playerMove)
            if result == 1:
                missilesLeft -= 1
                missilesAway += 1
                Score += 5
                              
                drawGame(missilesLeft, missilesAway, Score, playerMove)
            else:
                missilesLeft -= 1
                missilesAway += 1
                drawGame(missilesLeft, missilesAway, Score, playerMove)
                            
    # Game ended
    if Score == 160:
        print("Congrats! You WON!")
    elif missilesLeft == 0:
        print("YOU LOSE")
        
#initGame
def initGame(missilesLeft, missilesAway, Score, lastMove):  #This will call drawGame and loadShips 
    
    drawGame(missilesLeft, missilesAway, Score, lastMove)   #This function print the board
    loadShips()  #This function load ships and coordinates to a dictionary 
    
#drawGame  
def drawGame(missilesLeft, missilesAway, Score, lastMove):  
    ## Print the labels of the board
    alphaAddcol = 65
    i = 1
    j = 1

    print("   Python Battleship . . .")
    print("  ", end=" ")
    for j in range(column):   # Print Header Nummbers
        if j <9:
            print(j + 1, end=" ")
        else:
            print(chr(alphaAddcol), end=" ")
            alphaAddcol += 1
    print()

    alphaAdd = 55
    
    # Print the board layout
    for row in board:
        if i < 10:
            print(i, "|", end="")
            i += 1
        
        else:
            print(chr(i + alphaAdd), "|", end="")
            alphaAdd += 1
        print(' '.join(row), end="")  # Print the "~" rows
        print("|")
    
    print("Missiles Away:", str(missilesAway).zfill(2), "   Missiles Left:", str(missilesLeft).zfill(2))
    print("Current Score:", str(Score).zfill(3), "  Last Move:", lastMove)
    
#loadShips
#+ Randomly places all 'ships' onto the board making sure that the ship will
#  "fit" on a single row starting at a specific coordinate.
#[CCCCCCC=> (an aircraft carrier) (10 chars)
#[BBBBB=>   (a battle cruiser) (8 chars)
#[DDD=>     (a destroyer) (6 chars)
#[SS=>      (a submarine) (5 chars)
#[F>        (a frigate) (3 chars)
def loadShips():
    
    shipSizeList = [3,5,6,8,10]
    shipsRow = []
    # Generate random location coordinates for 5 ships
    for indexShip in list((shipSizeList)):  #indexShip start with "3"
        count = 0
        while count < 1:
            randRow = random.randint(1,row) 
            if randRow not in shipsRow:     #Verify that each ships is on diff. row
                shipsRow.append(randRow)
                count += 1
        randCol = random.randint(1,column-(indexShip-1)) 
        
        #show locations      
        for shipSeg in range (indexShip):  #start from 0 to indexShip=3    
            left = ""
            right = ""         
 
            # Convert "randRow" and "randCol" into string                 
            left = intToAlphaNum(randRow)                          
            right = intToAlphaNum(randCol)
            randCol += 1
          
            # Assign Chars from lower to higher col index    
            if shipSeg == 0:
                coordinates[left + right] = "["        
            elif ((shipSeg + 2) == indexShip) and indexShip != 3:
                coordinates[left + right] = "="            
            elif (shipSeg + 1) == indexShip:
                coordinates[left + right] = ">"               
            else:     
                if indexShip == 3:
                    coordinates[left + right] = "F"
                elif indexShip == 5:
                    coordinates[left + right] = "S"
                elif indexShip == 6:
                    coordinates[left + right] = "D"
                elif indexShip == 8:
                    coordinates[left + right] = "B"
                elif indexShip == 10:
                    coordinates[left + right] = "C"
    #Show Ships location
    #print(coordinates)
    
#checkMove
#+ Validates the player's coordinate input (you must accept player's input as a
#  string only) and sends back the numeric index that the coordinate 
#  corresponds to or the value -1 if the coordinate entered is in any way invalid.
#  For example, if 'coord' is "11", checkMove would return 0
# (first column of first row), "12"->1, "13"->2, etc.

def checkMove(playerInput):     # Verify that player move is in board range 
    
    try:        
        coordinates[playerInput]  #cheack if there is a matching key
        return 1             
    except KeyError:
        return 0                    # Coordinates ouside the board
    
#updateData
#+ After a player chooses a valid coordinate, this
#  function updates the 'board' by placing either an 'X' (for a miss)
#  or revealing a ship's character (for a hit). 
def UpdateData(playerInput):  
    
    # Convert Left Coordinate back to an int 
    left = alphaNumToInt(playerInput[0])
        
    # Convert Right Coordinate back to an int
    right = alphaNumToInt(playerInput[1])
  
    # Reveal value on board
    if coordinates[playerInput] == "0":   
        board[left][right] = "X"
        return 0          # Update data to battleShip()
    
    else:      
        try:
            hitRecord[playerInput]   #Prevent hitting the ship segment twice
            return 0              # Ship was already hit here. no extra ponts
                
        except KeyError:         
            hitRecord[playerInput] = 1          # Save hit to hitRecord
            board[left][right] = coordinates[playerInput]
            return 1          # Send update data to battleShip()

#Extra function
def randomPCmove ():
    
    randRowPC = random.randint(1,row) 
    randColPC = random.randint(1,column)       

    leftPCmove = ""
    rightPCmove = ""
               
    # Convert "randRowPC" and "randColPC" into string   
    leftPCmove = intToAlphaNum(randRowPC)                   
    rightPCmove = intToAlphaNum(randColPC)
 
    return leftPCmove + rightPCmove

# Convert Next AI move back to Alpha-Num
def alphaNumConversion (oldMove):
    
    if oldMove < 9:
        newMove = str(oldMove + 1)
    else:
        newMove = chr(oldMove + 56)    
             
    return newMove 

# Convert Int to Alpha-Num
def intToAlphaNum (oldMove, addValue = 55):
    
    if oldMove < 10:
        newMove = str(oldMove)
    else:
        newMove = chr(oldMove + addValue)    
             
    return newMove 

# Convert Alpha-Num to Int
def alphaNumToInt (playerInput):
    
    try:
        newMove = int(playerInput) - 1
    except ValueError:
        newMove = ord(playerInput) - 56  
    
    return newMove
    
# Main Function
    
random.seed() #without value, random will use the system clock

column = random.randint(10,35) #includes 35
row = random.randint(10,35) #includes 35

coordinates = {} # Stores all coordinates of board as Keys
hitRecord = {}     #Store previous ship hits

#board = [["~" for x in range(column)] for y in range(row)] 
# Another way to create 2-dimensional array
board=[]
for i in range(row):
   board.append(["~"] * column)
   
# Add coordinate as keys with "0" value
leftcoor = ""
rightcoor = ""
alphaleft = 65

for i in range(row):    # Convert "i" and "j" into string
    if i < 9:           
        leftcoor = str(i + 1)
    else:
        leftcoor = (chr(alphaleft))
        alphaleft += 1
    alpharight = 65

    for j in range(column):    
        if j < 9:
            rightcoor = str(j + 1)
        else:
            rightcoor = (chr(alpharight))
            alpharight += 1
            
        coordinates[leftcoor + rightcoor] = "0" 
     
playBattleship()        # Start the Game





    










