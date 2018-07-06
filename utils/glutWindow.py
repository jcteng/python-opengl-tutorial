

import OpenGL.GLUT as oglut
import sys
import OpenGL.GL as gl
import OpenGL.GLU as glu
class GlutWindow(object):

    def init_opengl(self):
        gl.glClearColor(0.0,0,0.4,0)
        gl.glDepthFunc(gl.GL_LESS)
        gl.glEnable(gl.GL_DEPTH_TEST)
        
    def ogl_draw(self):
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        oglut.GLUT_KEY_UP
        glu.gluLookAt(4.0,3.0,-3.0, 
                0.0,0.0,0.0,
                0.0,1.0,0.0)
        #built in model
        oglut.glutSolidTeapot(1)

        print "please overrider ogl_draw" 
    def display(self):    
        self.ogl_draw()
        oglut.glutSwapBuffers()
    def idle(self):
        pass
    def resize(self,Width,Height):
        print "please overrider resize"
        gl.glViewport(0, 0, Width, Height)
        glu.gluPerspective(45.0, float(Width)/float(Height), 0.1, 1000.0)        

    def on_keyboard(self,key,x,y):     
        if(self.controller!=None):
              self.controller.on_keyboard(key,x,y)
        else:
            print "please overrider on_keyboard" 
    def on_special_key(self,key,x,y):     
        if(self.controller!=None):
              self.controller.on_special_key(key,x,y)
        else:
            print "please overrider on_keyboard"         
        
    def on_mouse(self,*args,**kwargs):
        if(self.controller!=None):
              self.controller.on_mouse(*args,**kwargs)
        else:        
            print "please overrider on_mouse" 
    def on_mousemove(self,*args,**kwargs):
        if(self.controller!=None):
              self.controller.on_mousemove(*args,**kwargs)
        else:                
            print "please overrider on_mousemove" 
                
    def __init__(self,*args,**kwargs):

        oglut.glutInit(sys.argv)
        oglut.glutInitDisplayMode(oglut.GLUT_RGBA | oglut.GLUT_DOUBLE | oglut.GLUT_DEPTH)
        oglut.glutInitWindowSize(800, 480)
        self.window = oglut.glutCreateWindow(b"window")
        oglut.glutDisplayFunc(self.display)
        #oglut.glutIdleFunc(self.display) 
        oglut.glutReshapeFunc(self.resize)  
        oglut.glutKeyboardFunc(self.on_keyboard)   
        oglut.glutSpecialFunc(self.on_special_key)  
        oglut.glutMouseFunc(self.on_mouse)
        oglut.glutMotionFunc(self.on_mousemove)
        self.controller = None
        self.update_if = oglut.glutPostRedisplay

    def run(self):
        oglut.glutMainLoop()



if __name__ == "__main__":

    win = GlutWindow()
    win.run()