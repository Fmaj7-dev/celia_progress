
import sys
from PySide6 import QtCore, QtWidgets, QtGui, QtUiTools
import numpy as np
from PIL import Image, ExifTags

class graphicsScene(QtWidgets.QGraphicsScene):
    def __init__ (self, imagename):#, parent=None):
        super(graphicsScene, self).__init__ ()#parent)

        self.imagename = imagename

        # state
        self.lacrimal1 = None
        self.lacrimal2 = None

    def mousePressEvent(self, event):
        #super(graphicsScene, self).mousePressEvent(event)
        #print(str(event.scenePos().x()) + " " +str(event.scenePos().y()))

        if self.lacrimal1 == None:
            print ("storing lacrimal1")
            self.lacrimal1 = event.scenePos()
        else:
            print ("storing lacrimal2")
            self.lacrimal2 = event.scenePos()

    def write(self):
        f = open(self.imagename + ".txt", "w")
        f.write( str(int(self.lacrimal1.x())) + "\n" +str(int(self.lacrimal1.y())) +"\n")
        f.write( str(int(self.lacrimal2.x())) + "\n" +str(int(self.lacrimal2.y())) )
        f.close()

class EyesWidget(QtWidgets.QWidget):
    def __init__(self, imagename):
        super().__init__()

        print("opening "+imagename)
        self.background = QtGui.QPixmap(imagename)

        # fucking exif tag
        image=Image.open(imagename)

        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        
        exif = image._getexif()

        angle = 0
        if exif is not None:
            if exif[orientation] == 3:
                angle = 180
            elif exif[orientation] == 6:
                angle = 270
            elif exif[orientation] == 8:
                angle = 90
        else:
            print("no exif data found")

        print("exif: angle "+str(angle))
        rotation = QtGui.QTransform().rotate(-angle)
        self.background = self.background.transformed(rotation)

        
        width = self.background.size().width()
        height = self.background.size().height()
        print("size: "+str(width)+" "+str(height))
        
        # configure scene & view
        self.scene = graphicsScene(imagename) #QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.scene.addPixmap(self.background)
        #self.view.resize(self.background.size().width(), self.background.size().height() )

        # configure layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)

        # resize
        #self.resize(self.background.size().width(), self.background.size().height() )
        #self.resize(1200, 800)
        self.view.fitInView(QtCore.QRectF(0, 0, width/2, height/2), QtCore.Qt.KeepAspectRatio)

    # exit when space is pressed
    def keyPressEvent(self, event):
        super(EyesWidget, self).keyPressEvent(event)
        if event.key() == 32:
            self.scene.write()
            sys.exit()
        else:
            sys.exit()

    # print mouse position
    def mousePressEvent(self, QMouseEvent):
        print(QMouseEvent.pos())

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    myWidget = EyesWidget(sys.argv[1])
    myWidget.show()
    sys.exit(app.exec_())
