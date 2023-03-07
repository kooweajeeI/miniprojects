# QtDesigner로 디자인 사용
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from NaverApi import *


class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/naverApiSearch.ui', self)

        # 검색 버튼 클릭시그널 / 슬롯함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        # 검색어 입력 후 엔터를 치면 처리
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)

    def btnSearchClicked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self, '경고', '검색어를 입력하세요')
            return

        else:
            api = NaverApi()        # NaverApi 클래스 객체 생성
            node = 'news'           # movie로 변경하면 영화검색
            outputs = []            # 결과 담을 리스트 변수
            display = 100

            result = api.get_naver_search(node, search, 1, display)
            # print(result)
            # ListView에 출력
            while result != None and result['display'] != 0:
                for post in result['items']:    # 100개의 post
                    api.get_post_data(post, outputs)    # NaverApi 클래스에서 처리
                    


    def txtSearchReturned(self):
        self.btnSearchClicked()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())
