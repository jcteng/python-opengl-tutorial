# import os,sys
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))


from OpenGL.GL import *  # pylint: disable=W0614

from utils.meshViewer import MeshViewWindow, meshWithRender
from utils.shaderLoader import Shader

import glm


from math import fabs
 

class NormalMapping(meshWithRender):

    def __init__(self,meshName,textureName,location=[0.0,0.0,0.0]):
        self.meshName = meshName
        self.textureName = textureName
        self.location = location

    def indexVBO_TBN(self,vertex,uv,normal,tangents,bitangents):
        class Container(object):
            pass  
        indices = []
        out_vertexs = []
        out_uvs = []
        out_normals = []
        out_tangents =[]
        out_bitangents = []
        newindex = 0
        def getSimilarVertexIndex(in_vertex,in_uv,in_normal,vertex_list,uv_list,normal_list):

            def is_near(v1,v2):
                return fabs(v1-v2)<0.01
            for idx in range(0,len(vertex_list)/3): 
                vertex_in_list = vertex_list[idx*3:idx*3+3]
                uv_in_list = uv_list[idx*2:idx*2+2]
                normal_in_list = normal_list[idx*3:idx*3+3]
                
                if(is_near(in_vertex[0],vertex_in_list[0])&
                   is_near(in_vertex[1],vertex_in_list[1])&
                   is_near(in_vertex[2],vertex_in_list[2])&
                   is_near(in_uv[0],uv_in_list[0])&
                   is_near(in_uv[1],uv_in_list[1])&    
                   is_near(in_normal[0],normal_in_list[0])&
                   is_near(in_normal[1],normal_in_list[1])&   
                   is_near(in_normal[2],normal_in_list[2])):
                    return True,idx
 
            return False,0

        for idx in range(0,len(vertex)/3): 
            current_v = vertex[idx*3:idx*3+3]
            current_uv = uv[idx*2:idx*2+2]
            current_normal = normal[idx*3:idx*3+3]
            
            found,idx_found = getSimilarVertexIndex(current_v,current_uv,current_normal,out_vertexs,out_uvs,out_normals)
            if found  :
                indices.append( idx_found)
            else:
                indices.append(newindex)
                out_vertexs = out_vertexs + current_v
                out_uvs = out_uvs + current_uv
                out_normals = normal + current_normal
                out_tangents = out_tangents + tangents[idx*3:idx*3+3]
                out_bitangents = out_bitangents + bitangents[idx*3:idx*3+3]
                newindex +=1

        outobj = Container()
        outobj.indices = indices        
        outobj.vertexs = out_vertexs
        outobj.texcoords = out_uvs
        outobj.normals = out_normals
        outobj.tangents =out_tangents
        outobj.bitangents = out_bitangents

        return outobj        

    def computeTangentBasis(self,vertex,uv,normal):

              

        tangents = []
        bitangents = []
        for idx in range(0,len(vertex)/9):
            
            offset = idx*9
            v0 = vertex[offset:offset+3]
            v1 = vertex[offset+3:offset+6]
            v2 = vertex[offset+6:offset+9]

            offset = idx*6
            uv0 =   uv[offset:offset+2]
            uv1 =   uv[offset+2:offset+4]
            uv2 =   uv[offset+4:offset+6]
            #print v0,v1,v2
            deltaPos1 = glm.vec3([v1[0]-v0[0],v1[1]-v0[1],v1[2]-v0[2]])
            deltaPos2 = glm.vec3([v2[0]-v0[0],v2[1]-v0[1],v2[2]-v0[2]])

            deltaUV1 = glm.vec2([uv1[0]-uv0[0],uv1[1]-uv0[1]])
            deltaUV2 = glm.vec2([uv2[0]-uv0[0],uv2[1]-uv0[1]])

            r = 1.0 / (deltaUV1.x * deltaUV2.y - deltaUV1.y * deltaUV2.x)
            tangent = (deltaPos1 * deltaUV2.y   - deltaPos2 * deltaUV1.y)*r
            bitangent = (deltaPos2 * deltaUV1.x   - deltaPos1 * deltaUV2.x)*r

            tangents.extend([tangent.x,tangent.y,tangent.z])
            tangents.extend([tangent.x,tangent.y,tangent.z])
            tangents.extend([tangent.x,tangent.y,tangent.z])
            
            bitangents.extend([bitangent.x,bitangent.y,bitangent.z])
            bitangents.extend([bitangent.x,bitangent.y,bitangent.z])
            bitangents.extend([bitangent.x,bitangent.y,bitangent.z])
        

        return tangents,bitangents
    def loadShader(self):
        self.shader = Shader()
        self.shader.initShaderFromGLSL(
            ["glsl/tu10/NormalMapping.vertexshader.glsl"], ["glsl/tu10/NormalMapping.fragmentshader.glsl"])

        self.MatrixID = glGetUniformLocation(self.shader.program, "MVP")
        self.ViewMatrixID = glGetUniformLocation(self.shader.program, "V")
        self.ModelMatrixID = glGetUniformLocation(self.shader.program, "M")
        self.ModelView3x3MatrixID = glGetUniformLocation(self.shader.program, "MV3x3")
        self.DiffuseTextureID = glGetUniformLocation(self.shader.program, "DiffuseTextureSampler")
        self.NormalTextureID = glGetUniformLocation(self.shader.program, "NormalTextureSampler")
        self.SpecularTextureID = glGetUniformLocation(self.shader.program, "SpecularTextureSampler")
        self.LightID = glGetUniformLocation(self.shader.program, "LightPosition_worldspace")

    def loadObject(self):

        from utils.objLoader import objLoader            
        model = objLoader(self.meshName).to_array_style()

        tangents,bitangents = self.computeTangentBasis(model.vertexs,model.texcoords,model.normals)

        self.model = model = self.indexVBO_TBN(model.vertexs,model.texcoords,model.normals,tangents,bitangents)

         
        self.vertexbuffer  = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.vertexbuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(model.vertexs)*4,(GLfloat * len(model.vertexs))(*model.vertexs),GL_STATIC_DRAW)
        

        self.normalbuffer  = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.normalbuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(model.normals)*4,(GLfloat * len(model.normals))(*model.normals),GL_STATIC_DRAW)

        self.tangentbuffer  = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.tangentbuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(model.tangents)*4,(GLfloat * len(model.tangents))(*model.tangents),GL_STATIC_DRAW)

        self.bitangentbuffer  = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.bitangentbuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(model.bitangents)*4,(GLfloat * len(model.bitangents))(*model.bitangents),GL_STATIC_DRAW)

        self.indicesbufferSize = len(model.indices)

        self.indicesbuffer  = glGenBuffers(1)        		
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.indicesbuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(model.indices)*2,(GLushort * len(model.indices))(*model.indices),GL_STATIC_DRAW)

    def loadTexture(self):
            from utils.textureLoader import textureLoader
            DiffuseTexture = textureLoader(self.textureName[0])
            NormalTexture =  textureLoader(self.textureName[1])
            SpecularTexture =  textureLoader(self.textureName[2])

            model = self.model
            # if(DiffuseTexture.inversedVCoords):
            for index in range(0,len(model.texcoords)):
                if(index % 2):
                    model.texcoords[index] = 1.0 - model.texcoords[index]

            self.DiffuseTexture = DiffuseTexture.textureGLID
            self.NormalTexture = NormalTexture.textureGLID
            self.SpecularTexture = SpecularTexture.textureGLID

            self.uvbuffer  = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.uvbuffer)            
            glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(model.texcoords)*4,(GLfloat * len(model.texcoords))(*model.texcoords),GL_STATIC_DRAW)
    def rendering(self, MVP,View,Projection):
        self.shader.begin()
        ModelMatrix = glm.mat4(1.0)
        #print View
        ModelViewMatrix = glm.mat4(View)*ModelMatrix

        ModelView3x3Matrix = glm.mat3(ModelViewMatrix)        
        glUniformMatrix4fv(self.MatrixID,1,GL_FALSE, glm.value_ptr(MVP)     )          
        glUniformMatrix4fv(self.ModelMatrixID,1,GL_FALSE,glm.value_ptr(ModelMatrix))   
        glUniformMatrix4fv(self.ViewMatrixID,1,GL_FALSE, glm.value_ptr(View))
        glUniformMatrix3fv(self.ModelView3x3MatrixID,1,GL_FALSE,glm.value_ptr(ModelView3x3Matrix) )  

        lightPos = glm.vec3(0.0,0.0,4.0)
        glUniform3f(self.LightID, lightPos.x, lightPos.y, lightPos.z)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.DiffuseTexture)
        glUniform1i(self.DiffuseTextureID, 0)       

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.NormalTexture)
        glUniform1i(self.NormalTextureID, 1)  


        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.SpecularTexture)
        glUniform1i(self.SpecularTextureID, 2)  


        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexbuffer)
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.uvbuffer)
        glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,0,None)

        glEnableVertexAttribArray(2)
        glBindBuffer(GL_ARRAY_BUFFER, self.normalbuffer)
        glVertexAttribPointer(2,3,GL_FLOAT,GL_FALSE,0,None)


        glEnableVertexAttribArray(3)
        glBindBuffer(GL_ARRAY_BUFFER, self.tangentbuffer)
        glVertexAttribPointer(3,3,GL_FLOAT,GL_FALSE,0,None)

        glEnableVertexAttribArray(4)
        glBindBuffer(GL_ARRAY_BUFFER, self.bitangentbuffer)
        glVertexAttribPointer(4,3,GL_FLOAT,GL_FALSE,0,None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indicesbuffer)        

        glDrawElements(
            GL_TRIANGLES,      # mode
            self.indicesbufferSize,    #// count
            GL_UNSIGNED_SHORT, #  // type
            None          #// element array buffer offset
        )		

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)
        glDisableVertexAttribArray(3)
        glDisableVertexAttribArray(4)


from tu_07_basic_shading import basicShading
from tu_06_multobjs import meshFromObj
if __name__ == "__main__":
    win = MeshViewWindow().init_default()  
    win.add_mesh(NormalMapping(meshName="resources/tu10/cylinder.obj",textureName=["resources/tu10/diffuse.DDS","resources/tu10/normal.bmp","resources/tu10/specular.DDS"]))

    win.add_mesh(basicShading(meshName="resources/tu10/cylinder.obj",textureName="resources/tu10/diffuse.DDS",location=[0,0,3]))

    win.add_mesh(meshFromObj(meshName="resources/tu10/cylinder.obj",textureName="resources/tu10/diffuse.DDS",location=[3,0,0]))

    win.run()
