from OpenGL.GL import * # pylint: disable=W0614

import glm
from meshViewer import meshWithRender

from .shaderLoader import Shader


class worldSheet(meshWithRender):

    def loadShader(self):
        self.shader = Shader()
        self.shader.initShaderFromGLSL(["glsl/utils/worldsheet/vertex.glsl"],["glsl/utils/worldsheet/fragment.glsl"])
        self.MVP_ID   = glGetUniformLocation(self.shader.program,"MVP")
        
    def loadObject(self):

        lineX = []#[-10.0,0.0,0.0]+[10.0,0.0,0.0]
        lineY = []# [0.0,10.0,0.0]+[0.0,-0.0,0.0]
        lineZ = []#[0.0,0.0,-10.0]+[0.0,0.0,10.0]


        for i in range(-10,11):
            fi = float(i)
            lineX.extend([-10.0,0.0,fi]+[10.0,0.0,fi])
            lineY.extend([fi,0.0,-10.0]+[fi,0.0,10.0])
        
        lineX.extend(lineY)
        #print lineX
        lineX.extend(lineZ)
        self.lines = lineX
        #print len(self.lines)
        self.linebuffer  = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.linebuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(self.lines)*4,(GLfloat * len(self.lines))(*self.lines),GL_STATIC_DRAW)        
   
    def loadTexture(self):
        self.texture = None
        #print "No texture for this object"
    
    def rendering(self,MVP,View,Projection):
        self.shader.begin()
        glUniformMatrix4fv(self.MVP_ID,1,GL_FALSE,glm.value_ptr(MVP))
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self.linebuffer)
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None)
        
        glDrawArrays(GL_LINES  , 0, len(self.lines)/3) # 12*3 indices starting at 0 -> 12 triangles 

        glDisableVertexAttribArray(0)       
        self.shader.end()
