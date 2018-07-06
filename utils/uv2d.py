from OpenGL.GL import *
from .shaderLoader import Shader
import glm


class UV2D(object):
    def __init__(self):
        self.shader  = Shader()
        self.shader.initShaderFromGLSL(["glsl/utils/uv2d/vertex.glsl"],["glsl/utils/uv2d/fragment.glsl"])
    
    def bindUV(self,uv,indices,size):
        self.UVbuffer = uv
        self.size = size
        self.indicesbuffer =indices
        print self.indicesbuffer
    def draw(self):
        #do this without shader
        self.shader.begin()

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self.UVbuffer)
        glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,0,None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indicesbuffer) 
                 
        mode = glGetIntegerv(GL_POLYGON_MODE)         
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

       
        glDrawElements(
            GL_TRIANGLES,      # mode
            self.size,    #// count
            GL_UNSIGNED_SHORT, #  // type
            None          #// element array buffer offset
        )	
        
        
        glDisableVertexAttribArray(0)  
        glPolygonMode(GL_FRONT_AND_BACK, mode[0])    
        self.shader.end()