from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class ChoiceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Choose Device to get mic input from')
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        btn_phone = QPushButton('Phone')
        btn_phone.clicked.connect(lambda: self.return_choice(1))

        btn_pc = QPushButton('PC')
        btn_pc.clicked.connect(lambda: self.return_choice(0))

        btn_spc = QPushButton("Typing in shell")
        btn_spc.clicked.connect(lambda: self.return_choice(2))

        layout.addWidget(btn_phone)
        layout.addWidget(btn_pc)
        layout.addWidget(btn_spc)

        self.setLayout(layout)

    def return_choice(self, choice):
        self.choice = choice
        self.close()
