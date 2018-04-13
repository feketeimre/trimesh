"""
load a textured obj file
not testet thoroughly
"""
import numpy
import trimesh
from PIL import Image

#trimesh viewer needs some extra work to display textures 
#from trimesh.scene.viewer import SceneViewer
#from trimesh.scene import Scene

#use pg gl for now
from pyqtgraph.Qt import QtGui, QtCore, QtOpenGL
import pyqtgraph.opengl as gl

from OpenGL.GL import *
from pyqtgraph.opengl.GLGraphicsItem import GLGraphicsItem
#quick and dirty textured mesh
class texturedMesh(GLGraphicsItem):
    def __init__(self, v,t,i):
		GLGraphicsItem.__init__(self)
		self.setGLOptions("opaque")
		self.v, self.t, self.i = v, t, i
		self.glTexture = None

    def paint(self):
		self.setupGLState()
  		glEnableClientState(GL_VERTEX_ARRAY)
		glVertexPointerf(self.v)

		if self.glTexture is None:
            #gen texture for gl if does not exist
			self.glTexture = glGenTextures(1)
			glBindTexture( GL_TEXTURE_2D, self.glTexture )
			glPixelStorei(GL_UNPACK_ALIGNMENT,1)
			glTexImage2D(GL_TEXTURE_2D, 0, 3, self.i.shape[0], self.i.shape[1], 0, GL_RGB, GL_UNSIGNED_BYTE, self.i)


		glClientActiveTexture(GL_TEXTURE0)
		glEnableClientState(GL_TEXTURE_COORD_ARRAY)
		glTexCoordPointer(2, GL_FLOAT, 0, self.t)
		glEnable(GL_TEXTURE_2D)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

		glBindTexture(GL_TEXTURE_2D, self.glTexture)


		glDrawArrays(GL_TRIANGLES, 0, numpy.product(self.v.shape[:-1]))
		glDisableClientState(GL_VERTEX_ARRAY)
		glDisableClientState(GL_TEXTURE_COORD_ARRAY)
		glDisable(GL_TEXTURE_2D)
    

#grab example obj and texture from:
#http://paulbourke.net/dataformats/obj/minobj.html
#load obj with trimesh
x = trimesh.load_mesh(r"capsule.obj")
tex = Image.open("capsule0.jpg")

tex = numpy.asarray(tex.convert('RGB'))
#capsule0.jpg is not a square image, thats why we halve ::2 one dim
# also its flipped thats why we ::-1
tex = tex.copy()[::-1,::2,:] 

v = numpy.array(x.vertices)
f = numpy.array(x.faces)

#texcoords
vt = numpy.array(x.visual.uv_vertices)
ft = numpy.array(x.visual.uv_faces)
#load texture
x.visual.texture = tex


#trimesh viewer needs some extra work to display textures 
#s = Scene()
#s.add_geometry(x)
#SceneViewer(s, smooth=False)

#use pg gl for now
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()

m = texturedMesh(v[f], vt[ft], tex)
w.addItem(m)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()