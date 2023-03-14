import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from gtts import gTTS
from playsound import playsound
# from mpyg321.mpyg321 import MPyg321Player
# import os
import time


class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPython/ttsApp.ui', self)
        self.setWindowTitle('텍스트 투 스피치 v0.3')
        # self.setWindowIcon(QIcon('./studyPython/settings.png'))

        self.btnQrGen.clicked.connect(self.btnQrGenClicked)
        self.txtQrData.returnPressed.connect(self.btnQrGenClicked)

    def btnQrGenClicked(self):
        text = self.txtQrData.text()
        # player = MPyg321Player()

        if text == '':
            QMessageBox.warning(self, '경고', '텍스트를 입력하세요')
            return
        
        tts = gTTS(text=text, lang='ko', slow = False)
        tts.save('./studyPython/output/hi.mp3')
        time.sleep(1)
        # player.play_song('./studyPython/output/hi.mp3')
        playsound('./studyPython/output/hi.mp3')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())