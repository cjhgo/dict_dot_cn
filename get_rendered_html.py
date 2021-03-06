#coding: utf-8
#created at 16-10-26 17:47


from PyQt5.QtCore import QUrl
from PyQt5.QtWebKitWidgets import QWebView, QWebPage
from PyQt5.QtCore import QTimer
from bs4 import BeautifulSoup





class MMyWebPage(object):
    @staticmethod
    def instance(webview):
        if not hasattr(MyWebPage, "_instance"):
            MMyWebPage._instance = MMyWebPage(webview)
        return MMyWebPage._instance

    def __init__(self, webview, *args, **kwargs):
        super(MMyWebPage, self).__init__(*args, **kwargs)
        self.webview = webview
        self.webpage = QWebPage()
        self.webpage.loadFinished.connect(self.on_loadFinished)

    def set_content(self, url):
        self.content = ''
        self.result = False
        self.qurl = QUrl(url)
        self.webpage.mainFrame().load(self.qurl)


    def on_loadFinished(self, result):
        self.result = result
        if result:
            self.frame = self.webpage.mainFrame()
            self.content = self.frame.toHtml()
            doc = BeautifulSoup(self.content, 'lxml')
            temp = doc.find('div', class_='word')
            try:
                # adcontent = temp.find("div", class_="basic clearfix").find("ul", class_="dict-basic-ul").findAll('li')[-1]
                # adcontent.replaceWith('')
                adcontent = temp.find("div", class_="basic clearfix").find("ul").findAll('li')[-1]
                adcontent.replaceWith('')
            except:
                pass
            finally:
                self.webview.setHtml(str(temp))
                # with open('temp.html', 'w') as f:
                #     f.write(str(temp))

    @property
    def get_content(self):
        doc = BeautifulSoup(self.content, 'lxml')
        self.content = doc.find('div', class_='word')
        return self.content

class MyWebPage(QWebPage):
    # @staticmethod
    # def instance():
    #     if not hasattr(MyWebPage, "_instance"):
    #         MyWebPage._instance = MyWebPage()
    #     return MyWebPage._instance

    def __init__(self, url, widget, *args, **kwargs):
        super(MyWebPage, self).__init__(*args, **kwargs)
        self.content = ''
        self.result = False
        self.qurl = QUrl(url)
        self.loadFinished.connect(self.on_loadFinished)
        self.mainFrame().load(self.qurl)
        self.widget = widget

    def on_loadFinished(self, result):
        self.result = result
        if result:
            self.frame = self.mainFrame()
            self.content = self.frame.toHtml()
            doc = BeautifulSoup(self.content, 'lxml')
            temp = doc.find('div', class_='word')
            try:
                # adcontent = temp.find("div", class_="basic clearfix").find("ul", class_="dict-basic-ul").findAll('li')[-1]
                # adcontent.replaceWith('')
                adcontent = temp.find("div", class_="basic clearfix").find("ul").findAll('li')[-1]
                adcontent.replaceWith('')
            except:
                pass
            finally:
                if str(temp):
                    self.widget.webview.setHtml(str(temp))
                    if self.widget.windowOpacity() == 1:
                        self.widget.show()
                        self.widget.setWindowOpacity(0.98)
                        QTimer.singleShot(3000, lambda: self.widget.fadeout(1))
            # with open('temp.html', 'w') as f:
            #     f.write(str(temp))
    @property
    def get_content(self):
        doc = BeautifulSoup(self.content, 'lxml')
        self.content = doc.find('div', class_='word')
        return self.content



