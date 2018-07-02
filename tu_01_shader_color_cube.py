# import os,sys
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))


from OpenGL.GL import *  # pylint: disable=W0614

import glm
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
g_color_buffer_data = [ 
		0.583,  0.771,  0.014,
		0.609,  0.115,  0.436,
		0.327,  0.483,  0.844,
		0.822,  0.569,  0.201,
		0.435,  0.602,  0.223,
		0.310,  0.747,  0.185,
		0.597,  0.770,  0.761,
		0.559,  0.436,  0.730,
		0.359,  0.583,  0.152,
		0.483,  0.596,  0.789,
		0.559,  0.861,  0.639,
		0.195,  0.548,  0.859,
		0.014,  0.184,  0.576,
		0.771,  0.328,  0.970,
		0.406,  0.615,  0.116,
		0.676,  0.977,  0.133,
		0.971,  0.572,  0.833,
		0.140,  0.616,  0.489,
		0.997,  0.513,  0.064,
		0.945,  0.719,  0.592,
		0.543,  0.021,  0.978,
		0.279,  0.317,  0.505,
		0.167,  0.620,  0.077,
		0.347,  0.857,  0.137,
		0.055,  0.953,  0.042,
		0.714,  0.505,  0.345,
		0.783,  0.290,  0.734,
		0.722,  0.645,  0.174,
		0.302,  0.455,  0.848,
		0.225,  0.587,  0.040,
		0.517,  0.713,  0.338,
		0.053,  0.959,  0.120,
		0.393,  0.621,  0.362,
		0.673,  0.211,  0.457,
		0.820,  0.883,  0.371,
		0.982,  0.099,  0.879
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


		self.shader = shader = Shader()
		shader.initShaderFromGLSL(["glsl/tu01/vertex.glsl"],["glsl/tu01/fragment.glsl"])

		self.context.MVP_ID   = glGetUniformLocation(shader.program,"MVP")


		self.context.vertexbuffer  = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER,self.context.vertexbuffer)
		glBufferData(GL_ARRAY_BUFFER,len(g_vertex_buffer_data)*4,(GLfloat * len(g_vertex_buffer_data))(*g_vertex_buffer_data),GL_STATIC_DRAW)


		self.context.colorbuffer  = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER,self.context.colorbuffer)
		glBufferData(GL_ARRAY_BUFFER,len(g_color_buffer_data)*4,(GLfloat * len(g_color_buffer_data))(*g_color_buffer_data),GL_STATIC_DRAW)

	def calc_MVP(self,width=1920,height=1080):

		self.context.Projection = glm.perspective(glm.radians(45.0),float(width)/float(height),0.1,1000.0)
		self.context.View =  glm.lookAt(glm.vec3(4,3,-3), # Camera is at (4,3,-3), in World Space
						glm.vec3(0,0,0), #and looks at the (0.0.0))
						glm.vec3(0,1,0) ) #Head is up (set to 0,-1,0 to look upside-down)

		self.context.Model=  glm.mat4(1.0)

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

		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, self.context.vertexbuffer)
		glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None)

		glEnableVertexAttribArray(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.context.colorbuffer)
		glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,0,None)


		glDrawArrays(GL_TRIANGLES, 0, 12*3) # 12*3 indices starting at 0 -> 12 triangles

		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		self.shader.end()
        

if __name__ == "__main__":

    win = Tu01Win()
    win.init_opengl()
    win.init_context()
    win.run()
