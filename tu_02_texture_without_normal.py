# import os,sys
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))


from OpenGL.GL import *  # pylint: disable=W0614

import glm
from utils.textureLoader import textureLoader
from utils.glutWindow import GlutWindow
from utils.shaderLoader import Shader

g_vertex_buffer_data = [
		-1.0,-1.0,-1.0,
		-1.0,-1.0, 1.0,
		-1.0, 1.0, 1.0,
		 1.0, 1.0,-1.0,
		-1.0,-1.0,-1.0,
		-1.0, 1.0,-1.0,
		 1.0,-1.0, 1.0,
		-1.0,-1.0,-1.0,
		 1.0,-1.0,-1.0,
		 1.0, 1.0,-1.0,
		 1.0,-1.0,-1.0,
		-1.0,-1.0,-1.0,
		-1.0,-1.0,-1.0,
		-1.0, 1.0, 1.0,
		-1.0, 1.0,-1.0,
		 1.0,-1.0, 1.0,
		-1.0,-1.0, 1.0,
		-1.0,-1.0,-1.0,
		-1.0, 1.0, 1.0,
		-1.0,-1.0, 1.0,
		 1.0,-1.0, 1.0,
		 1.0, 1.0, 1.0,
		 1.0,-1.0,-1.0,
		 1.0, 1.0,-1.0,
		 1.0,-1.0,-1.0,
		 1.0, 1.0, 1.0,
		 1.0,-1.0, 1.0,
		 1.0, 1.0, 1.0,
		 1.0, 1.0,-1.0,
		-1.0, 1.0,-1.0,
		 1.0, 1.0, 1.0,
		-1.0, 1.0,-1.0,
		-1.0, 1.0, 1.0,
		 1.0, 1.0, 1.0,
		-1.0, 1.0, 1.0,
		 1.0,-1.0, 1.0]
g_uv_buffer_data = [
		0.000059, 1.0-0.000004, 
		0.000103, 1.0-0.336048, 
		0.335973, 1.0-0.335903, 
		1.000023, 1.0-0.000013, 
		0.667979, 1.0-0.335851, 
		0.999958, 1.0-0.336064, 
		0.667979, 1.0-0.335851, 
		0.336024, 1.0-0.671877, 
		0.667969, 1.0-0.671889, 
		1.000023, 1.0-0.000013, 
		0.668104, 1.0-0.000013, 
		0.667979, 1.0-0.335851, 
		0.000059, 1.0-0.000004, 
		0.335973, 1.0-0.335903, 
		0.336098, 1.0-0.000071, 
		0.667979, 1.0-0.335851, 
		0.335973, 1.0-0.335903, 
		0.336024, 1.0-0.671877, 
		1.000004, 1.0-0.671847, 
		0.999958, 1.0-0.336064, 
		0.667979, 1.0-0.335851, 
		0.668104, 1.0-0.000013, 
		0.335973, 1.0-0.335903, 
		0.667979, 1.0-0.335851, 
		0.335973, 1.0-0.335903, 
		0.668104, 1.0-0.000013, 
		0.336098, 1.0-0.000071, 
		0.000103, 1.0-0.336048, 
		0.000004, 1.0-0.671870, 
		0.336024, 1.0-0.671877, 
		0.000103, 1.0-0.336048, 
		0.336024, 1.0-0.671877, 
		0.335973, 1.0-0.335903, 
		0.667969, 1.0-0.671889, 
		1.000004, 1.0-0.671847, 
		0.667979, 1.0-0.335851
	]



class Tu01Win(GlutWindow):

	class GLContext(object):
		pass
	def init_opengl(self):
		glClearColor(0.0,0,0.4,0)
		glDepthFunc(GL_LESS)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_CULL_FACE)

	def init_context(self):
		self.context = self.GLContext()

		# vertex = glGenVertexArrays(1) # pylint: disable=W0612
		# glBindVertexArray(vertex)

		self.shader = shader = Shader()
		shader.initShaderFromGLSL(["glsl/tu02/vertex.glsl"],["glsl/tu02/fragment.glsl"])

		self.context.MVP_ID   = glGetUniformLocation(shader.program,"MVP")
		self.context.TextureID =  glGetUniformLocation(shader.program, "myTextureSampler")


		texture = textureLoader("resources/tu02/uvtemplate.tga")
		#texture = textureLoader("resources/tu02/uvtemplate.dds")

		self.context.textureGLID = texture.textureGLID

		self.context.vertexbuffer  = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER,self.context.vertexbuffer)
		glBufferData(GL_ARRAY_BUFFER,len(g_vertex_buffer_data)*4,(GLfloat * len(g_vertex_buffer_data))(*g_vertex_buffer_data),GL_STATIC_DRAW)

		if(texture.inversedVCoords):
			for index in range(0,len(g_uv_buffer_data)):
				if(index % 2):
					g_uv_buffer_data[index] = 1.0 - g_uv_buffer_data[index]

		self.context.uvbuffer  = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER,self.context.uvbuffer)
		glBufferData(GL_ARRAY_BUFFER,len(g_uv_buffer_data)*4,(GLfloat * len(g_uv_buffer_data))(*g_uv_buffer_data),GL_STATIC_DRAW)

	def calc_MVP(self,width=1920,height=1080):

		self.context.Projection = glm.perspective(glm.radians(45.0),float(width)/float(height),0.1,1000.0)
		self.context.View =  glm.lookAt(glm.vec3(4,3,-3), # Camera is at (4,3,-3), in World Space
						glm.vec3(0,0,0), #and looks at the (0.0.0))
						glm.vec3(0,1,0) ) #Head is up (set to 0,-1,0 to look upside-down)
		#fixed Cube Size
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
		glBindTexture(GL_TEXTURE_2D, self.context.textureGLID)
		glUniform1i(self.context.TextureID, 0)


		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, self.context.vertexbuffer)
		glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None)

		glEnableVertexAttribArray(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.context.uvbuffer)
		glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,0,None)


		glDrawArrays(GL_TRIANGLES, 0, 12*3) # 12*3 indices starting at 0 -> 12 triangles

		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		self.shader.end()
        

if __name__ == "__main__":

    win = Tu01Win()
    win.init_opengl()
    win.init_context()
    win.run()
