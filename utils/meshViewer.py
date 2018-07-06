

from OpenGL.GL import *  # pylint: disable=W0614
from OpenGL.GLUT import *  # pylint: disable=W0614

import glm
from glutWindow import GlutWindow
from MVPControl import MVPController
from utils.shaderLoader import Shader


class MeshViewWindow(GlutWindow):


    def init_opengl(self):
        glClearColor(0.1, 0.1, 0.1, 0.8)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        #glEnable(GL_CULL_FACE)

    def add_mesh(self,meshObj):
        self.meshes.append(meshObj.makeContext())

    def init_context(self):        
        self.meshes = []
        

    def calc_MVP(self,width=0,height=0):
        
        if(width!=0):
            self.controller.resize(width,height)        
        self._MVP = self.controller.calcMVP(glm.mat4(1.0)) 
        self.MVPPtr = glm.value_ptr(self._MVP)

    def resize(self,Width,Height):  
        print "resize"      
        glViewport(0, 0, Width, Height)
        self.calc_MVP(Width,Height)

    def ogl_draw(self):     
        print "draw"    
        self.calc_MVP()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for mesh in self.meshes:
            mesh.rendering(self.MVPPtr)
    def processMenuEvents(self,*args,**kwargs):
        action, = args

        if(action == 3):
            self.controller.reset()
            self.update_if() 
        if(action == 2):
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
            self.update_if()
        if(action == 4):
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)    
            self.update_if()        
        return 0

    def init_default(self):
        from worldsheet import worldSheet
        self.controller = MVPController(self.update_if)
        self.init_opengl()
        self.init_context()    
        self.add_mesh(worldSheet())
        self.menu = glutCreateMenu(self.processMenuEvents)
        glutAddMenuEntry("UV MAP",1)
        glutAddMenuEntry("WireFrame Mode",2)
        glutAddMenuEntry("GL_FILL Mode",4)
        glutAddMenuEntry("Reset View",3)
        glutAttachMenu(GLUT_RIGHT_BUTTON)
        return self


class meshWithRender(object):

    def makeContext(self):
        self.loadShader()
        self.loadObject()
        self.loadTexture()
        return self
    def loadShader(self):
        self.shader = Shader()
        
    def loadObject(self):
        self.mesh = None
        print "Make and fill OPENGL buffers,vertex,uv,normal,trangent,indices"
    def loadTexture(self):
        self.texture = None
        print "No texture for this object"
    
    def rendering(self):
        print "override rendering process"
        pass
