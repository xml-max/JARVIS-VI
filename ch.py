from PyQt5.QtWidgets import QApplication
from choice import ChoiceWindow

def get_user_input():
    app = QApplication([])
    choice_window = ChoiceWindow()
    choice_window.show()
    app.exec_()
    if choice_window.choice is None:
        return "EXIT"
    else:
        return choice_window.choice


