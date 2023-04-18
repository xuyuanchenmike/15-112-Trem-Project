from cmu_graphics import *
import math,copy
import random

class Bee: 
    def __init__(self,x,y): 
        self.x=x
        self.y=y
    def drawPlayer(self):
        drawCircle(self.x,self.y,25,fill="orange")
    def playerOnStep(self,app):
        self.x=app.cursorX
        self.y=app.cursorY

class Pollinator:
    pollinatorList=[]
    gathered=[]
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.color=random.choice(["red","blue","green","purple"])
        self.gathered=False
        self.pollenGathered=0
        Pollinator.pollinatorList.append(self)
    def drawPollinator(self):
        drawCircle(self.x,self.y,15,fill=self.color)
    def isClose(self,other):
        if distance(self.x,self.y,other.x,other.y)<=40:  
            return True
        else: 
            return False
    def gatheredState(self,app):
        #for pollinator in Pollinator.pollinatorList:
            if self.isClose(app.player) and\
                self not in Pollinator.gathered:
                Pollinator.gathered.append(self)
                return True
    def pollinatorOnStep(self):
        self.y-=10

class Flower:
    flowerList=[]
    gathered=[]
    def __init__(self,x,y,width,height,color):
        self.x=x
        self.y=y
        self.width=50
        self.height=50
        self.color=random.choice(["red","blue","green","purple"])
        Flower.flowerList.append(self)
    def drawFlower(self):
        drawRect(self.x,self.y,self.width,self.height,fill=self.color,\
                 align="center")
    def isClose(self,other):
        if distance(self.x,self.y,other.x,other.y)<=self.width+15 or\
        distance(self.x,self.y,other.x,other.y)<=self.height+15:
            return True
        else: 
            return False
    def pollinatedState(self,app):
        #for flower in Flower.flowerList:
            if self.isClose(app.player) and\
                self not in self.gathered:
                Flower.gathered.append(self)
                return True
    def flowerOnStep(self):
        self.y-=10

def onAppStart(app):
    app.stepsPerSecond=25
    app.stepTimeCounter=0
    app.width=800
    app.height=800
    app.cursorX=200
    app.cursorY=200
    app.player=Bee(200,200)
    app.numOfPollen=0
    app.pollen=[]

def redrawAll(app):
    drawRect(400,400,800,800,fill="cyan",align="center")
    app.player.drawPlayer()
    for flower in Flower.flowerList: 
        flower.drawFlower()
    for pollinator in Pollinator.pollinatorList:
        pollinator.drawPollinator()
    for (cx,cy,color) in app.pollen:
        drawCircle(cx,cy,10,fill=color)

def onMouseMove(app,mouseX,mouseY):
    app.cursorX=mouseX
    app.cursorY=mouseY 
                
def onStep(app):
    app.stepTimeCounter+=1
    app.player.playerOnStep(app)
    if app.stepTimeCounter%50==0:
        Pollinator(random.randrange(800),800,"pink")
        Flower(random.randrange(800),800,50,50,"blue")
    for pollinator in Pollinator.pollinatorList:
        if pollinator.gatheredState(app):
            app.numOfPollen+=1
            numOfPollen=app.numOfPollen
            app.pollen.append((25+20*numOfPollen,25,\
                               pollinator.color))
              
    for flower in Flower.flowerList: 
        if flower.pollinatedState(app):
            if app.pollen!=[]:
                app.pollen.pop()
                app.numOfPollen-=1
                
    for pollinator in Pollinator.pollinatorList:
        pollinator.pollinatorOnStep()
    for flower in Flower.flowerList: 
        flower.flowerOnStep()

def distance(x1,y1,x2,y2): 
    return ((x1-x2)**2+(y1-y2)**2)**(1/2)

def main():
    runApp()

main()