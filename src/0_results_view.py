
import sys
from PySide6 import QtCore, QtWidgets, QtGui, QtUiTools
import numpy as np

class graphicsScene(QtWidgets.QGraphicsScene):
    def __init__ (self):#, parent=None):
        super(graphicsScene, self).__init__ ()#parent)

    def mousePressEvent(self, event):
        #super(graphicsScene, self).mousePressEvent(event)
        print(str(event.scenePos().x()) + " " +str(event.scenePos().y()))


class EyesWidget(QtWidgets.QWidget):
    def __init__(self, image):
        super().__init__()

        print("opening "+image)
        self.background = QtGui.QPixmap(image)
        width = self.background.size().width()
        height = self.background.size().height()
        #print("size: "+str(width)+" "+str(height))
        
        # configure scene & view
        self.scene = graphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.scene.addPixmap(self.background)

        # configure layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)

        # resize
        self.view.fitInView(QtCore.QRectF(0, 0, width/2, height/2), QtCore.Qt.KeepAspectRatio)

    # exit when space is pressed
    def keyPressEvent(self, event):
        super(EyesWidget, self).keyPressEvent(event)
        if event.key() == 32:
            sys.exit()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    myWidget = EyesWidget(sys.argv[1])
    myWidget.show()
    sys.exit(app.exec_())
