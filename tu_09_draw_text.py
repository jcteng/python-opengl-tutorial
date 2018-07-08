# import os,sys
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))


from OpenGL.GL import *  # pylint: disable=W0614

from utils.meshViewer import MeshViewWindow, meshWithRender
from utils.shaderLoader import Shader

import glm



from tu_07_basic_shading import basicShading


class Draw2DText(meshWithRender):

    def __init__(self,text_str,x,y,Xsize,Ysize):
        (self.text_str,self.x,self.y,self.Xsize,self.Ysize ) = (text_str,x,y,Xsize,Ysize)
        
        
        

    def loadShader(self):
        self.shader = Shader()
        self.shader.initShaderFromGLSL(
            ["glsl/tu09/TextVertexShader.vertexshader.glsl"], ["glsl/tu09/TextVertexShader.fragmentshader.glsl"])
        self.HALFSCREENSIZE_ID = glGetUniformLocation(self.shader.program, "HALFSCREENSIZE")
        self.Texture_ID = glGetUniformLocation(self.shader.program, "myTextureSampler")
    
    def loadObject(self):

        vertex_array = []
        uv_array = []
        lineCount =0
        for line in self.text_str:            
            for idx in range(0,len(line)):
                xoffset = idx*self.Xsize
                yoffset = lineCount*self.Ysize
                vertex_up_left =    [self.x+xoffset          ,self.y+yoffset+self.Ysize]
                vertex_up_right =   [self.x+xoffset+self.Xsize,self.y+yoffset+self.Ysize]
                vertex_down_right = [self.x+xoffset+self.Xsize,self.y+yoffset]
                vertex_down_left =  [self.x+xoffset          ,self.y+yoffset]
                vertex_array = vertex_array + vertex_up_left+vertex_down_left+vertex_up_right
                vertex_array = vertex_array + vertex_down_right+vertex_up_right+vertex_down_left
                
                character =  ord(line[idx])
                uv_x = (character%16)/16.0
                uv_y = (character/16)/16.0

                uv_up_left   =  [uv_x,uv_y]
                uv_up_right   =  [uv_x +1.0/16.0,uv_y]
                uv_down_right =  [uv_x + 1.0/16.0,uv_y+1.0/16.0]
                uv_down_left   =  [uv_x,uv_y+1.0/16.0]
                uv_array = uv_array + uv_up_left+uv_down_left+uv_up_right
                uv_array = uv_array + uv_down_right+uv_up_right+uv_down_left
            lineCount+=1
        self.vertexbuffer  = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.vertexbuffer)        
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(vertex_array)*4,(GLfloat * len(vertex_array))(*vertex_array),GL_STATIC_DRAW)
 
        self.uvbuffer  = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.uvbuffer)    
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(uv_array)*4,(GLfloat * len(uv_array))(*uv_array),GL_STATIC_DRAW)
 
        self.vertex_array = vertex_array
    def loadTexture(self):
            from utils.textureLoader import textureLoader
            texture = textureLoader("resources/tu09/Holstein.DDS")	
            self.texturebuffer = texture.textureGLID
    def rendering(self, MVP,View,Projection):
        self.shader.begin()

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texturebuffer)
        glUniform1i(self.Texture_ID, 0)

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexbuffer)
        glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,0,None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.uvbuffer)
        glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,0,None)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertex_array))
        glDisable(GL_BLEND)
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)       
        self.shader.end() 
if __name__ == "__main__":
    win = MeshViewWindow().init_default()  
    win.add_mesh(basicShading(meshName="resources/tu04/suzanne.obj",textureName="resources/tu04/uvmap.dds"))
    win.add_mesh(Draw2DText(["enjoy it","this is the sample"],0,0,20,20))
    win.run()
