from java.awt import Color
from java.awt import Robot
from time import time
import random


def SelectFriend():
    print "SelectFriend"
    def _findFriend():
        dragFrom = friendSlotCenter.offset(-500, 240)
        dragTo = friendSlotCenter.offset(-500, 100)
        drag(dragFrom)
        hcm = exists("hcm.png", 0.001)
        apollo = exists("apollo.png", 0.001)
        roy = exists("roy.png", 0.001)

        if apollo:
            dropAt(dragTo)
            click(apollo.getCenter().offset(0, 100))
        elif hcm:
            dropAt(dragTo)
            click(hcm.getCenter().offset(0, 100))
        elif roy:
            dropAt(dragTo)
            click(roy.getCenter().offset(0, 100))
        elif exists("delan_sp.png", 0.001):
            dropAt(dragTo)
            click("delan_sp.png")
        else:
            dropAt(dragTo)
            return False
 
        return True
        
    friendSlot = exists("SelectFriend.png", 0.001)
    if not friendSlot:
        return
    click(friendSlot)
    friendSlotCenter = friendSlot.getCenter()
    
    if not _findFriend():  # drag and drop to second half friends
        dragDrop(friendSlotCenter.offset(-50,240), 
                 friendSlotCenter.offset(-900,240))
        _findFriend()


def ClickStartFighting():
    print "ClickStartFighting"
    if exists("gotofight.png", 30):
        click("gotofight.png")
        wait(1)
        SelectFriend()
        
        wait("gotofight.png")
        click("gotofight.png")
        wait(1)

def DragForward():
    print "DragForward"
    start_time = time()
    clock = exists("clock.png" , 0.001)
    if clock:
        dragFrom = clock.getCenter().offset(100,400)           
        drag(dragFrom)
        hover(Location(dragFrom.x+500, dragFrom.y))
        while not exists("board.png", 1):
            end_time = time()
            time_taken = end_time - start_time # time_taken is in seconds
            if(time_taken >= 30): # not found
                break            #exit while not exists
        print "exists"
        dropAt(Location(dragFrom.x+500, dragFrom.y)) 

   
def ClickFinish():
    print "ClickFinish"
    start_time = time()
    while True:
        finish = exists(Pattern("finish_button.png").similar(0.80),1)
        if finish:
            wait(2)
            click(Pattern("finish_button.png").similar(0.80).targetOffset(26,0))
            break
        end_time = time()
        time_taken = end_time - start_time # time_taken is in seconds
        if(time_taken >= 30): # not found
            break

def PlayDots(color, number, dotLoc, dotColor):
    if number == 1:
        return PlayOneDot(color, dotLoc, dotColor)
    elif number == 2:
        return PlayTwoDot(color, dotLoc, dotColor)
    elif number == 4:
        return PlayFourDot(color, dotLoc, dotColor)
    else:
        return False

def PlayOneDot(color, dotLoc, dotColor):
    for i in range(0, 7):
        if dotColor[i] == color:
            click(dotLoc[i])
            return 1
        elif dotColor[i+7] == color:
            click(dotLoc[i+7])
            return 1
    return 0

def PlayTwoDot(color, dotLoc, dotColor):
    for i in range(0, 7): #verical
        if dotColor[i] == color and dotColor[i+7] == color :
            dragDrop(dotLoc[i], dotLoc[i+7])
            #print "%s, 2" % color
            return 1
    for i in range(0, 6): #horizontal
        if dotColor[i] == color and dotColor[i+1] == color:
            dragDrop(dotLoc[i], dotLoc[i+1])
            #print "%s, 2" % color
            return 1
        if dotColor[i+7] == color and dotColor[i+8] == color:
            dragDrop(dotLoc[i], dotLoc[i+1])
            #print "%s, 2" % color
            return 1
    return 0

def PlayFourDot(color, dotLoc, dotColor):
    for i in range(0, 6): #verical
        if dotColor[i] == color and dotColor[i+1] == color and dotColor[i+7] == color and dotColor[i+8] == color:
            dragDrop(dotLoc[i], dotLoc[i+8])
            #print "%s, 4" % color
            return 1
    return 0


def SimpleAlgo(dotLoc, dotColor):
    for number in (4, 2, 1):   
        for color in ("b", "y", "w"):
            if PlayDots(color, number, dotLoc, dotColor):
                return

def C10_2_Algo(dotLoc, dotColor):
    print "C10_2_Algo"
    if PlayDots("b", 1, dotLoc, dotColor):
        return
    SimpleAlgo(dotLoc, dotColor)

def CheckLost():
    print "CheckLost"
    if exists(Pattern("ok_button.png").similar(0.90), 0.001):
        click(Pattern("ok_button.png").similar(0.90))
        return 1
    return 0

def GetDotBoard():
    print "GetDotBoard"
    if exists(Pattern("ok_button.png").similar(0.90), 0.001):
        return 0, 0, 0
    if not exists(Pattern("soul_normal.png").similar(0.85), 1):
        if not exists(Pattern("soul_dead.png").similar(0.85), 1):
            return 0, 0, 0
    clock = exists("clock.png", 0.001)
    dotLoc = []
    dotLoc.append(clock.getCenter().offset(221,471))
    stepX = 96
    stepY = 99
    for i in range(1, 7):
        dotLoc.append(Location(dotLoc[i-1].x+stepX, dotLoc[i-1].y))
    for i in range(0, 7):
        dotLoc.append( Location(dotLoc[i].x, dotLoc[i].y+stepY))
    dotColor = []
    r = Robot()
    for i in range(0, 14):
        c = r.getPixelColor(dotLoc[i].x, dotLoc[i].y) # get the color object
        if c.getRed() < 150 and c.getGreen() < 150 and c.getBlue() > 200:
            dotColor.append("b")
        elif c.getRed() > 200 and c.getGreen() > 200 and c.getBlue() < 150:
            dotColor.append("y")
        elif c.getRed() > 220 and c.getGreen() > 220 and c.getBlue() > 220:
            dotColor.append("w")
        else:
            dotColor.append("?")
        #crgb = ( c.getRed(), c.getGreen(), c.getBlue() ) # decode to RGB values
        #print dotColor[i]
    return 1, dotLoc, dotColor
        
def PlayDrag():
    print "PlayDrag"
    if not exists("clock.png" , 0.001):
        return
    while True:
        isFound, dotLoc, dotColor = GetDotBoard()
        if not isFound:
            break
        C10_2_Algo(dotLoc, dotColor)
        #SimpleAlgo(dotLoc, dotColor)
        wait(1)


def main():
    for i in range(100):
        isFailed = False
        print i
        ClickStartFighting()
        wait("clock.png", 20)
        while exists("clock.png" , 0.001):
            DragForward() 
            wait(1)
            PlayDrag()
            if CheckLost():
                isFailed = True
                print "lost"
                wait(5)
                break
        if not isFailed:
            ClickFinish()
    
if __name__ == "__main__":
    #ClickFinish()
    main()

    
