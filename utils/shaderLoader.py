
from OpenGL import GL as gl


def printOpenGLError():
    err = gl.glGetError() # pylint: disable=E1111
    if (err != gl.GL_NO_ERROR):
        print('GLERROR: ', gl.gluErrorString(err)) # pylint: disable=E1101

import os
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
class Shader(object):

    def initShaderFromGLSL(self, vertex_shader_paths, fragment_shader_paths):
        vertex_shader_source_list = []
        fragment_shader_source_list = []
        if(isinstance(vertex_shader_paths,list)):

            
            for GLSL in vertex_shader_paths:
                absDIR =  os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__),".."),GLSL))
                f = open(absDIR,'rb')
                vertex_shader_source_list.append(f.read())
                f.close()
            for GLSL in fragment_shader_paths:
                absDIR =  os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__),".."),GLSL))
                f = open(absDIR,'rb')
                fragment_shader_source_list.append(f.read())      
                f.close()    
            self.initShader(vertex_shader_source_list,fragment_shader_source_list)


    def initShader(self, vertex_shader_source_list, fragment_shader_source_list):
        # create program
        self.program= gl.glCreateProgram() # pylint: disable=E1111
        #print('create program ',self.program)
        printOpenGLError()

        # vertex shader
        #print('compile vertex shader...')
        self.vs = gl.glCreateShader(gl.GL_VERTEX_SHADER) # pylint: disable=E1111
        gl.glShaderSource(self.vs, vertex_shader_source_list)
        gl.glCompileShader(self.vs)
        if(gl.GL_TRUE!=gl.glGetShaderiv(self.vs, gl.GL_COMPILE_STATUS)):
    	    err =  gl.glGetShaderInfoLog(self.vs) 
            raise Exception(err)  
        gl.glAttachShader(self.program, self.vs)
        printOpenGLError()

        # fragment shader
        #print('compile fragment shader...')
        self.fs = gl.glCreateShader(gl.GL_FRAGMENT_SHADER) # pylint: disable=E1111
        gl.glShaderSource(self.fs, fragment_shader_source_list)
        gl.glCompileShader(self.fs)
        if(gl.GL_TRUE!=gl.glGetShaderiv(self.fs, gl.GL_COMPILE_STATUS)):
    	    err =  gl.glGetShaderInfoLog(self.fs) 
            raise Exception(err)       
        gl.glAttachShader(self.program, self.fs)
        printOpenGLError()

        #print('link...')
        gl.glLinkProgram(self.program)
        if(gl.GL_TRUE!=gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS)):
    	    err =  gl.glGetShaderInfoLog(self.vs) 
            raise Exception(err)          
        printOpenGLError()

    def begin(self):
        if gl.glUseProgram(self.program):
            printOpenGLError()

    def end(self):
        gl.glUseProgram(0)