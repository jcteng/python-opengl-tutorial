
import os
class objLoader(object):

    def __init__(self,fname):
        fname =  os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__),".."),fname))
        f = open(fname,"r") # in text mode

        self.vertexs = []
        self.indices = []
        self.normals = []
        self.texcoords = []

        for line in f:
            if line.startswith('#'): continue
            items = line.split()

            if(items[0]=="v"):
                v = map(float, items[1:4])
                self.vertexs.extend(v)
            elif(items[0]=="vn"):
                v = map(float, items[1:4])
                self.normals.extend(v)
            elif(items[0]=="vt"):
                v = map(float, items[1:3])
                self.texcoords.extend(v)
            elif(items[0]=="f"):
                index = map(int,items[1].split("/"))
                self.indices.extend(index)  
                index = map(int,items[2].split("/"))
                self.indices.extend(index)
                index = map(int,items[3].split("/"))
                self.indices.extend(index)
            elif(items[0]=="s"):               
                self.smooth = items[1] 
            elif(items[0]=="mtllib"):   
                self.referenceMaterials = items[1]
            elif(items[0]=="usemtl"):   
                self.Materials = items[1]
            else:
                print "skip unknown line : %s"%line[0:-1]          
    def to_array_style(self):
        class Container(object):
            pass
        outobj = Container()
        outobj.vertexs=[]
        outobj.texcoords = []
        outobj.normals = []

        for i in range(0,len(self.indices),3):
            index = 3*(self.indices[i]-1)            
            outobj.vertexs.extend(self.vertexs[index:index+3])
            index = 2*(self.indices[i+1]-1)
            outobj.texcoords.extend(self.texcoords[index:index+2])
            index = 3*(self.indices[i+2]-1)
            outobj.normals.extend(self.normals[index:index+3])

        return outobj



    def to_single_index_style(self):
        class Container(object):
            pass                
        outobj = Container()
        outobj.vertexs=[]
        outobj.texcoords = []
        outobj.normals = []
        outobj.indices = []
        combinations = []
        for i in range(0,len(self.indices),3):
            point = self.indices[i:i+3]
            if(point in combinations):
                pass
            else:
                combinations.append(point)
                index = 3*(self.indices[i]-1)            
                outobj.vertexs.extend(self.vertexs[index:index+3])
                index = 2*(self.indices[i+1]-1)
                outobj.texcoords.extend(self.texcoords[index:index+2])
                index = 3*(self.indices[i+2]-1)
                outobj.normals.extend(self.normals[index:index+3])                
            newindex = combinations.index(point)
            outobj.indices.append(newindex)
        return outobj
#print objLoader("resources/tu03/cube.obj").vertexs  

