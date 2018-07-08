# import os,sys
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))


from OpenGL.GL import *  # pylint: disable=W0614

from utils.meshViewer import MeshViewWindow, meshWithRender
from utils.shaderLoader import Shader

import glm
class meshFromArray(meshWithRender):

    def __init__(self, vertex_array, color_array):
        self.vertex_data = vertex_array
        self.color_data = color_array

    def loadShader(self):
        self.shader = Shader()
        self.shader.initShaderFromGLSL(
            ["glsl/tu01/vertex.glsl"], ["glsl/tu01/fragment.glsl"])
        self.MVP_ID = glGetUniformLocation(self.shader.program, "MVP")

    def loadObject(self):
        self.vertexbuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexbuffer)
        glBufferData(GL_ARRAY_BUFFER, len(self.vertex_data)*4, (GLfloat *
                                                                len(self.vertex_data))(*self.vertex_data), GL_STATIC_DRAW)

        self.vertexLen = len(self.vertex_data)

        self.colorbuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.colorbuffer)
        glBufferData(GL_ARRAY_BUFFER, len(self.color_data)*4, (GLfloat *
                                                               len(self.color_data))(*self.color_data), GL_STATIC_DRAW)
    def loadTexture(self):
        self.texture = None

    def rendering(self, MVP,View,Projection):

        self.shader.begin()
        glUniformMatrix4fv(self.MVP_ID, 1, GL_FALSE,  glm.value_ptr(MVP)  )

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexbuffer)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.colorbuffer)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

        
        glDrawArrays(GL_TRIANGLES, 0, self.vertexLen)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        self.shader.end()


class meshFromObj(meshWithRender):
    def __init__(self,meshName,textureName,location=[0.0,0.0,0.0]):
        self.meshName = meshName
        self.textureName = textureName
        self.location = location
    def loadShader(self):
        self.shader = Shader()
        self.shader.initShaderFromGLSL(
            ["glsl/tu02/vertex.glsl"], ["glsl/tu02/fragment.glsl"])
        self.MVP_ID = glGetUniformLocation(self.shader.program, "MVP")
        self.OFFSET_ID = glGetUniformLocation(self.shader.program, "OFFSET")
        self.Texture_ID =  glGetUniformLocation(self.shader.program, "myTextureSampler")

    def loadObject(self):

        from utils.objLoader import objLoader            
        model = objLoader(self.meshName).to_single_index_style()
        self.model = model
        self.vertexbuffer  = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.vertexbuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(model.vertexs)*4,(GLfloat * len(model.vertexs))(*model.vertexs),GL_STATIC_DRAW)
        

        self.indicesbufferSize = len(model.indices)

        self.indicesbuffer  = glGenBuffers(1)        		
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.indicesbuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(model.indices)*2,(GLushort * len(model.indices))(*model.indices),GL_STATIC_DRAW)

    def loadTexture(self):
            from utils.textureLoader import textureLoader
            texture = textureLoader(self.textureName)	
            model = self.model
            if(texture.inversedVCoords):
                for index in range(0,len(model.texcoords)):
                    if(index % 2):
                        model.texcoords[index] = 1.0 - model.texcoords[index]

            self.texturebuffer = texture.textureGLID

            self.uvbuffer  = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.uvbuffer)            
            glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(model.texcoords)*4,(GLfloat * len(model.texcoords))(*model.texcoords),GL_STATIC_DRAW)

    def rendering(self, MVP,View,Projection):
        self.shader.begin()
        glUniformMatrix4fv(self.MVP_ID,1,GL_FALSE, glm.value_ptr(MVP)        )
        glUniform3f(self.OFFSET_ID,self.location[0],self.location[1],self.location[2])

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texturebuffer)
        glUniform1i(self.Texture_ID, 0) 		#// Set  "myTextureSampler" sampler to use Texture Unit 0

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexbuffer)
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.uvbuffer)
        glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,0,None)

        
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indicesbuffer)
        
        glDrawElements(
            GL_TRIANGLES,      # mode
            self.indicesbufferSize,    #// count
            GL_UNSIGNED_SHORT, #  // type
            None          #// element array buffer offset
        )		
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        self.shader.end()        
from tu_01_color_cube import g_vertex_buffer_data, g_color_buffer_data
if __name__ == "__main__":

    win = MeshViewWindow().init_default()    
    win.add_mesh(meshFromObj(meshName="resources/tu04/suzanne.obj",textureName="resources/tu04/uvmap.dds",location=[0.0,2.0,0.0]))
    win.add_mesh(meshFromArray(g_vertex_buffer_data, g_color_buffer_data))
    win.run()
