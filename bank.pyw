import sys
from postgres_cursor import db_cursor
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, QTimer


class Bank(QMainWindow):
    def __init__(self):
        super(Bank, self).__init__()
        self.db_cursor = db_cursor()
        self.time_on_screen: int = 1500
        self.login_label = None
        self.login_edit = None
        self.password_label = None
        self.password_edit = None
        self.sign_in = None
        self.sign_up = None
        self.sign_up_dialog = None
        self.autoFillBackground()
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
        self.sign_in.setStyleSheet("background-color: #ffffff")
        self.sign_in.setToolTip('Sign in with your existing account')
        self.sign_in.resize(self.sign_in.sizeHint())
        self.sign_in.move(100, 110)
        self.sign_in.clicked.connect(self.sign_in_with_check)

        # --- sign_up ---
        self.sign_up = QPushButton('Sign up', self)
        self.sign_up.setStyleSheet("background-color: #ffffff")
        self.sign_up.setToolTip('Create new user')
        self.sign_up.resize(self.sign_up.sizeHint())
        self.sign_up.move(300, 48)
        self.sign_up.clicked.connect(self.sign_up_with_check)

        self.sign_up_dialog = SignUp(self)
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
        self.statusBar().showMessage('{}: {}'.format(sender.text(), msg), self.time_on_screen)

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
                # TODO: Create window with buttons
            else:
                self.button_clicked('incorrect password')

    def sign_up_with_check(self):
        self.sign_up_dialog.show()


class SignUp(QDialog):
    def __init__(self, parent=None):
        super(SignUp, self).__init__(parent)
        self.login_label = None
        self.login_edit = None
        self.password_label1 = None
        self.password_edit1 = None
        self.password_label2 = None
        self.password_edit2 = None
        self.confirm = None
        self.init_ui()

    def init_ui(self):
        # --- login ---
        self.login_label = QLabel('Login', self)
        self.login_label.move(30, 25)
        self.login_edit = QLineEdit(self)
        self.login_edit.setToolTip('Minimum length - 6 char. Case sensitive')
        self.login_edit.move(100, 25)

        # --- password1 ---
        self.password_label1 = QLabel('Password', self)
        self.password_label1.move(30, 70)
        self.password_edit1 = QLineEdit(self)
        self.password_edit1.setEchoMode(QLineEdit.Password)
        self.password_edit1.setToolTip('Minimum length - 8 char. Case sensitive')
        self.password_edit1.move(100, 70)

        # --- password2 ---
        self.password_label2 = QLabel('Re Enter\nPassword', self)
        self.password_label2.move(30, 115)
        self.password_edit2 = QLineEdit(self)
        self.password_edit2.setEchoMode(QLineEdit.Password)
        self.password_edit2.setToolTip('Minimum length - 8 char. Case sensitive')
        self.password_edit2.move(100, 115)

        # --- confirm ---
        self.confirm = QPushButton('Confirm', self)
        self.confirm.setStyleSheet("background-color: #ffffff")
        self.confirm.setToolTip('Confirm creating new account')
        self.confirm.resize(self.confirm.sizeHint())
        self.confirm.move(100, 160)
        self.confirm.clicked.connect(self.confirm_with_check)

        self.setFixedSize(250, 200)
        self.center()
        self.setWindowTitle('P-Bank')
        self.setWindowIcon(QIcon('bank.png'))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def fade(self, state):
        if state == 1:
            self.confirm.setStyleSheet("background-color: red")
        elif state == 0:
            self.confirm.setStyleSheet("background-color: green")
        QTimer.singleShot(300, self.unfade)

    def unfade(self):
        self.confirm.setStyleSheet("background-color: #ffffff")

    def confirm_with_check(self):
        if len(self.login_edit.text()) > 5 and self.password_edit1.text() == self.password_edit2.text() and len(
                self.password_edit1.text()) > 7:
            curs = db_cursor()
            curs.execute(
                "select bank.sign_up_new_user('{}','{}');".format(self.login_edit.text(), self.password_edit1.text()))
            res = curs.fetchall()[0][0]
            if res == '1':
                self.fade(1)
                # User with same login already exists
            elif res == '0':
                self.fade(0)
                self.hide()
        elif len(self.login_edit.text()) < 6 or len(self.password_edit1.text()) < 8 or len(
                self.password_edit2.text()) < 8:
            # Incorrect length of login or password
            self.fade(1)
        elif self.password_edit1.text() != self.password_edit2.text():
            # Incorrect password
            self.fade(1)
        else:
            # Confirm creating new account
            self.fade(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    bank = Bank()
    sys.exit(app.exec())
