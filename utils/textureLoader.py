import os
import struct

from OpenGL.GL import *
from OpenGL.GL.EXT import texture_compression_s3tc
from OpenGL.raw import GL
from PIL import Image


class textureLoader(object):
    
    def loadDDS(self,fname):
        
        f = open(fname,'rb')
        ddstag =f.read(4)
        if(ddstag!="DDS "):
            raise Exception("invp'yild dds file") 
        head =  f.read(124)
        height, = self.height = struct.unpack( "I",head[8:12])
        width, = self.width = struct.unpack( "I",head[12:16])
        linearSize, = struct.unpack( "I",head[16:20])        
        mipMapCount,  = struct.unpack( "I",head[24:28])
        fourCC        = head[80:84]
        supported_DDS = ["DXT1","DXT3","DXT5"]

        if(not(fourCC in supported_DDS)):
            raise Exception("Not supported DDS file: %s"%fourCC)
        
        self.format = fourCC  
        
        #print "fourCC",fourCC
        if(fourCC=="DXT1"):
            components = 3
            blockSize  = 8
        else:
            components = 4
            blockSize  = 16
 

        if(fourCC=="DXT1")  :
            format = texture_compression_s3tc.GL_COMPRESSED_RGBA_S3TC_DXT1_EXT
        elif(fourCC=="DXT3") :  
            format = texture_compression_s3tc.GL_COMPRESSED_RGBA_S3TC_DXT3_EXT
        elif(fourCC=="DXT5")  :
            format = texture_compression_s3tc.GL_COMPRESSED_RGBA_S3TC_DXT5_EXT

        
        if(mipMapCount>1 ):
            bufferSize = linearSize*2
        else:
            bufferSize = linearSize
        #print bufferSize    
        ddsbuffer = f.read(bufferSize)
        offset = 0
        self.textureGLID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textureGLID)

        for level in range(0,mipMapCount):
            size = ((width+3)/4)*((height+3)/4)*blockSize
            glCompressedTexImage2D(GL_TEXTURE_2D, level, format, width, height,
            0, size, ddsbuffer[offset:offset+size])
            offset +=size
            width  /= 2
            height /= 2
            if(width==0 | height==0):
                #print "___",width,height,level,mipMapCount
                break
        self.inversedVCoords = True
        f.close()


    def loadByPIL(self,fname,mode):
        image = Image.open(fname)
        converted = image.convert(mode)        
        self.buffer = converted.transpose( Image.FLIP_TOP_BOTTOM ).tobytes()
        self.height = image.height
        self.width = image.width
        self.format = mode
        len(self.buffer)/(image.width*image.height)
        image.close()
        self.textureGLID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textureGLID)
        glTexImage2D(GL_TEXTURE_2D, 0,GL_RGB, self.width, self.height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.buffer)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)

    def __init__(self,fname,mode="RGB"):
        self.inversedVCoords = False
        fname =  os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__),".."),fname))
        if(fname.lower().endswith(".dds")):
            self.loadDDS(fname)
        else:
            self.loadByPIL(fname,mode)    
            
    def __len__(self):
        return len(self.buffer)
