# import os,sys
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))


from OpenGL.GL import *  # pylint: disable=W0614

import glm
from utils.glutWindow import GlutWindow
from utils.objLoader import objLoader
from utils.shaderLoader import Shader
from utils.textureLoader import textureLoader
from utils.MVPControl import MVPController
from utils.worldsheet import worldSheet
from utils.uv2d import UV2D

class Tu01Win(GlutWindow):

    class GLContext(object):
        pass
    def init_opengl(self):
        glClearColor(0.1,0.1,0.1,0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        #glEnable(GL_CULL_FACE)

    def init_context(self):
        self.context = self.GLContext()

        self.shader = shader = Shader()

        self.UV2d = UV2D()
        shader.initShaderFromGLSL(["glsl/tu02/vertex.glsl"],["glsl/tu02/fragment.glsl"])
        # shader var ids 
        self.context.MVP_ID   = glGetUniformLocation(shader.program,"MVP")
        self.context.Texture_ID =  glGetUniformLocation(shader.program, "myTextureSampler")
        
        # texture = textureLoader("resources/tu03/uvmap.dds")
        # model = objLoader("resources/tu03/cube.obj").to_single_index_style()
        texture = textureLoader("resources/tu04/uvmap.dds")		
        model = objLoader("resources/tu04/suzanne.obj").to_single_index_style()        
        self.context.texturebuffer = texture.textureGLID
        if(texture.inversedVCoords):
            for index in range(0,len(model.texcoords)):
                if(index % 2):
                    model.texcoords[index] = 1.0 - model.texcoords[index]	
                    
        #print "ccc",len(model.texcoords)
        self.context.vertexbuffer  = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.context.vertexbuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(model.vertexs)*4,(GLfloat * len(model.vertexs))(*model.vertexs),GL_STATIC_DRAW)

        self.context.uvbuffer  = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.context.uvbuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(model.texcoords)*4,(GLfloat * len(model.texcoords))(*model.texcoords),GL_STATIC_DRAW)

        

        self.context.elementbuffer  = glGenBuffers(1)
        self.context.elementbufferSize = len(model.indices)		
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.context.elementbuffer)
        
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(model.indices)*2,(GLushort * len(model.indices))(*model.indices),GL_STATIC_DRAW)

        self.UV2d.bindUV(self.context.uvbuffer,self.context.elementbuffer,self.context.elementbufferSize)
    

    def calc_MVP(self,width=0,height=0):
        if(width!=0):
            self.controller.resize(width,height)
        self.context.Model=  glm.mat4(1.0)
        self.context.MVP =  self.controller.calcMVP(self.context.Model)
        

    def resize(self,Width,Height):        
        glViewport(0, 0, Width, Height)
        self.calc_MVP(Width,Height)

    def ogl_draw(self):

        print "draw++"
        #print self.context.MVP
        self.calc_MVP()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.shader.begin()
        glUniformMatrix4fv(self.context.MVP_ID,1,GL_FALSE,glm.value_ptr(self.context.MVP))

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.context.texturebuffer)
        glUniform1i(self.context.Texture_ID, 0) 		#// Set  "myTextureSampler" sampler to use Texture Unit 0

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self.context.vertexbuffer)
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.context.uvbuffer)
        glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,0,None)

        
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.context.elementbuffer)
        
        glDrawElements(
            GL_TRIANGLES,      # mode
            self.context.elementbufferSize,    #// count
            GL_UNSIGNED_SHORT, #  // type
            None          #// element array buffer offset
        )		
        

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        self.shader.end()
        
        self.UV2d.draw()
if __name__ == "__main__":

    win = Tu01Win()
    win.controller = MVPController(win.update_if)
    win.init_opengl()
    win.init_context()
    win.run()
