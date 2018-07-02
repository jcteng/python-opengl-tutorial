
import glfw
from OpenGL.GL import *  # pylint: disable=W0614
from OpenGL.GLU import *  # pylint: disable=W0614

import glm
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


glfw.init()
glfw.window_hint(glfw.SAMPLES,4)
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,3)
glfw.window_hint(glfw.OPENGL_PROFILE,glfw.OPENGL_CORE_PROFILE)


window  = glfw.create_window(1024,768,"title of the window",None,None)

glfw.make_context_current(window)


glClearColor(0.0,0,0.4,0)
glDepthFunc(GL_LESS)
glEnable(GL_DEPTH_TEST)

vertex = glGenVertexArrays(1) # pylint: disable=W0612
glBindVertexArray(vertex)

shader = Shader()
shader.initShaderFromGLSL(["glsl/tu01/vertex.glsl"],["glsl/tu01/fragment.glsl"])

MVP_ID   = glGetUniformLocation(shader.program,"MVP")

Projection = glm.perspective(glm.radians(45.0),800.0/480.0,0.1,100.0)
View =  glm.lookAt(glm.vec3(4,3,-3), # Camera is at (4,3,-3), in World Space
                glm.vec3(0,0,0), #and looks at the (0.0.0))
                glm.vec3(0,1,0) ) #Head is up (set to 0,-1,0 to look upside-down)

Model=  glm.mat4(1.0)
MVP =  Projection * View *Model
#print context.MVP
#exit(0)

vertexbuffer  = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,vertexbuffer)
glBufferData(GL_ARRAY_BUFFER,len(g_vertex_buffer_data)*4,(GLfloat * len(g_vertex_buffer_data))(*g_vertex_buffer_data),GL_STATIC_DRAW)


colorbuffer  = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,colorbuffer)
glBufferData(GL_ARRAY_BUFFER,len(g_color_buffer_data)*4,(GLfloat * len(g_color_buffer_data))(*g_color_buffer_data),GL_STATIC_DRAW)

while(True):
	#print self.context.MVP
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	#shader.begin()
	glUseProgram(shader.program)
	glUniformMatrix4fv(MVP_ID,1,GL_FALSE,glm.value_ptr(MVP))

	glEnableVertexAttribArray(0)
	glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer)

	glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None) # None means ctypes.c_voidp(0)

	glEnableVertexAttribArray(1)
	glBindBuffer(GL_ARRAY_BUFFER, colorbuffer)
	glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,0,ctypes.c_voidp(0))


	glDrawArrays(GL_TRIANGLES, 0, 12*3) # 12*3 indices starting at 0 -> 12 triangles

	glDisableVertexAttribArray(0)
	glDisableVertexAttribArray(1)
	#shader.end()
	glfw.swap_buffers(window)
