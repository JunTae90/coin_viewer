from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class CoinOrderBook(QWidget):
    def __init__(self, parent=None, top=False):
        QWidget.__init__(self, parent)
        if top:
            self.binanceLabel = QLabel(self)
            self.binanceLabel.setText("바이낸스")
            self.binanceLabel.setAlignment(Qt.AlignCenter)
            self.upbitLabel = QLabel(self)
            self.upbitLabel.setText("업비트")
            self.upbitLabel.setAlignment(Qt.AlignCenter)
            self.bithumbLabel = QLabel(self)
            self.bithumbLabel.setText("빗썸")
            self.bithumbLabel.setAlignment(Qt.AlignCenter)
        self.askLabel = QLabel(self)
        self.askLabel.setText("매도(가격/개수)")
        self.askLabel.setAlignment(Qt.AlignCenter)
        self.bidLabel = QLabel(self)
        self.bidLabel.setText("매수(가격/개수)")
        self.bidLabel.setAlignment(Qt.AlignCenter)
        self.curLabel = QLabel(self)
        self.curLabel.setText("체결(가격/프리미엄)")
        self.curLabel.setAlignment(Qt.AlignCenter)
        self.binanceAskLineEdit = QLineEdit(self)
        self.binanceAskLineEdit.setAlignment(Qt.AlignCenter)
        self.binanceBidLineEdit = QLineEdit(self)
        self.binanceBidLineEdit.setAlignment(Qt.AlignCenter)
        self.binanceCurLineEdit = QLineEdit(self)
        self.binanceCurLineEdit.setAlignment(Qt.AlignCenter)
        self.upbitAskLineEdit = QLineEdit(self)
        self.upbitAskLineEdit.setAlignment(Qt.AlignCenter)
        self.upbitBidLineEdit = QLineEdit(self)
        self.upbitBidLineEdit.setAlignment(Qt.AlignCenter)
        self.upbitCurLineEdit = QLineEdit(self)
        self.upbitCurLineEdit.setAlignment(Qt.AlignCenter)
        self.bithumbAskLineEdit = QLineEdit(self)
        self.bithumbAskLineEdit.setAlignment(Qt.AlignCenter)
        self.bithumbBidLineEdit = QLineEdit(self)
        self.bithumbBidLineEdit.setAlignment(Qt.AlignCenter)
        self.bithumbCurLineEdit = QLineEdit(self)
        self.bithumbCurLineEdit.setAlignment(Qt.AlignCenter)

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setHorizontalSpacing(2)
        self.layout.setVerticalSpacing(2)
        add = 0
        if top:
            self.layout.addWidget(self.binanceLabel, 0, 1)
            self.layout.addWidget(self.upbitLabel, 0, 2)
            self.layout.addWidget(self.bithumbLabel, 0, 3)
            add = 1
        self.layout.addWidget(self.askLabel, 0+add, 0)
        self.layout.addWidget(self.bidLabel, 1+add, 0)
        self.layout.addWidget(self.curLabel, 2+add, 0)
        self.layout.addWidget(self.binanceAskLineEdit, 0+add, 1)
        self.layout.addWidget(self.binanceBidLineEdit, 1+add, 1)
        self.layout.addWidget(self.binanceCurLineEdit, 2+add, 1)
        self.layout.addWidget(self.upbitAskLineEdit, 0+add, 2)
        self.layout.addWidget(self.upbitBidLineEdit, 1+add, 2)
        self.layout.addWidget(self.upbitCurLineEdit, 2+add, 2)
        self.layout.addWidget(self.bithumbAskLineEdit, 0+add, 3)
        self.layout.addWidget(self.bithumbBidLineEdit, 1+add, 3)
        self.layout.addWidget(self.bithumbCurLineEdit, 2+add, 3)

        for i in self.findChildren(QLineEdit):
            i.setReadOnly(True)
            i.setAlignment(Qt.AlignCenter)

    def setData(self, data):
        if "binance" in data.keys():
            binance_data = data["binance"]
            self.binanceAskLineEdit.setText(binance_data["ask"])
            self.binanceBidLineEdit.setText(binance_data["bid"])
            self.binanceCurLineEdit.setText(binance_data["price"])

        if "upbit" in data.keys():
            upbit_data = data["upbit"]
            self.upbitAskLineEdit.setText(upbit_data["ask"])
            self.upbitBidLineEdit.setText(upbit_data["bid"])
            self.upbitCurLineEdit.setText(upbit_data["price"]+"/"+str(data["upbit_premium"]))

        if "bithumb" in data.keys():
            bithumb_data = data["bithumb"]
            self.bithumbAskLineEdit.setText(bithumb_data["ask"])
            self.bithumbBidLineEdit.setText(bithumb_data["bid"])
            self.bithumbCurLineEdit.setText(bithumb_data["price"]+"/"+str(data["bithumb_premium"]))

    def clear(self):
        for i in self.findChildren(QLineEdit):
            i.clear()

class CoinWidget(QWidget):
    delSignal = pyqtSignal(str)
    def __init__(self, parent=None, top=False):
        QWidget.__init__(self, parent)
        self.symbolLabel = QLabel(self)
        self.symbolLabel.setAlignment(Qt.AlignVCenter)
        self.symbolLabel.setFixedWidth(50)
        self.symbolShow = QRadioButton(self)
        self.symbolShow.setText("show")
        self.symbolShow.setChecked(True)
        self.symbolHide = QRadioButton(self)
        self.symbolHide.setText("hide")
        self.symbolHide.setChecked(False)
        self.deleteBtn = QPushButton(self)
        self.deleteBtn.setText("삭제")

        self.symbolFrame = QFrame()
        self.symbolFrame.setFrameShape(QFrame.Box)
        self.symbolFrame.setFrameShadow(QFrame.Plain)

        self.symbolLayout = QHBoxLayout(self.symbolFrame)
        self.symbolLayout.setContentsMargins(0, 0, 0, 0)
        self.symbolLayout.addWidget(self.symbolLabel)
        self.symbolLayout.addWidget(self.symbolShow)
        self.symbolLayout.addWidget(self.symbolHide)
        self.symbolLayout.addWidget(self.deleteBtn)

        self.orderbook = CoinOrderBook(self, top)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)
        self.layout.addWidget(self.symbolFrame)
        self.layout.addWidget(self.orderbook)
        self.layout.setAlignment(Qt.AlignLeft)

        self.symbolShow.clicked.connect(self.radioButtonFunction)
        self.symbolHide.clicked.connect(self.radioButtonFunction)

        self.deleteBtn.clicked.connect(self.emitDelete)

    def radioButtonFunction(self):
        if self.symbolShow.isChecked():
            self.orderbook.show()

        elif self.symbolHide.isChecked():
            self.orderbook.hide()

    def setData(self, symbol, data):
        self.symbolLabel.setText(symbol)
        self.orderbook.setData(data)

    def clear(self):
        self.symbolLabel.clear()
        self.orderbook.clear()

    def emitDelete(self):
        self.delSignal.emit(self.symbolLabel.text())

class MainWidget(QWidget):
    def __init__(self, parent=None, num = 10):
        QWidget.__init__(self, parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        for i in range(num):
            if not i:
                self.coinWidget = CoinWidget(top=True)
            else:
                self.coinWidget = CoinWidget()

            self.coinWidget.setObjectName("coin_widget_{}".format(i))
            self.layout.addWidget(self.coinWidget)