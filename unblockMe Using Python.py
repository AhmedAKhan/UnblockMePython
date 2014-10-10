# Course: CS 1MD3
# Name:  Ahmed Khan
# File: assgn4.py
# Description: This file creates a simple unblock me game which the user can play, The objective of the game is to get the red block to the other side,
#   When the block goes to the other side, it will blink 3 times and the window will close.

#   there is a comment explaining what each line does but there is also a description of the structure of the entire code at the bottem of the page


#imports the necessary classes
from graphics import *
import math
import time

#this is a global variable
#it represents the position of the top left cordinate of the grid
#everything in the code will be represented relative to this
originX = 20
originY = 20

#this function just draws the border (the gray part) of the game.
#it takes in the x and y positions of grid and the window to where it will draw the border
def makeBorder(x, y, window):    
    #this just creates a gray rectangle that covers the grid as well as the border
    #and then draws another white rectangle that covers the grid area
    #and then draws another little rectangle to draw the exit door 
    shadowRect = Rectangle(Point(x-8, y-8), Point(x+248,y+248))
    whiteRect = Rectangle(Point(x, y), Point(x+240, y+240))
    exitDoor = Rectangle(Point(x+240, y+80), Point(x+268, y+120))

    #this just sets the color of all the componenets    
    shadowRect.setFill('gray')
    exitDoor.setFill('white')
    exitDoor.setOutline('white')
    whiteRect.setFill('white')

    #draws it onto the frame
    shadowRect.draw(window)
    whiteRect.draw(window)
    exitDoor.draw(window)
    return

#this function just makes the grid lines, it takes in the x and y positions of the starting of the grid and the object to where it will draw the object
def makeTheGrid(x,y, window):
    #starts a for loop that runs 5 times, because there are 5 lines horizontally and vertically
    for c1 in range(1,6,1):
        #draws the horizontal Lines
        horizontalLines = Line(Point(x,y+c1*40),Point(x+240,y+c1*40))
        horizontalLines.setWidth(1)
        horizontalLines.setFill('gray')
        horizontalLines.draw(window)

        #draws the vertical lines
        verticalLines = Line(Point(x+c1*40,y), Point(x+c1*40, y+240))
        verticalLines.setWidth(1)
        verticalLines.setFill('gray')
        verticalLines.draw(window)
    return

#sets up the game by initiallizing the variables, calls the functions that draws the field
#and draws all the blocks onto the field as well
def setupGame():
    #creates the window
    window = GraphWin('unblock me', 280, 280)

    #make the border
    makeBorder(originX, originY, window)    
    
    #make the fields array
    fields = []
    for i in range(37):
        fields.append([])
    
    #make the block object from the class and stores it into the fields array
    counter = 0
    for i in  [[1, 3, True], [6, 3,False], [9, 3, False],[13, 2,True, 'r'],[19, 2, False],[23, 2, True],[29, 2,False],[31, 3, True]]:
                                            #fid, length, orien, color
        if len(i) == 3:
            b = Block(originX, originY, window, i[0], i[1], i[2], 'brown', counter)
        else:
            b = Block(originX, originY, window, i[0], i[1], i[2], 'red', counter)
        counter += 1
        b.draw()
        if i[2] == True:
            for j in range(i[1]):
                fields[j+i[0]] = b
        else:
            for j in range(i[1]):
                fields[j*(6)+i[0]] = b
                
    #just starts the game
    #printList(fields)
    makeTheGrid(originX, originY, window)#makes the grid ontop of the blocks
    startGame(fields, window)
    return

#this function takes in the fields array and the window where the game is setup and then starts up the game
def startGame(fields, window):
    #initializes variables
    isHilighted = False
    lastObjectClicked = []

    #creates a loop which runs the game 
    while True:
        #waits for mouse to click
        try:
            mouseClick = window.getMouse()
        except:
            print('you lose the game')
            return
        fieldIdClicked = convertPointToFid(mouseClick)#converts the point to a fieldId
        
        #checks if a block is highlighted if it is then it moves the block to the new position if that new position is valid
        #if it is not hilighted then if you clicked a block it just highlights it
        if isHilighted:
            #moves the block to the new location
            #if the new location is not valid it will move it to back to the same place
            lastObjectClicked.move(fieldIdClicked, fields)

            #makes the object unhilighted
            isHilighted = False
            lastObjectClicked.unhilite()

            #checks if u won the game, if you have then it blinks the block 3 times and then
            #closes the window
            if lastObjectClicked.fid == 17 and lastObjectClicked.isHorizontal:
                for i in range(6):
                    if i%2 == 0:
                        lastObjectClicked.hilite()#swithces the highlight of the block
                    else:
                        lastObjectClicked.unhilite()
                    makeTheGrid(originX, originY, window)
                    time.sleep(0.5)#waits for 0.5 seconds
                    
                window.close()#closes the window
                print('the game has ended you have won')#ends the game
                return
        elif str(fields[fieldIdClicked]) == 'b':
            #highlights the nwe blocked clicked, and sets the variables accordingly
            fields[fieldIdClicked].hilite()
            lastObjectClicked =fields[fieldIdClicked] 
            isHilighted = True
            
        makeTheGrid(originX, originY, window)
    return

#this function takes in a point and returns the field Id it belongs to
def convertPointToFid(point):
    #if does this by converting the x and y coordinates to intervals of 40, then checks if the click is inside the grid
    #then the field id is equal to  x + y*6 + 1 because as you go 1 block lower the field id increases by 6. and since the block starts at 1 instead of 0 it just adds 1 more
    x = (point.getX() - originX)//40
    y = (point.getY() - originY)//40
    if x > 5 or y > 5:
        return 0
        
    fid = y*6 + x + 1
    return fid

#this is the start of the block class
#the details of the class block is explained at the bottem of the code
# --------------------------class Block --------------------------------------------------------
class Block:
    # x and y are coordinates of the top left corner of the first field
    # win is the window handle
    # fid is the field id of the first square of the block
    # length is the number of squares the block spans (i.e. 2 or 3)
    # orienIsHorizontal indicates orientation (i.e. horizontal or vertical) True = horizontal, False = vertical
    # color is the color of the block
    # identifier is a number given from 0 - 8(number of blocks) which help with debugging and finding errors, incase if the program stops working

    #this function just represents the block as a string, which is represented by the character b
    def __str__(self):
        return "b" 

    #this is the function that is called when the object is first created
    def __init__(self, x, y, win, fid, length, orienIsHorizontal, color, identifier):
        #constructor code

        #first initialize all the variables
        self.originX = x
        self.originY = y
        self.win = win
        self.length = length
        self.color = color
        self.highlights = []
        self.fid = fid
        self.identifier = identifier
        self.borderColor = 'black'
        position = self.fieldIDToPosition(fid)
        self.x = position[0]
        self.y = position[1]

        self.isHorizontal = orienIsHorizontal

        #sets thex and y co-ordinates        
        x = self.x + self.originX
        y = self.y + self.originY
    #end __init__

    #this function just draws the block onto the window
    def draw(self):
        #clears the object and recreates it
        self.objects = []
        
        #declares and initializes variables
        xLength = 1
        yLength = 1

        #sets the horizontal and vertical length
        if self.isHorizontal:
            xLength = self.length
        else:
            yLength = self.length

        #defines the x and y co-ordinate
        x = self.x + self.originX
        y = self.y + self.originY

        #creates the object block
        borderWidth = 3
        self.objects.append(Rectangle(Point(x,y), Point(x+40*xLength,y+40*yLength)))
        self.objects.append(Rectangle(Point(x + borderWidth, y+borderWidth), Point(x+40*xLength - borderWidth,y+40*yLength - borderWidth)))

        #colors the block and draws it onto the stage
        self.objects[0].setFill('black')
        self.objects[1].setFill(self.color)
        self.objects[0].draw(self.win)
        self.objects[1].draw(self.win)
        return

    #removes the object from the field
    def undraw(self):
        for i in self.objects:
            i.undraw()
    #end undraw

    #when called the object becomes hilited
    #this works by making the oultine of it green
    def hilite(self):
        self.objects[0].setFill('green')
        self.objects[0].setOutline('green')
        self.borderColor = 'green'
        return
    #end hlite

    #unhilites the block
    def unhilite(self):
        self.objects[0].setFill('black')
        self.objects[0].setOutline('black')
        self.borderColor = 'black'
    #end unhilite
    
    def switchHilite(self):
        if self.borderColor == 'black':
            self.hilite()
        else:
            self.unhilite()
        return
    
    # move the block to new target, the target is the new Field id that the top left position should be in
    # fields is the list which stores the position of all the objects
    # after the move, the block is in unhilited
    def move(self,target, fields):
        #it checks if the move is valid, if it is not valid it returns 0 for not valid and if it is close to being valid it makes it vaid
        newFieldID = self.checkTargetIsValid(fields, target, self.fid)
        if newFieldID == 0:
            return

        #this function checks to see if the position where you want to go is being filled with any other block
        #if it is filled with another position then it will adjust self.fid accordingly
        self.updateField(fields, self.fid, newFieldID)
        newPosition = self.fieldIDToPosition(self.fid)
        self.x = newPosition[0]
        self.y = newPosition[1]

        #this will unhilite and draw the block with the new attributes
        self.unhilite()
        self.undraw()
        self.draw()
        return

    #this function is called with the arguments self, fields which is the list which stores the current positions of all the blocks, and the new and old position
    #of the block, This function checks to see if the new position is filled with another block, if it is it makes the new position of the block its old position
    #if it is not then it undates the fields list by putting the new position of the block into the list
    def updateField(self, fields, oldFieldId, nfid):
        #declares and initializes the variable
        if self.isHorizontal:
            multiplier = 1
        else:
            multiplier = 6

        #removes the block from the old postion of the fields list
        for i in range(self.length):
             fields[oldFieldId + i*multiplier] = []

        #decalres and initializes more variables
        newFieldId = nfid
        counter = 0
        counterIncrementer = 1
        if newFieldId < oldFieldId:
            counterIncrementer = -1

        #checks every single position of your current position and the position you are trying go to        
        while True:
            #checks if that field is empty, if it not then it sets the new position of the block to the position before this
            if not self.checkIfFieldIDIsEmpty(fields, oldFieldId+counter*multiplier):#if it is not empty
                newFieldId = oldFieldId+(counter - counterIncrementer)*multiplier
                break

            #if this is the position of the block you want to be in then it ends the loop
            counter += counterIncrementer 
            if counterIncrementer == 1:
                if newFieldId < oldFieldId+counter*multiplier:
                    break
            elif newFieldId > oldFieldId+counter*multiplier:
                break
                    
        #updates the fields list so that the block is stores in the correct position
        for i in range(self.length):
            fields[newFieldId + i*multiplier] = self

        #makes the class variable field id become equal to the local variable newFieldId
        self.fid = newFieldId
        #printList(fields)
        return

    #this checks if the position you want to go to is valid
    #if the block is horizontal and the new position is in the same row then it is valid
    #and if the block is vertical and the new position is in the same column the new position is valid
    #the newFieldID represents the top left position of the block
    #if you choose for example the bottem right position for a vertical block, then the rest of the block will be outside the field
    #so it will adjust the new position so the block will not go outside the boundry
    def checkTargetIsValid(self, fields, newFieldId, currentFieldId):
        currentFieldId -= 1
        newFieldId -= 1
        if self.isHorizontal:
            #find the row number this is at
            if currentFieldId //6 == newFieldId//6: #checks if its in the same row
                if currentFieldId//6 == (newFieldId + self.length-1)//6:#check that the length doesnt make it go outside the edge
                    return newFieldId + 1
                return (currentFieldId//6 + 1)*6 - self.length + 1
        
        else:#the block is vertical
            if newFieldId%6 == currentFieldId%6:#check the block is in the same column
                if newFieldId < 0 :#if the lenth causes the block to be above or below the grid then adjust the new position
                    return 0
                elif newFieldId//6 +self.length > 6:
                    return (newFieldId%6)+(6-self.length)*6 + 1
                else:
                    return newFieldId + 1 #if it is not then just return the position, since we subtracted one earlier we have to add one now
                
        return 0#

    #this function just converts the field ID to a position, it is used to draw the block
    def fieldIDToPosition(self, fid):
        fid -= 1
        y = (fid//6)*40
        x = (fid%6)*40
        return (x, y)

    #checks if the field id is empty, it returns true or false, and is given the fields list, and the new field id to check
    def checkIfFieldIDIsEmpty(self, fields, newFieldId):
        #declares and initializes variables
        if self.isHorizontal:
            multiplyingFactor = 1
        else: # it is vertical
            multiplyingFactor = 6

        #checks if the block is currently located at that position OR located in the next 2 or 3 locations depending on its length
        for i in range(self.length):
            if str(fields[newFieldId + i*multiplyingFactor]) == 'b':
                return False
        return True
    #end move
#end class Block ------------------------------------------------------


#this is just a function that prints out the list fields in a manor which is easier to see and evaluate.
#If you want to see how the fields list changes as the game is played, just uncomment the lines that call this function
def printList(fields):
    print('[')
    for i in range(0,6,1):
        for j in [1,2,3,4,5,6]:
            if str(fields[j+i*6]) == 'b':
                print('b'+str(fields[j+i*6].identifier) + ', ' ,end = '\t')
            else:
                print('e0 , ', end = '\t')
            
        print()
    print(']')

setupGame()


'''
this is how the fields list works

it is a list which is initialized like this
[
b0, 	b0, 	b0, 	e0 , 	e0 , 	b1, 	
e0 , 	e0 , 	b2, 	e0 , 	e0 , 	b1, 	
b3, 	b3, 	b2, 	e0 , 	e0 , 	b1, 	
b4, 	e0 , 	b2, 	e0 , 	b5, 	b5, 	
b4, 	e0 , 	e0 , 	b6, 	e0 , 	e0 , 	
b7, 	b7, 	b7, 	b6, 	e0 , 	e0 , 	
]
(it is not a 2d list, it is a simply list with 36 elements)

the elements of the list are either empty or it is an instance of the block object. there are 8 objects in the game.
Each object is stored inside the fields list multiple times depending on its length. the position of the object in the list represents where it will be
on the window. The representation is the same as assignmnet 3, where the id starts at 1, and increases horizontally.
each block has an identifier, that was just to make debugging easier, to tell which block is stored where.

the block itself is stored inside the object list in the block object. the object list has 2 items inside it. one is the large rectangle and the second is
the smaller rectangle. The smaller rectangle is the actual block you see with the brown or red color and thelarger rectangle is the black part you see, which
turns green when pressed
'''
