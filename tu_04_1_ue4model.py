# import os,sys
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))


from OpenGL.GL import *  # pylint: disable=W0614

import glm
from utils.glutWindow import GlutWindow
from utils.objLoader import objLoader
from utils.shaderLoader import Shader
from utils.textureLoader import textureLoader

import numpy as np
class MeshUE4:

	def loadMesh(self):
		from ue4reader import uasset
		ArchiveName = "D:/unpack/objects/Weapon/Rifles/AK-47/Meshes/AK-47_01.uasset"
		#ArchiveName = "D:/unpack/objects/Weapon/Rifles/AWM/Meshes/AWM_01.uasset"
		asset = uasset.UAssetReader(ArchiveName,forceUE4Ver=513)
		meshObj = asset.ExportsMap[1].GetObject()
		meshObj.Serialize(asset)
		print meshObj.properties[1].to_dict()
		return meshObj.RenderData.LODResources[0]

	def getMesh(self):
		ue4LOD =self.loadMesh()
		self.vertexs =ue4LOD.VertexBuffers.PositionVertexBuffer.VertexData.to_array()        			
		self.indices  = ue4LOD.IndexBuffer.to_array()
		self.texcoords = ue4LOD.VertexBuffers.StaticMeshVertexBuffer.TexcoordData.to_array()
		self.tangentXZ = ue4LOD.VertexBuffers.StaticMeshVertexBuffer.TangentsData.to_array()
		# self.texcoords= []
		# for i in range(0,len(self._texcoords),2):
		# 	print "."
		# 	self.texcoords.append(float(self._texcoords[i]))
		# 	self.texcoords.append(1.0 - float(self._texcoords[i+1]))
		return self
					
		 

class Tu01Win(GlutWindow):

	class GLContext(object):
		pass
	def init_opengl(self):
		glClearColor(0.0,0,0.4,0)
		glDepthFunc(GL_LESS)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_CULL_FACE)

	def on_keyboard(self,key,x,y):        		
		print "please overrider on_keyboard" 
	def on_mouse(self,*args,**kwargs):
		print "please overrider on_mouse" 
	def on_mousemove(self,*args,**kwargs):
		print "please overrider on_mousemove" 

	def init_context(self):
		self.context = self.GLContext()

		self.shader = shader = Shader()
		shader.initShaderFromGLSL(["glsl/tu02/vertex.glsl"],["glsl/tu02/fragment.glsl"])
		# shader var ids 
		self.context.MVP_ID   = glGetUniformLocation(shader.program,"MVP")
		self.context.Texture_ID =  glGetUniformLocation(shader.program, "myTextureSampler")		

		texture = textureLoader("resources/tu05/AK-47_01_D_Fix.png")				
		self.context.texturebuffer = texture.textureGLID

					
		model = MeshUE4().getMesh()
		self.context.vertexbuffer  = glGenBuffers(1)
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.context.vertexbuffer)
		glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(model.vertexs)*4,(GLfloat * len(model.vertexs))(*model.vertexs),GL_STATIC_DRAW)

		self.context.uvbuffer  = glGenBuffers(1)
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.context.uvbuffer)
		glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(model.texcoords)*4,(GLfloat * len(model.texcoords))(*model.texcoords),GL_STATIC_DRAW)


		self.context.indices  = glGenBuffers(1)
		self.context.indicesSize = len(model.indices)		
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.context.indices)
		glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(model.indices)*2,(GLushort * len(model.indices))(*model.indices),GL_STATIC_DRAW)

	

	def calc_MVP(self,width=1920,height=1080):

		self.context.Projection = glm.perspective(glm.radians(45.0),float(width)/float(height),0.1,1000.0)
		self.context.View =  glm.lookAt(glm.vec3(80,80,80), # Camera is at (4,3,-3), in World Space
						glm.vec3(0,0,0), #and looks at the (0.0.0))
						glm.vec3(0,1,0) ) #Head is up (set to 0,-1,0 to look upside-down)

		self.context.Model=  glm.mat4(1.0)
		#print self.context.Model
		self.context.MVP =  self.context.Projection * self.context.View * self.context.Model	

	def resize(self,Width,Height):
		
		glViewport(0, 0, Width, Height)
		self.calc_MVP(Width,Height)

	def ogl_draw(self):

		print "draw++"
		#print self.context.MVP
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

		
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.context.indices)
		
		glDrawElements(
			GL_TRIANGLES,      # mode
			self.context.indicesSize,    #// count
			GL_UNSIGNED_SHORT, #  // type
			None          #// element array buffer offset
		)		
		

		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		self.shader.end()
        

if __name__ == "__main__":

    win = Tu01Win()
    win.init_opengl()
    win.init_context()
    win.run()
