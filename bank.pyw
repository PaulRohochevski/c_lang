import sys
import datetime
import subprocess
from postgres_cursor import db_cursor
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer

exe_path: str = "C:/Users/paul_/source/repos/p-bank/Debug/p-bank.exe"


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
        self.user_login = None
        self.user_password = None
        self.user_window = None
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
                self.user_login = self.login_edit.text()
                self.user_password = expected_password
                self.button_clicked('success')
                self.user_window = UserWindow(self, self.user_login)
                self.user_window.show()
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


class UserWindow(QMainWindow):
    def __init__(self, parent, user_login):
        super(UserWindow, self).__init__(parent)
        self.user_login = user_login
        self.db_cursor = db_cursor()
        self.time_on_screen: int = 1500
        self.user_id = None
        self.combo = None
        self.combo_label = None
        self.create_new_account = None
        self.recall_bank_account = None
        self.money_label = None
        self.money_value = None
        self.deposit_label = None
        self.deposit_info = None
        self.credit_label = None
        self.credit_info = None
        self.put_money_into_a_bank = None
        self.take_a_credit = None
        self.transfer_money = None
        self.order_a_money = None
        self.get_id()
        self.autoFillBackground()
        self.init_ui()

    def get_id(self):
        self.db_cursor.execute(
            "SELECT user_id FROM bank.user_credentials WHERE user_login ='{}';".format(self.user_login))
        self.user_id = self.db_cursor.fetchall()[0][0]

    def init_ui(self):
        QToolTip.setFont(QFont('SansSerif', 9))

        self.center()
        self.statusBar()
        self.setFixedSize(500, 338)
        self.setWindowTitle('P-Bank: User: {}'.format(self.user_login))
        self.setWindowIcon(QIcon('bank.png'))

        # --- create new account ---
        self.create_new_account = QPushButton('Create new\naccount', self)
        self.create_new_account.setStyleSheet("background-color: #ffffff")
        self.create_new_account.resize(self.create_new_account.sizeHint())
        self.create_new_account.move(350, 48)
        self.create_new_account.clicked.connect(self.create_acc)

        # --- recall bank account ---
        self.recall_bank_account = QPushButton('Recall existing\nbank account', self)
        self.recall_bank_account.setStyleSheet("background-color: #ffffff")
        self.recall_bank_account.setToolTip(
            "To delete an account,\nyour money value must be zero,\nyou do not have any credits or deposits")
        self.recall_bank_account.resize(self.recall_bank_account.sizeHint())
        self.recall_bank_account.move(350, 98)
        self.recall_bank_account.clicked.connect(self.recall_acc)

        # --- combo box ---
        self.combo = QComboBox(self)
        self.db_cursor.execute(
            "select account_id from bank.user_account WHERE user_id = {} order by account_id;".format(self.user_id))
        self.combo.addItems([str(it[0]) for it in self.db_cursor.fetchall()])
        self.combo.move(230, 48)
        self.combo.activated[str].connect(self.show_active_combo)

        # --- combo label ---
        self.combo_label = QLabel('Choose appropriate account number:', self)
        self.combo_label.setFixedWidth(220)
        self.combo_label.move(10, 48)

        # --- money label ---
        self.money_label = QLabel('Money:', self)
        self.money_label.move(30, 98)

        # --- money value ---
        mn = self.get_money_value(int(self.combo.currentText()))
        self.money_value = QLabel(str(mn), self)
        self.money_value.move(80, 98)

        # --- deposit label ---
        self.deposit_label = QLabel('Deposit:', self)
        self.deposit_label.move(30, 128)

        # --- deposit info ---
        di = self.get_deposit_info(int(self.combo.currentText()))
        self.deposit_info = QLabel(str(di), self)
        self.deposit_info.setFixedWidth(200)
        self.deposit_info.move(30, 158)

        # --- credit label ---
        self.credit_label = QLabel('Credit:', self)
        self.credit_label.move(30, 228)

        # --- credit info ---
        self.credit_info = QLabel('info', self)
        self.credit_info.setFixedWidth(200)
        self.credit_info.setFixedHeight(60)
        self.credit_info.move(30, 258)
        cred = self.get_credit_info(int(self.combo.currentText()))
        if isinstance(cred, str):
            self.credit_info.setText(cred)
        else:
            exp_d = datetime.date.strftime(cred[0][2], '%Y-%m-%d')
            self.credit_info.setText(
                'Credit money: {}\nInterest rate: {}\nExpiration date: {}'.format(cred[0][0], cred[0][1], exp_d))

        # --- put money into a bank ---
        self.put_money_into_a_bank = QPushButton('Put money\ninto a bank', self)
        self.put_money_into_a_bank.setStyleSheet("background-color: #ffffff")
        self.put_money_into_a_bank.resize(self.put_money_into_a_bank.sizeHint())
        self.put_money_into_a_bank.move(350, 148)
        self.put_money_into_a_bank.clicked.connect(self.put_money)

        # --- take a credit ---
        self.take_a_credit = QPushButton('Take a credit', self)
        self.take_a_credit.setStyleSheet("background-color: #ffffff")
        self.take_a_credit.resize(self.take_a_credit.sizeHint())
        self.take_a_credit.move(350, 198)
        self.take_a_credit.clicked.connect(self.take_money)

        # --- transfer money ---
        self.transfer_money = QPushButton('Transfer money', self)
        self.transfer_money.setStyleSheet("background-color: #ffffff")
        self.transfer_money.resize(self.transfer_money.sizeHint())
        self.transfer_money.move(350, 234)
        self.transfer_money.clicked.connect(self.trans_money)

        # --- order a money ---
        self.order_a_money = QPushButton('Order money', self)
        self.order_a_money.setStyleSheet("background-color: #ffffff")
        self.order_a_money.resize(self.order_a_money.sizeHint())
        self.order_a_money.move(350, 270)
        self.order_a_money.clicked.connect(self.ord_money)

        self.show()

    def show_active_combo(self, text):
        # --- account id ---
        account_id = int(text)

        # --- money ---
        money = self.get_money_value(account_id)
        self.money_value.setText(str(money))

        # --- deposit ---
        dep = self.get_deposit_info(account_id)
        if isinstance(dep, str):
            self.deposit_info.setText(dep)
        else:
            pass

        # --- credit ---
        cred = self.get_credit_info(account_id)
        if isinstance(cred, str):
            self.credit_info.setText(cred)
        else:
            exp_d = datetime.date.strftime(cred[0][2], '%Y-%m-%d')
            self.credit_info.setText(
                'Credit money: {}\nInterest rate: {}\nExpiration date: {}'.format(cred[0][0], cred[0][1], exp_d))

    def put_money(self):
        account_id = int(self.combo.currentText())
        # Сделать проверку через си код
        if self.get_deposit_info(account_id) is None:
            # do the work
            self.db_cursor.execute()
        else:
            pass

    def take_money(self):
        account_id = int(self.combo.currentText())

        if isinstance(self.get_credit_info(account_id), str):
            cred_dial = CreditDialog(self, False, account_id, self.db_cursor)
            cred_dial.show()
        else:
            cred_dial = CreditDialog(self, True, account_id, self.db_cursor)
            cred_dial.show()

    def trans_money(self):
        account_id = int(self.combo.currentText())
        # Сделать проверку через си код
        pass

    def ord_money(self):
        account_id = int(self.combo.currentText())
        # Сделать проверку через си код
        pass

    def get_money_value(self, account_id: int) -> float:
        self.db_cursor.execute("select money from bank.user_account where account_id = {};".format(account_id))
        money = self.db_cursor.fetchall()[0][0]
        return money

    def get_credit_info(self, account_id: int):
        self.db_cursor.execute(
            "select money, interest_rate, expiration_date from bank.user_credit where account_id = {};".format(
                account_id))
        info = self.db_cursor.fetchall()
        if len(info) > 0:
            return info
        else:
            return "Bank credit didn't detected"

    def get_deposit_info(self, account_id: int):
        self.db_cursor.execute(
            "select money, interest_rate, expiration_date from bank.user_deposit where account_id = {};".format(
                account_id))
        info = self.db_cursor.fetchall()
        if len(info) > 0:
            return info
        else:
            return "Bank deposit didn't detected"

    def create_acc(self):
        self.db_cursor.execute("INSERT INTO bank.user_account VALUES (DEFAULT, {}, 0.0)".format(self.user_id))
        self.button_clicked('Created new account successfully')
        self.db_cursor.execute("select currval('bank.user_account_account_id_seq');")
        self.combo.addItems([str(self.db_cursor.fetchall()[0][0])])
        self.fade_cr(0)

    def recall_acc(self):
        account_id = int(self.combo.currentText())
        money = self.get_money_value(account_id)
        dep = self.get_deposit_info(account_id)
        cred = self.get_credit_info(account_id)
        if money == 0.0 and isinstance(dep, str) and isinstance(cred, str):
            self.db_cursor.execute("delete from bank.user_account * where account_id = {}".format(account_id))
            self.combo.clear()
            self.db_cursor.execute("select account_id from bank.user_account WHERE user_id = {};".format(self.user_id))
            self.combo.addItems([str(it[0]) for it in self.db_cursor.fetchall()])
            self.show_active_combo(self.combo.currentText())
            self.button_clicked('Deleted account #{} successfully'.format(account_id))
            self.fade(0)
        else:
            self.fade(1)

    def button_clicked(self, msg: str):
        sender = self.sender()
        self.statusBar().showMessage('{}: {}'.format(sender.text(), msg), self.time_on_screen)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def fade(self, state):
        if state == 1:
            self.recall_bank_account.setStyleSheet("background-color: red")
        elif state == 0:
            self.recall_bank_account.setStyleSheet("background-color: green")
        QTimer.singleShot(300, self.unfade)

    def unfade(self):
        self.recall_bank_account.setStyleSheet("background-color: #ffffff")

    def fade_cr(self, state):
        if state == 1:
            self.create_new_account.setStyleSheet("background-color: red")
        elif state == 0:
            self.create_new_account.setStyleSheet("background-color: green")
        QTimer.singleShot(300, self.unfade_cr)

    def unfade_cr(self):
        self.create_new_account.setStyleSheet("background-color: #ffffff")


class CreditDialog(QDialog):
    def __init__(self, parent, previous_credit, account_id, db_cursor):
        super(CreditDialog, self).__init__(parent)
        self.previous_credit = previous_credit
        self.account_id = account_id
        self.db_cursor = db_cursor
        self.credit_1_lable = None
        self.credit_1_button = None
        self.credit_1_edit = None
        self.credit_2_lable = None
        self.credit_2_button = None
        self.credit_2_edit = None
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(350, 200)
        self.center()
        self.setWindowTitle('P-Bank')
        self.setWindowIcon(QIcon('bank.png'))

        # --- credit 1 ---
        self.credit_1_lable = QLabel(
            'Credit: Pobeda\nDue date: 2 years\nInterest rate: 15.99%\nMax money: 25000\nMin money: 5000\nEnter apropriate value:',
            self)
        self.credit_1_lable.move(30, 25)
        self.credit_1_edit = QLineEdit(self)
        self.credit_1_edit.move(30, 130)
        self.credit_1_button = QPushButton('Take money', self)
        self.credit_1_button.setStyleSheet("background-color: #ffffff")
        self.credit_1_button.resize(self.credit_1_button.sizeHint())
        self.credit_1_button.clicked.connect(self.confirm_credit_1)
        self.credit_1_button.move(30, 160)

        # --- credit 2 ---
        self.credit_2_lable = QLabel(
            'Credit: Polet\nDue date: 5 years\nInterest rate: 12.99%\nMax money: 50000\nMin money: 20000\nEnter apropriate value:',
            self)
        self.credit_2_lable.move(200, 25)
        self.credit_2_edit = QLineEdit(self)
        self.credit_2_edit.move(200, 130)
        self.credit_2_button = QPushButton('Take money', self)
        self.credit_2_button.setStyleSheet("background-color: #ffffff")
        self.credit_2_button.resize(self.credit_2_button.sizeHint())
        self.credit_2_button.clicked.connect(self.confirm_credit_2)
        self.credit_2_button.move(200, 160)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def fade_1(self, state):
        if state == 1:
            self.credit_1_button.setStyleSheet("background-color: red")
        elif state == 0:
            self.credit_1_button.setStyleSheet("background-color: green")
        QTimer.singleShot(300, self.unfade_1)

    def unfade_1(self):
        self.credit_1_button.setStyleSheet("background-color: #ffffff")

    def fade_2(self, state):
        if state == 1:
            self.credit_2_button.setStyleSheet("background-color: red")
        elif state == 0:
            self.credit_2_button.setStyleSheet("background-color: green")
        QTimer.singleShot(300, self.unfade_2)

    def unfade_2(self):
        self.credit_2_button.setStyleSheet("background-color: #ffffff")

    def confirm_credit_1(self):
        credit_money = float(self.credit_1_edit.text())
        expiration_date = datetime.date.today()
        expiration_date = expiration_date.replace(year=expiration_date.year + 2)
        run_exe = subprocess.run(
            [exe_path, 'credit', '{}'.format(self.previous_credit), '5000.0', '25000.0', '{}'.format(credit_money)],
            stdout=subprocess.PIPE)
        if run_exe.stdout == b'0':
            self.db_cursor.execute(
                "INSERT INTO bank.user_credit VALUES (DEFAULT, {account_id}, {money}, 15.99, {exp_date});".format(
                    account_id=self.account_id, money=credit_money,
                    exp_date="'{}'".format(datetime.date.strftime(expiration_date, '%Y-%m-%d'))))
            self.db_cursor.execute(
                "update bank.user_account set money = money + {money} where account_id = {account_id};".format(
                    money=credit_money, account_id=self.account_id))
            self.fade_1(0)
            self.close()
        elif run_exe.stdout == b'1':
            self.fade_1(1)

    def confirm_credit_2(self):
        credit_money = float(self.credit_2_edit.text())
        expiration_date = datetime.date.today()
        expiration_date = expiration_date.replace(year=expiration_date.year + 5)
        run_exe = subprocess.run(
            [exe_path, 'credit', '{}'.format(self.previous_credit), '20000.0', '50000.0', '{}'.format(credit_money)],
            stdout=subprocess.PIPE)
        if run_exe.stdout == b'0':
            self.db_cursor.execute(
                "INSERT INTO bank.user_credit VALUES (DEFAULT, {account_id}, {money}, 12.99, {exp_date});".format(
                    account_id=self.account_id, money=credit_money,
                    exp_date="'{}'".format(datetime.date.strftime(expiration_date, '%Y-%m-%d'))))
            self.db_cursor.execute(
                "update bank.user_account set money = money + {money} where account_id = {account_id};".format(
                    money=credit_money, account_id=self.account_id))
            self.fade_2(0)
            self.close()
        elif run_exe.stdout == b'1':
            self.fade_2(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    bank = Bank()
    sys.exit(app.exec())
