import sys
from postgres_cursor import db_cursor
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Bank(QMainWindow):
    def __init__(self):
        super(Bank, self).__init__()
        self.db_cursor = db_cursor()
        self.login_label = None
        self.login_edit = None
        self.password_label = None
        self.password_edit = None
        self.sign_in = None
        self.sign_up = None
        self.init_ui()

    def init_ui(self):
        QToolTip.setFont(QFont('SansSerif', 9))

        # --- login ---
        self.login_label = QLabel('Login', self)
        self.login_label.move(30, 25)
        self.login_edit = QLineEdit(self)
        self.login_edit.setToolTip('Minimum length - 6 char. Case sensitive')
        self.login_edit.move(100, 25)

        # --- password ---
        self.password_label = QLabel('Password', self)
        self.password_label.move(30, 70)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setToolTip('Minimum length - 8 char. Case sensitive')
        self.password_edit.move(100, 70)

        # --- sign_in ---
        self.sign_in = QPushButton('Sign in', self)
        self.sign_in.setToolTip('Sign in with your existing account')
        self.sign_in.resize(self.sign_in.sizeHint())
        self.sign_in.move(100, 110)
        self.sign_in.clicked.connect(self.sign_in_with_check)

        # --- sign_up ---
        self.sign_up = QPushButton('Sign up', self)
        self.sign_up.setToolTip('Create new user')
        self.sign_up.resize(self.sign_up.sizeHint())
        self.sign_up.move(300, 48)
        # self.sign_up.clicked.connect(self.button_clicked)

        self.statusBar()
        self.center()
        self.setFixedSize(500, 338)
        self.setWindowTitle('P-Bank')
        self.setWindowIcon(QIcon('bank.png'))
        self.show()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Confirm Exit',
                                     "Are you sure you want to exit P-Bank?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def button_clicked(self, msg: str):

        sender = self.sender()
        self.statusBar().showMessage('{}: {}'.format(sender.text(), msg), 1500)

    def sign_in_with_check(self):
        expected_password = None

        if len(self.login_edit.text()) > 5 and len(self.password_edit.text()) > 7:
            self.db_cursor.execute("select bank.get_password_by_login('{}');".format(self.login_edit.text()))
            res = self.db_cursor.fetchall()[0][0]
            if len(res) > 1:
                expected_password = res
            elif res == '1':
                self.button_clicked('incorrect login')
            elif res == '2':
                self.button_clicked('something get wrong')
            else:
                raise Exception('Unexpected response from DB')
        else:
            self.button_clicked('incorrect length of login or password')

        if expected_password is not None:
            if self.password_edit.text() == expected_password:
                self.button_clicked('success')
            else:
                self.button_clicked('incorrect password')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    bank = Bank()
    sys.exit(app.exec())
