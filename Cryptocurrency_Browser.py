from bs4 import BeautifulSoup
from PyQt5 import QtWidgets, QtCore, QtGui
import requests
import sys
import datetime
import webbrowser
from requests.exceptions import ConnectionError
import os
class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
    
        self.init_ui()
        self.setTheme()
        self.coinScraping()
        self.setWindowTitle("Crypto Browser")
        
    def init_ui(self):
        
        ## Menu bar area. ################################################
        bar = QtWidgets.QMenuBar()
        file = bar.addMenu('File')
        about = bar.addMenu('About')
        
        goGitub_page = about.addAction('Author')
        saveData = file.addAction('Save As Text File')
        close_app = file.addAction('Exit')
        
        ## Short cuts.
        close_app.setShortcut("CTRL+Q")
        saveData.setShortcut("CTRL+S")
        goGitub_page.setShortcut("CTRL+A")
        
        ## Actions.
        goGitub_page.triggered.connect(self.browseMyGithubPage)
        saveData.triggered.connect(self.saveDataAsText)
        close_app.triggered.connect(self.closeApp)
        
        ###################################################################
        
        
        ## A timer for refresh data. Every 30 seconds, refresh function run.
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(30000)
        self.refreshingAnnouncement = QtWidgets.QLabel("Not refreshed yet")
        
        # A message box for giving error/information message.
        self.msgBox = QtWidgets.QMessageBox()
        
        ## Widgets.
        self.coins_combobox = QtWidgets.QComboBox()
        self.coinTitle = QtWidgets.QLabel("Coin Not Selected")
        self.coinPrice_label = QtWidgets.QLabel("Price:")
        self.coinMarketCap_label = QtWidgets.QLabel("Market Cap:")
        self.coinVolume24_label = QtWidgets.QLabel("Volume (24h):")
        self.coinCirculatingSupply_label = QtWidgets.QLabel("Circulating Supply:                                                   ")
        
        ## These will get data which come from data scraping.
        self.coinPrice = QtWidgets.QLabel("no data")
        self.coinMarketCap = QtWidgets.QLabel("no data")
        self.coinVolume24h = QtWidgets.QLabel("no data")
        self.coinCirculatingSupply = QtWidgets.QLabel("no data")
        
        ## Two buttons for actions.
        self.confirmButton = QtWidgets.QPushButton("Confirm")
        self.showGraphButton = QtWidgets.QPushButton("Open TradingView")
            
    
        ## Some alignments.
        self.coinTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.refreshingAnnouncement.setAlignment(QtCore.Qt.AlignCenter)
        
        ## Layout adjustments.
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(bar)
        vbox.addWidget(self.coins_combobox)
        vbox.addWidget(self.coinTitle)
        vbox.addWidget(self.coinPrice_label)
        vbox.addWidget(self.coinPrice)
        vbox.addWidget(self.coinMarketCap_label)
        vbox.addWidget(self.coinMarketCap)
        vbox.addWidget(self.coinVolume24_label)
        vbox.addWidget(self.coinVolume24h)
        vbox.addWidget(self.coinCirculatingSupply_label)
        vbox.addWidget(self.coinCirculatingSupply)
        vbox.addWidget(self.confirmButton)
        vbox.addWidget(self.showGraphButton)
        vbox.addWidget(self.refreshingAnnouncement)
        
        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch()
        hbox.addLayout(vbox)
        hbox.addStretch()

        ## Buttons are connecting their functions.
        self.confirmButton.clicked.connect(self.bringData)
        self.showGraphButton.clicked.connect(self.showGraph)
        
        ## UI loaded.
        self.setLayout(hbox)
        self.show()
    
    def coinScraping(self):
        ## We take data right here. Try-except is for handle connection error.
        try:
            page = requests.get('https://coinmarketcap.com')
            soup = BeautifulSoup(page.content, 'html.parser')
            c_table = soup.find(class_='col-xl-10 padding-top-1x')
            the_currencies = c_table.find(class_='table-fixed-column-mobile compact-name-column')
            self.name = the_currencies.find_all(class_='currency-name-container link-secondary')
            self.price = the_currencies.find_all(class_='price')
            self.market_cap = the_currencies.find_all(class_='no-wrap market-cap text-right')
            self.volume24h = the_currencies.find_all(class_='volume')
            self.circulatingSupply = the_currencies.find_all(class_='no-wrap text-right circulating-supply')
             
            for k in range(0,100):
                
                self.coins_combobox.addItems([self.name[k].get_text()])
                ## Put coin names into the coins_combobox.
            
        except ConnectionError:
            self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            self.msgBox.setText("No connection! Check your internet connection please.")
            self.msgBox.setWindowTitle("An error occured.")
            self.msgBox.exec_()
            
    def bringData(self):
        
        ## Show all coin data to user.
        currentIndex = self.coins_combobox.currentIndex()
        self.coinTitle.setText(" ".join(self.name[currentIndex].get_text().split()))
        self.coinPrice.setText(" ".join(self.price[currentIndex].get_text().split()))
        self.coinMarketCap.setText(" ".join(self.market_cap[currentIndex].get_text().split()))
        self.coinVolume24h.setText(" ".join(self.volume24h[currentIndex].get_text().split()))
        self.coinCirculatingSupply.setText(" ".join(self.circulatingSupply[currentIndex].get_text().split()))
        
        ## When data come, we change the color to white. It was red first.
        self.coinMarketCap.setStyleSheet("QLabel {color: white;}")
        self.coinPrice.setStyleSheet("QLabel {color: white;}")
        self.coinVolume24h.setStyleSheet("QLabel {color: white;}")
        self.coinCirculatingSupply.setStyleSheet("QLabel {color: white;}")
        
    def refresh(self):
        now = datetime.datetime.now() ## to show refreshed moment, getting datetime.now()
        self.refreshingAnnouncement.setText(now.strftime("Refreshed %H:%M")) ## and show it.
        
        self.coinScraping() # calling that function again that way we keep data fresh.
        self.bringData()    # and that one too. (Not very necessary though.)
        
    def showGraph(self):
        ## Open tradingview website in default browser. Try-except is for handle connection error.
        try:
            self.currentText = self.coins_combobox.currentText() ## We take coin name right here.
            
            if self.currentText == "Bitcoin":
                url = "https://www.tradingview.com/chart/?symbol=BITFINEX%3ABTCUSD"
                webbrowser.get('windows-default').open(url)
            
            elif self.currentText == "Ethereum":
                url = "https://www.tradingview.com/chart/?symbol=POLONIEX%3AETHUSD"
                webbrowser.get('windows-default').open(url)
            
            elif self.currentText == "XRP":
                url = "https://www.tradingview.com/chart/?symbol=POLONIEX%3AXRPUSD"
                webbrowser.get('windows-default').open(url)
            
            elif self.currentText == "Litecoin":
                url = "https://www.tradingview.com/chart/?symbol=POLONIEX%3ALTCUSD"
                webbrowser.get('windows-default').open(url)
                
            elif self.currentText == "EOS":
                url = "https://www.tradingview.com/chart/?symbol=BITFINEX%3AEOSUSD"
                webbrowser.get('windows-default').open(url)
                
            elif self.currentText == "TRON":
                url = "https://www.tradingview.com/chart/?symbol=BITFINEX%3ATRXUSD"
                webbrowser.get('windows-default').open(url)
                
            elif self.currentText == "IOTA":
                url = "https://www.tradingview.com/chart/?symbol=BITFINEX%3AIOTUSD"
                webbrowser.get('windows-default').open(url)
            else:
                self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                self.msgBox.setText("Sorry! {} has no graph for now.".format(self.currentText))
                self.msgBox.setWindowTitle("Warning")
                self.msgBox.exec_()
        except:
            self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            self.msgBox.setText("No connection! Check your internet connection please.")
            self.msgBox.setWindowTitle("An error occured.")
            self.msgBox.exec_()
            
    def setTheme(self):
        
        ## Font settings.
        self.coinLabels_Font = QtGui.QFont("Trebuchet MS", 11, QtGui.QFont.Bold)
        self.coinName_Font = QtGui.QFont("Corbel", 15, QtGui.QFont.Bold)
        self.data_font = QtGui.QFont("Trebuchet MS", 9, QtGui.QFont.Bold)
        self.buttons_Font = QtGui.QFont("Trebuchet MS", 11, QtGui.QFont.Bold)
        
        self.coinCirculatingSupply_label.setFont(self.coinLabels_Font)
        self.coinMarketCap_label.setFont(self.coinLabels_Font)
        self.coinPrice_label.setFont(self.coinLabels_Font)
        self.coinVolume24_label.setFont(self.coinLabels_Font)
        self.coinTitle.setFont(self.coinName_Font)
        self.coins_combobox.setFont(self.buttons_Font)
        self.coinMarketCap.setFont(self.data_font)
        self.coinPrice.setFont(self.data_font)
        self.coinVolume24h.setFont(self.data_font)
        self.coinCirculatingSupply.setFont(self.data_font)
        self.confirmButton.setFont(self.buttons_Font)
        self.showGraphButton.setFont(self.buttons_Font)
        
        self.coinCirculatingSupply_label.setStyleSheet("QLabel {color: #F39C12;}")
        self.coinMarketCap_label.setStyleSheet("QLabel {color: #F39C12;}")
        self.coinPrice_label.setStyleSheet("QLabel {color: #F39C12;}")
        self.coinVolume24_label.setStyleSheet("QLabel {color: #F39C12;}")
        self.coinTitle.setStyleSheet("QLabel {color: #00F0FF;}")
        self.refreshingAnnouncement.setStyleSheet("QLabel {color: white;}")
        self.coinMarketCap.setStyleSheet("QLabel {color: #FF0000;}")
        self.coinPrice.setStyleSheet("QLabel {color: #FF0000;}")
        self.coinVolume24h.setStyleSheet("QLabel {color: #FF0000;}")
        self.coinCirculatingSupply.setStyleSheet("QLabel {color: #FF0000;}")
        self.confirmButton.setStyleSheet("QPushButton {background: #444444; color: #FFE400;}")
        self.showGraphButton.setStyleSheet("QPushButton {background: #444444; color: #FFE400;}")
            
            
            
    def browseMyGithubPage(self):
            url = "https://github.com/ethemguner"
            webbrowser.get('windows-default').open(url)
    
    def saveDataAsText(self):
        
        currentIndex = self.coins_combobox.currentIndex()
        now = datetime.datetime.now()
                
        with open("Save_File_{}.txt".format(now.strftime("%d-%m-%y_%H-%M-%S")), 'w') as f:
           f.write("### Coin: {}\n".format(self.name[currentIndex].get_text().split()))
           f.write("### Price: {}\n".format(" ".join(self.price[currentIndex].get_text().split())))
           f.write("### Market Cap: {}\n".format(" ".join(self.market_cap[currentIndex].get_text().split())))
           f.write("### Volume (24h): {}\n".format(" ".join(self.volume24h[currentIndex].get_text().split())))
           f.write("### Circulating Supply: {}\n".format(" ".join(self.circulatingSupply[currentIndex].get_text().split())))
    
        f.close()
        
        fileName = "Save_File_{}.txt".format(now.strftime("%d-%m-%y_%H;%M;%S"))
        os.startfile(fileName)
        
        
        
    def closeApp(self):
        sys.exit(app.exec_())
        
app = QtWidgets.QApplication(sys.argv)
window = Window()
window.move(700, 120)
app.setStyle("Fusion")
window.setFixedSize(270, 400)
window.setStyleSheet("Window {background : #073D5B;}")
sys.exit(app.exec_())
