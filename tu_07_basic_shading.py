# import os,sys
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))


from OpenGL.GL import *  # pylint: disable=W0614

from utils.meshViewer import MeshViewWindow, meshWithRender
from utils.shaderLoader import Shader

import glm


class basicShading(meshWithRender):
    def __init__(self,meshName,textureName):
        self.meshName = meshName
        self.textureName = textureName

    def loadShader(self):
        self.shader = Shader()
        self.shader.initShaderFromGLSL(
            ["glsl/tu07/StandardShading.vertexshader.glsl"], ["glsl/tu07/StandardShading.fragmentshader.glsl"])
        self.MVP_ID = glGetUniformLocation(self.shader.program, "MVP")
        self.ModelMatrix_ID = glGetUniformLocation(self.shader.program, "M")
        self.ViewMatrix_ID = glGetUniformLocation(self.shader.program, "V")
        self.Texture_ID =  glGetUniformLocation(self.shader.program, "myTextureSampler")
        self.Light_ID =  glGetUniformLocation(self.shader.program, "LightPosition_worldspace")

    def loadObject(self):

        from utils.objLoader import objLoader            
        model = objLoader(self.meshName).to_single_index_style()
        self.model = model
        self.vertexbuffer  = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.vertexbuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(model.vertexs)*4,(GLfloat * len(model.vertexs))(*model.vertexs),GL_STATIC_DRAW)

        # used normal
        self.normalbuffer  = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.normalbuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(model.normals)*4,(GLfloat * len(model.normals))(*model.normals),GL_STATIC_DRAW)
      

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
        glUniformMatrix4fv(self.MVP_ID,1,GL_FALSE, glm.value_ptr(MVP))
        glUniformMatrix4fv(self.ModelMatrix_ID,1,GL_FALSE,glm.value_ptr(glm.mat4(1.0)))   
        glUniformMatrix4fv(self.ViewMatrix_ID,1,GL_FALSE,glm.value_ptr(View))     

        lightPos = glm.vec3(4.0,4.0,4.0)
        glUniform3f(self.Light_ID, lightPos.x, lightPos.y, lightPos.z)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texturebuffer)
        glUniform1i(self.Texture_ID, 0) 		#// Set  "myTextureSampler" sampler to use Texture Unit 0

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexbuffer)
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.uvbuffer)
        glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,0,None)

        glEnableVertexAttribArray(2)
        glBindBuffer(GL_ARRAY_BUFFER, self.normalbuffer)
        glVertexAttribPointer(2,3,GL_FLOAT,GL_FALSE,0,None)
        
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indicesbuffer)
        
        glDrawElements(
            GL_TRIANGLES,      # mode
            self.indicesbufferSize,    #// count
            GL_UNSIGNED_SHORT, #  // type
            None          #// element array buffer offset
        )		
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(1)
     

from tu_06_multobjs import meshFromObj
if __name__ == "__main__":

    win = MeshViewWindow().init_default()    
    win.add_mesh(meshFromObj(meshName="resources/tu04/suzanne.obj",textureName="resources/tu04/uvmap.dds",location=[0.0,3.0,0.0]))    
    win.add_mesh(basicShading(meshName="resources/tu04/suzanne.obj",textureName="resources/tu04/uvmap.dds"))

    win.run()
