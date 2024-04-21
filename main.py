from USOSLite import Ui_MainWindow
from logowanie import Ui_Dialog
from dialog_prowadzacy import Ui_Dialog_prowadzacy
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt, QSize, QEvent
from PyQt5.QtCore import QObject, QProcess, QCoreApplication, QItemSelection, QTimer
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog, QListWidgetItem, QTableWidgetItem, QComboBox, \
    QStyleFactory, QWidget, QLabel, QToolButton
import time, random, string, sys, webbrowser


# do jednego exe pyinstaller --onefile --noconsole main.py

g_imie = ""
g_nazwisko = ""
g_email = ""
g_block_main_tab = False

class Prowadzacy_dialog(QtWidgets.QDialog, Ui_Dialog_prowadzacy):
    def __init__(self, data):
        super(Prowadzacy_dialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Informacja")
        self.label_imie.setText(data[0])
        self.label_opis.setText(data[1])

class Logowanie(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Logowanie, self).__init__()
        self.setupUi(self)
        self.parent = parent
        print("asd")



    @pyqtSlot()
    def on_pushButton_pressed(self):
        if self.lineEdit_2.text() == "" or "@student.uj.edu.pl" not in self.lineEdit_2.text() or "." not in self.lineEdit_2.text() or self.lineEdit_2.text()[0] == "@" or self.lineEdit_2.text()[0] == ".":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Nieprawidlowy adres email, powinien byc @student.uj.edu.pl")
            msg.setWindowTitle("Blad")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
            return
        if len(self.lineEdit.text()) < 3:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Nieprawidlowe haslo")
            msg.setWindowTitle("Blad")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
            return
        global g_imie
        global g_nazwisko
        global g_block_main_tab
        global g_email
        g_email = self.lineEdit_2.text()
        imie,nazwisko = self.lineEdit_2.text().split("@")[0].split(".")
        imie = ''.join([i for i in imie if not i.isdigit()]).upper()
        nazwisko = ''.join([i for i in nazwisko if not i.isdigit()]).upper()
        g_imie, g_nazwisko = imie, nazwisko
        g_block_main_tab = True
        self.parent.tabWidget.setCurrentIndex(1)
        self.close()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowTitle("USOS Lite")
        self.pushButton.mousePressEvent = self.on_pushButton_next_week_clicked
        self.pushButton_2.mousePressEvent = self.on_pushButton_prev_week_clicked

        self.tabWidget.setTabIcon(0, QtGui.QIcon(':icons/logo.png'))
        self.tabWidget.setIconSize(QSize(150, 100))

        self.tableWidget.cellClicked.connect(self.on_click_cell_event)
        self.nralbumu = random.randrange(1000000, 9999999)


        dialog = Logowanie(self)
        dialog.installEventFilter(self)
        dialog.exec()
        global g_imie
        global g_nazwisko
        if g_imie == "" and g_nazwisko == "":
            sys.exit()
        self.zmien_nazwe_ucznia()

    def zmien_nazwe_ucznia(self):
        self.label_imienaziwsko.setText(f"{g_imie} {g_nazwisko}")
        self.label_opis.setText(f"""<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">
        <html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">
        p, li {{ white-space: pre-wrap; }}
        hr {{ height: 1px; border-width: 0; }}
        </style></head><body style=" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;">
        <p align="center" style=" margin-top:1px; margin-bottom:1px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">NR ALBUMU: {self.nralbumu}</p>
        <p align="center" style=" margin-top:1px; margin-bottom:1px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">I stopień, Informatyka Stosowana</p>
        <p align="center" style=" margin-top:1px; margin-bottom:1px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">{g_email}</p></body></html>""")

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Close and g_imie == "" and g_nazwisko == "":
            self.close()
        return False

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, i):  # changed!
        global g_block_main_tab
        print( "Tab Index Changed!","Current Tab Index: %d" % i)
        if i == 6:  # wyloguj
            g_block_main_tab = False
            self.tabWidget.setCurrentIndex(0)
            global g_imie
            global g_nazwisko
            g_imie = ""
            g_nazwisko = ""
            dialog = Logowanie(self)
            dialog.installEventFilter(self)
            dialog.exec()
            self.nralbumu = random.randrange(1000000, 9999999)
            print("wylogowano")
        elif i == 1:  # glowna
            self.zmien_nazwe_ucznia()
        elif i == 0 and g_block_main_tab:
            self.tabWidget.setCurrentIndex(1)

    @pyqtSlot()
    def on_pushButton_poczta_clicked(self):
        webbrowser.open('http://outlook.com')

    @pyqtSlot()
    def on_pushButton_dziekanat_clicked(self):
        self.plainTextEdit_dziekanat1.setPlainText("")
        self.plainTextEdit_dziekanat2.setPlainText("")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Wyslano wiadomosc do dziekanatu")
        msg.setWindowTitle("Informacja")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

        ############################################plan zajec###############################################

    przedmioty_info = {"algebra": ("Robert Krawczyk", '1-02'), "Projektowanie": ("Karolina Kowal", '2-02'),
                       "Interfacy NieGraficzne": ("Kali Mell", '1-12'), "C++": ("Dziadek mroz ", '1-05'),
                       "Java": ("Santa Claus ", '1-13')}
    przedmioty = [*przedmioty_info.keys()]
    plany = [[[2, -1, -1, -1, -1], [-1, -1, -1, 3, -1], [-1, 4, -1, -1, -1], [-1, -1, -1, -1, -1], [0, -1, 1, -1, -1],[-1, -1, -1, -1, -1]],
             [[-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, 2, -1, -1, -1], [1, -1, -1, -1, -1], [3, 4, -1, -1, 0],[-1, -1, -1, -1, -1]],
             [[-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, 1, 2, -1, -1], [-1, 3, 4, 0, -1], [-1, -1, -1, -1, -1],[-1, -1, -1, -1, -1]],
             [[-1, -1, -1, -1, -1], [-1, -1, 1, -1, -1], [-1, -1, 0, 2, -1], [-1, -1, -1, -1, -1], [-1, -1, 3, -1, -1],[-1, -1, -1, 4, -1]]]
    wlasne = []

    def on_click_cell_event(self, row, column):
        index = self.plany[week_counter][row][column]
        if index>-1:
            przedmiot= self.przedmioty[index]
            print(self.przedmioty_info[przedmiot])
            dialog = Prowadzacy_dialog(self.przedmioty_info[przedmiot])
            dialog.exec()

    def on_pushButton_next_week_clicked(self, event):
        global week_counter
        if event.button() == Qt.LeftButton and week_counter != 3:
            week_counter += 1
            week = self.plany[week_counter]
            print(self.wlasne)
            for x in range(6):
                for y in range(5):
                    if self.tableWidget.item(x, y).text() not in self.przedmioty and self.plany[week_counter - 1][x][y] < 0:
                        if len(self.wlasne) == 0 or self.tableWidget.item(x, y).text() not in self.wlasne:
                            self.wlasne.append(self.tableWidget.item(x, y).text())
                            self.plany[week_counter - 1][x][y] = -1 - len(self.wlasne)
                        elif len(self.wlasne) != 0 and self.tableWidget.item(x, y).text() in self.wlasne:
                            self.plany[week_counter - 1][x][y] = -2 - self.wlasne.index(
                                self.tableWidget.item(x, y).text())
                    if week[x][y] > -1:
                        self.tableWidget.item(x, y).setText(self.przedmioty[week[x][y]])
                    else:
                        if week[x][y] < -1:
                            self.tableWidget.item(x, y).setText(self.wlasne[-2 - week[x][y]])
                        else:
                            self.tableWidget.item(x, y).setText(" ")
            self.update()

    def on_pushButton_prev_week_clicked(self, event):

        global week_counter
        if event.button() == Qt.LeftButton and week_counter > 0:
            week_counter -= 1
            week = self.plany[week_counter]
            for x in range(6):
                for y in range(5):
                    if str(self.tableWidget.item(x, y).text()) not in self.przedmioty and self.plany[week_counter + 1][x][y] < 0:
                        if len(self.wlasne) == 0 or self.tableWidget.item(x, y).text() not in self.wlasne:
                            self.wlasne.append(self.tableWidget.item(x, y).text())
                            self.plany[week_counter + 1][x][y] = -1 - len(self.wlasne)
                        elif len(self.wlasne) != 0 and self.tableWidget.item(x, y).text() in self.wlasne:
                            self.plany[week_counter + 1][x][y] = -2 - self.wlasne.index(
                                self.tableWidget.item(x, y).text())
                    if week[x][y] > -1:
                        self.tableWidget.item(x, y).setText(self.przedmioty[week[x][y]])
                    else:
                        if week[x][y] < -1:
                            self.tableWidget.item(x, y).setText(self.wlasne[-2 - week[x][y]])
                        else:
                            self.tableWidget.item(x, y).setText(" ")
            self.update()


if __name__ == "__main__":
    week_counter = 0

    # print silent QT errors
    sys._excepthook = sys.excepthook


    def exception_hook(exctype, value, traceback):
        # print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    sys.excepthook = exception_hook

    app = QtWidgets.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())