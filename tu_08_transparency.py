# import os,sys
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))


from OpenGL.GL import *  # pylint: disable=W0614

from utils.meshViewer import MeshViewWindow, meshWithRender
from utils.shaderLoader import Shader

import glm



from tu_07_basic_shading import basicShading

# no different with tutorial 07 , only changed shader
class AlphaShading(basicShading):

    def loadShader(self):
        self.shader = Shader()
        self.shader.initShaderFromGLSL(
            ["glsl/tu08/StandardShading.vertexshader.glsl"], ["glsl/tu08/StandardTransparentShading.fragmentshader.glsl"])
        self.MVP_ID = glGetUniformLocation(self.shader.program, "MVP")
        self.ModelMatrix_ID = glGetUniformLocation(self.shader.program, "M")
        self.ViewMatrix_ID = glGetUniformLocation(self.shader.program, "V")
        self.Texture_ID =  glGetUniformLocation(self.shader.program, "myTextureSampler")
        self.Light_ID =  glGetUniformLocation(self.shader.program, "LightPosition_worldspace")
        self.OFFSET_ID = glGetUniformLocation(self.shader.program, "LOCATION_OFFSET")

class AlphaEnabledWin(MeshViewWindow):
    def init_opengl(self):
        MeshViewWindow.init_opengl(self)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


if __name__ == "__main__":

    win = AlphaEnabledWin().init_default()    
    win.add_mesh(AlphaShading(meshName="resources/tu04/suzanne.obj",textureName="resources/tu04/uvmap.dds"))

    win.run()
