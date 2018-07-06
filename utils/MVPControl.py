

import glm
import math
class MVPControl:

    def __init__(self,width=800,height=480,*args,**kwargs):

        self.ScreenWidth = width
        self.ScreenHeight = height
        self.reset()
        
    def reset(self):

        #Initial position : on +Z
        self.position = glm.vec3(5,5,5)
        #Initial horizontal angle : toward -Z
        self.horizontalAngle = 4
        #Initial vertical angle : none
        self.verticalAngle = - 0.6
        # Initial Field of View
        self.Fov = 60.0
        self.computeMatrices()

    def moveFoward(self,foward):
        self.position += self.direction*foward
        self.computeMatrices()
    def moveUp(self,up):    
        self.position += self.up*up
        self.computeMatrices()
    def moveRight(self,right):    
        self.position += self.right*right 
        self.computeMatrices()  
    def lookUpward(self,yaw):
        self.verticalAngle += yaw
        self.computeMatrices()  
    def turn(self,angle):
        self.horizontalAngle += angle
        self.computeMatrices()  
    #calc direction right and up
    def computeMatrices(self):
        self.direction = glm.vec3(math.cos(self.verticalAngle) * math.sin(self.horizontalAngle), 
                        math.sin(self.verticalAngle),
                        math.cos(self.verticalAngle) * math.cos(self.horizontalAngle)
                        )
        self.right =  glm.vec3(
            math.sin(self.horizontalAngle - 3.14/2.0), 
            0.0,
            math.cos(self.horizontalAngle - 3.14/2.0 )
            )
        self.up = glm.cross(self.right,self.direction)

        self.lookPos = self.position+ self.direction

        self.ProjectionMatrix = glm.perspective(glm.radians(self.Fov), float(self.ScreenWidth) / float(self.ScreenHeight), 0.1, 1000.0)
        
        self.ViewMatrix = glm.lookAt(self.position,           # Camera is here
                                     self.lookPos, # and looks here : at the same position, plus "direction"
                                     self.up                       # Head is up (set to 0,-1,0 to look upside-down)
                            )
    def resize(self,width=0,height=0):
        self.ScreenWidth = width
        self.ScreenHeight = height
        self.computeMatrices()

    def calcMVP(self,modelMaterix):

        #print self.position
        #print self.horizontalAngle,self.verticalAngle
        return self.ProjectionMatrix * self.ViewMatrix * modelMaterix                                  

def dummyUpdate():
    print "please implement update"
class MVPController(MVPControl):

    def __init__(self,updateCallback=dummyUpdate,*args,**kwargs):
        self.updateCallback =updateCallback
        MVPControl.__init__(self,*args,**kwargs)
        self.mouse_mode  = -1
        self.lastX =0 
        self.lastY =0 
    def on_special_key(self,key,x,y):  
        print key
        _key = key   
        if(_key==104): #page down
            self.moveUp(1.0) 
            self.updateCallback()
        elif(_key==105):
            self.moveUp(-1.0) #page up
            self.updateCallback()
        elif(_key==101):#up
            self.lookUpward(0.1)
            self.updateCallback()
        elif(_key==103):#down
            self.lookUpward(-0.1)
            self.updateCallback()             
        elif(_key==102):#right
            self.turn(0.1) 
            self.updateCallback()
        elif(_key==100): #left
            self.turn(-0.1) 
            self.updateCallback()  

    def on_keyboard(self,key,x,y):     
        _key = key.lower()
        if(_key=='w'):
            self.moveFoward(0.5) 
            self.updateCallback()
        elif(_key=='s'):
            self.moveFoward(-0.5)
            self.updateCallback()
        elif(_key=='a'):
            self.moveRight(-0.5) 
            self.updateCallback()
        elif(_key=='d'):
            self.moveRight(0.5)
            self.updateCallback()        
   
              
    def on_mouse(self,*args,**kwargs):

            (key,Up,x,y) = args
            if((key==0) & (Up == 0)):
                self.lastX = x
                self.lastY = y
                self.mouse_mode = 1
            elif((key==2) & (Up == 0)):
                self.lastX = x
                self.lastY = y
                self.mouse_mode = 2  
        
            else:
                self.lastX = -1
                self.lastY = -1    
                self.mouse_mode = -1           
            #print "please overrider on_mousemove" ,args
    def on_mousemove(self,*args,**kwargs):
            deltaX = self.lastX - args[0]
            deltaY = self.lastY - args[1]
            if(self.mouse_mode==1):
                (self.lastX,self.lastY) = args
                self.lookUpward(deltaY*0.01)
                self.turn(deltaX*0.01)
                self.updateCallback()
            elif(self.mouse_mode==2):
                (self.lastX,self.lastY) = args
                #self.lookUpward(deltaY*0.01)
                #print "."
                self.moveUp(-0.5*deltaX) #page up
                self.updateCallback()                
            #print "please overrider on_mousemove" ,args