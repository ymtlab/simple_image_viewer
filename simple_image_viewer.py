# -*- coding: utf-8 -*-
import sys
from mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._numScheduledScalings = 0
        self.ui.graphicsView.wheelEvent = self.wheelEvent

    def exec_context_menu(self, point):
        self.menu = QtWidgets.QMenu(self)
        self.menu.addAction('Close', self.close)
        self.menu.exec( self.focusWidget().mapToGlobal(point) )

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            event.accept()
            return
        event.ignore()

    def dropEvent(self, event):
        event.accept()
        path = event.mimeData().urls()[0]
        pixmap = QtGui.QPixmap(path.toLocalFile())
        pixmap_item = QtWidgets.QGraphicsPixmapItem(pixmap)
        pixmap_item.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable)
        scene = QtWidgets.QGraphicsScene(self)
        scene.addItem(pixmap_item)
        self.ui.graphicsView.setScene(scene)
        self.ui.graphicsView.scale(1.0, 1.0)

    def wheelEvent(self, event):
        numDegrees = event.angleDelta().y() / 8
        numSteps = numDegrees / 15
        self._numScheduledScalings += numSteps
        if self._numScheduledScalings * numSteps < 0:
            self._numScheduledScalings = numSteps
        anim = QtCore.QTimeLine(350, self)
        anim.setUpdateInterval(20)
        anim.valueChanged.connect(self.scalingTime)
        anim.finished.connect(self.animFinished)
        anim.start()

    def scalingTime(self, x):
        factor = 1.0 + float(self._numScheduledScalings) / 300.0
        self.ui.graphicsView.scale(factor, factor)

    def animFinished(self):
        if self._numScheduledScalings > 0:
            self._numScheduledScalings -= 1
        else:
            self._numScheduledScalings += 1

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
 
if __name__ == '__main__':
    main()
