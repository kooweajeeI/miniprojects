# QtDesigner로 디자인 사용
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from NaverApi import *
import webbrowser
# import urllib
from urllib.request import urlopen


class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/naverApiMovie.ui', self)
        self.setWindowIcon(QIcon('./studyPyQt/newspaper.png'))

        # 검색 버튼 클릭시그널 / 슬롯함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        # 검색어 입력 후 엔터를 치면 처리
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)

        self.tblResult.doubleClicked.connect(self.tblResultDoubleClicked)

    def tblResultDoubleClicked(self):
        # row = self.tblResult.currentIndex().row()
        # column = self.tblResult.currentIndex().column()
        # print(row,column)
        selected = self.tblResult.currentRow()
        url = self.tblResult.item(selected, 5).text()
        webbrowser.open(url)

    def btnSearchClicked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self, '경고', '영화명을 입력하세요')
            return

        else:
            api = NaverApi()        # NaverApi 클래스 객체 생성
            node = 'movie'           # movie로 변경하면 영화검색
            outputs = []            # 결과 담을 리스트 변수
            display = 100

            result = api.get_naver_search(node, search, 1, display)
            # print(result)
            # 테이블위젯에 출력
            items = result['items']    # json결과 중 items 아래 배열만 추출
            self.makeTable(items)      # 테이블위젯에 데이터들을 할당 함수

    # 테이블 위젯에 데이터 표시 -- 네이버 영화 결과 변경
    def makeTable(self, items) -> None:
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblResult.setColumnCount(7)
        self.tblResult.setRowCount(len(items))      # 현재(100개) 행 생성
        self.tblResult.setHorizontalHeaderLabels(
            ['영화제목', '개봉연도', '감독', '배우진', '평점', '영화링크', '포스터'])
        self.tblResult.setColumnWidth(0, 150)
        self.tblResult.setColumnWidth(1, 50)
        self.tblResult.setColumnWidth(2, 100)
        self.tblResult.setColumnWidth(3, 200)
        self.tblResult.setColumnWidth(4, 50)
        self.tblResult.setColumnWidth(5, 200)

        self.tblResult.setEditTriggers(
            QAbstractItemView.NoEditTriggers)      # 컬럼데이터 수정금지

        for i, post in enumerate(items):
            title = self.replaceHtmlTag(post['title'])      # HTML 특수문자 변환
            pubDate = post['pubDate']
            link = post['link']
            director = self.replaceHtmlTag(post['director'])
            actor = self.replaceHtmlTag(post['actor'])
            userRating = post['userRating']
            image = post['image']
        
            if image != '':
                img_data = urlopen(image).read()
                pixmap = QPixmap()
                pixmap.loadFromData(img_data)
                imgLabel = QLabel()
                imgLabel.setPixmap(pixmap)
                self.tblResult.setCellWidget(i, 6, imgLabel)
                # print('사진있음')
                # print(image)
            # else:
            #     print('사진없음')
            #     print(image)

            # setItem(행, 컬럼, 넣을데이터)            
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(pubDate))
            self.tblResult.setItem(i, 2, QTableWidgetItem(director))
            self.tblResult.setItem(i, 3, QTableWidgetItem(actor))
            self.tblResult.setItem(i, 4, QTableWidgetItem(userRating))
            self.tblResult.setItem(i, 5, QTableWidgetItem(link))
            # self.tblResult.setItem(i, 6, QTableWidgetItem(image))
            
            


    def txtSearchReturned(self):
        self.btnSearchClicked()

    def replaceHtmlTag(self, result) -> str:
        result = result.replace('&lt;', '<')      # lesser than
        result = result.replace('&gt;', '>')       # greater than
        result = result.replace('<b>', '')         # bold
        result = result.replace('</b>', '')
        result = result.replace('&apos;', "'")      # apostrophe 홑따옴표
        result = result.replace('&quot;', '"')      # quotation mark 쌍따옴표
        result = result.replace('&amp;', '&')
        result = result.replace('|', '.')

        # 변환되지않은 특수문자가 나타나면 추가

        return result


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())
