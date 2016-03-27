import sys
from PyQt4 import QtGui
import pyqtgraph as pg


class GraphApp(QtGui.QMainWindow):

    def __init__(self):
        super(GraphApp, self).__init__()
        self.initUI()


    def initUI(self):
        self.setCentralWidget(pg.PlotWidget())
        self.statusBar()
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Random Data')
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    ga = GraphApp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

