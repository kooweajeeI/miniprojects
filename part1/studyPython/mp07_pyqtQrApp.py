# QRCODE PyQT app
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qrcode

# QRCode 커스터마이징 클래스
class Image(qrcode.image.base.BaseImage):
    def __init__(self, border, width, box_size) -> None:
        self.border = border
        self.width = width
        self.box_size = box_size
        # size 생성
        size = (width + border * 2) * box_size

        self._image = QImage(size, size, QImage.Format_RGB8)
        self._image.fill(Qt.white)  # 흰색

    def pixmap(self):
        return QPixmap.fromImage(self._image)


class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPython/qrcodeApp.ui', self)
        self.setWindowTitle('QrCode 생성앱 v0.1')

        # 시그널/슬롯
        self.btnQrGen.clicked.connect(self.btnQrGenClicked)
        self.txtQrData.returnPressed.connect(self.btnQrGenClicked) 
        self.setWindowIcon(QIcon('./studyPython/qr-code.png'))

    def btnQrGenClicked(self):
        data = self.txtQrData.text()

        if data == '':
            QMessageBox.warning(self, '경고', '데이터를 입력하세요')
            return
        
        else :
            qr_img = qrcode.make(data)
            qr_img.save('./studyPython/site.png')
            img = QPixmap('./studyPython/site.png')
            self.lblQrCode.setPixmap(QPixmap(img).scaledToWidth(300))





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())

