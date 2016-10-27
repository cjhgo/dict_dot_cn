#coding: utf-8
#created at 16-10-26 17:47


from PyQt5.QtCore import QUrl
from PyQt5.QtWebKitWidgets import QWebView, QWebPage

from bs4 import BeautifulSoup



class MyWebPage(QWebPage):
    def __init__(self, url, webview, *args, **kwargs):
        super(QWebPage, self).__init__(*args, **kwargs)
        self.content = ''
        self.result = False
        self.qurl = QUrl(url)
        self.loadFinished.connect(self.on_loadFinished)
        self.mainFrame().load(self.qurl)
        self.webview = webview

    def on_loadFinished(self, result):
        print 'process on loadfinished'
        self.result = result
        if result:
            self.frame = self.mainFrame()
            self.content = self.frame.toHtml()

            doc = BeautifulSoup(self.content, 'lxml')
            temp = doc.find('div', class_='word')
            # print self.content
            self.webview.setHtml(str(temp))

            with open('temp.html', 'w') as f:
                f.write(str(temp))
    @property
    def get_content(self):
        doc = BeautifulSoup(self.content, 'lxml')
        self.content = doc.find('div', class_='word')
        return self.content



