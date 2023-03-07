# QtDesigner로 디자인 사용
import sys
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *

class qtApp(QWidget):
    count = 0       # 클릭회수 카운트 변수
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/mainApp.ui',self)

        # Qt Designer에서 구성한 위젯시그널 만듦
        self.btnOK.clicked.connect(self.btnOKClicked)
        self.btnPOP.clicked.connect(self.btnPOPClicked)

    def btnOKClicked(self):     # 슬롯함수
        self.count += 1
        self.lblMessage.clear()
        self.lblMessage.setText(f'메시지: OK!! + {self.count}')

    def btnPOPClicked(self):
        QMessageBox.about(self,'popup','까꿍!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())