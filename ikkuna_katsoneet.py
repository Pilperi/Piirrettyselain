from PyQt5 import QtCore, QtGui, QtWidgets
import vakiot_piirrettysijainnit as ps
import class_piirretyt as cp

class Ui_Dialog(object):
    def setupUi(self, Dialog, sarja):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 250, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        paivita = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        paivita.setText('Päivitä')
        peru = self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)
        peru.setText('Peru')

        self.katsoneet = [k for k in sarja.katsoneet]

        self.txt_eikatsonut = QtWidgets.QLabel(Dialog)
        self.txt_eikatsonut.setGeometry(QtCore.QRect(50, 0, 301, 241))
        font = QtGui.QFont()
        font.setPointSize(12)

        if True:
            self.txt_eikatsonut.setFont(font)
            self.txt_eikatsonut.setFrameShape(QtWidgets.QFrame.Box)
            self.txt_eikatsonut.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
            self.txt_eikatsonut.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            self.txt_eikatsonut.setObjectName("txt_eikatsonut")

            self.nappi_pilperi = QtWidgets.QPushButton(Dialog)
            self.nappi_pilperi.setGeometry(QtCore.QRect(50, 40, 100, 100))
            self.nappi_pilperi.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_pilperi.setCheckable(False)
            self.nappi_pilperi.setObjectName("nappi_pilperi")
            if "Pilperi" in self.katsoneet:
                self.nappi_pilperi.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_1))
            else:
                self.nappi_pilperi.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_0))
            self.nappi_pilperi.setIconSize(QtCore.QSize(100,100))
            self.nappi_pilperi.clicked.connect(lambda: self.klikkaakatsojaa("Pilperi"))

            self.nappi_haider = QtWidgets.QPushButton(Dialog)
            self.nappi_haider.setGeometry(QtCore.QRect(150, 40, 100, 100))
            self.nappi_haider.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_haider.setCheckable(False)
            self.nappi_haider.setObjectName("nappi_haider")
            if "Haider" in self.katsoneet:
                self.nappi_haider.setIcon(QtGui.QIcon(ps.KUVA_HAIDER_1))
            else:
                self.nappi_haider.setIcon(QtGui.QIcon(ps.KUVA_HAIDER_0))
            self.nappi_haider.setIconSize(QtCore.QSize(100,100))
            self.nappi_haider.clicked.connect(lambda: self.klikkaakatsojaa("Haider"))

            self.nappi_lihakunkari = QtWidgets.QPushButton(Dialog)
            self.nappi_lihakunkari.setGeometry(QtCore.QRect(250, 40, 100, 100))
            self.nappi_lihakunkari.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_lihakunkari.setCheckable(False)
            self.nappi_lihakunkari.setObjectName("nappi_lihakunkari")
            if "Lihakunkari" in self.katsoneet:
                self.nappi_lihakunkari.setIcon(QtGui.QIcon(ps.KUVA_LIHAKUNKARI_1))
            else:
                self.nappi_lihakunkari.setIcon(QtGui.QIcon(ps.KUVA_LIHAKUNKARI_0))
            self.nappi_lihakunkari.setIconSize(QtCore.QSize(100,100))
            self.nappi_lihakunkari.clicked.connect(lambda: self.klikkaakatsojaa("Lihakunkari"))

            self.nappi_nailo = QtWidgets.QPushButton(Dialog)
            self.nappi_nailo.setGeometry(QtCore.QRect(50, 140, 100, 100))
            self.nappi_nailo.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_nailo.setCheckable(False)
            self.nappi_nailo.setObjectName("nappi_nailo")
            if "Nailo" in self.katsoneet:
                self.nappi_nailo.setIcon(QtGui.QIcon(ps.KUVA_NAILO_1))
            else:
                self.nappi_nailo.setIcon(QtGui.QIcon(ps.KUVA_NAILO_0))
            self.nappi_nailo.setIconSize(QtCore.QSize(100,100))
            self.nappi_nailo.clicked.connect(lambda: self.klikkaakatsojaa("Nailo"))

            self.nappi_tursake = QtWidgets.QPushButton(Dialog)
            self.nappi_tursake.setGeometry(QtCore.QRect(150, 140, 100, 100))
            self.nappi_tursake.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_tursake.setCheckable(False)
            self.nappi_tursake.setObjectName("nappi_tursake")
            if "Tursake" in self.katsoneet:
                self.nappi_tursake.setIcon(QtGui.QIcon(ps.KUVA_TURSAKE_1))
            else:
                self.nappi_tursake.setIcon(QtGui.QIcon(ps.KUVA_TURSAKE_0))
            self.nappi_tursake.setIconSize(QtCore.QSize(100,100))
            self.nappi_tursake.clicked.connect(lambda: self.klikkaakatsojaa("Tursake"))

            self.nappi_null = QtWidgets.QPushButton(Dialog)
            self.nappi_null.setGeometry(QtCore.QRect(250, 140, 100, 100))
            self.nappi_null.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nappi_null.setCheckable(False)
            self.nappi_null.setObjectName("nappi_null")
            self.nappi_null.clicked.connect(lambda: self.klikkaakatsojaa("Null"))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Muokkaa katsoneita"))
        self.txt_eikatsonut.setText(_translate("Dialog", "Katsoneet"))

    def klikkaakatsojaa(self,katsoja):
        '''
        Vaihtaa jäbän kuvaketta ja muokkaa hakuparametrejä asiaankuuluvasti
        '''
        print(self.katsoneet)
        if katsoja == "Pilperi":
            # Poista kriteereistä ja aseta kuva harmaaksi
            if "Pilperi" in self.katsoneet:
                self.katsoneet.remove("Pilperi")
                self.nappi_pilperi.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_0))
            # Lisää kriteereihin
            else:
                self.katsoneet.append("Pilperi")
                self.nappi_pilperi.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_1))

        elif katsoja == "Haider":
            # Poista kriteereistä ja aseta kuva harmaaksi
            if "Haider" in self.katsoneet:
                self.katsoneet.remove("Haider")
                self.nappi_haider.setIcon(QtGui.QIcon(ps.KUVA_HAIDER_0))
            # Lisää kriteereihin
            else:
                self.katsoneet.append("Haider")
                self.nappi_haider.setIcon(QtGui.QIcon(ps.KUVA_HAIDER_1))

        elif katsoja == "Lihakunkari":
            # Poista kriteereistä ja aseta kuva harmaaksi
            if "Lihakunkari" in self.katsoneet:
                self.katsoneet.remove("Lihakunkari")
                self.nappi_lihakunkari.setIcon(QtGui.QIcon(ps.KUVA_LIHAKUNKARI_0))
            # Lisää kriteereihin
            else:
                self.katsoneet.append("Lihakunkari")
                self.nappi_lihakunkari.setIcon(QtGui.QIcon(ps.KUVA_LIHAKUNKARI_1))

        elif katsoja == "Nailo":
            # Poista kriteereistä ja aseta kuva harmaaksi
            if "Nailo" in self.katsoneet:
                self.katsoneet.remove("Nailo")
                self.nappi_nailo.setIcon(QtGui.QIcon(ps.KUVA_NAILO_0))
            # Lisää kriteereihin
            else:
                self.katsoneet.append("Nailo")
                self.nappi_nailo.setIcon(QtGui.QIcon(ps.KUVA_NAILO_1))

        elif katsoja == "Tursake":
            # Poista kriteereistä ja aseta kuva harmaaksi
            if "Tursake" in self.katsoneet:
                self.katsoneet.remove("Tursake")
                self.nappi_tursake.setIcon(QtGui.QIcon(ps.KUVA_TURSAKE_0))
            # Lisää kriteereihin
            else:
                self.katsoneet.append("Tursake")
                self.nappi_tursake.setIcon(QtGui.QIcon(ps.KUVA_TURSAKE_1))

        # Kaikki päälle/pois
        else:
            # Poista kriteereistä ja aseta kuva harmaaksi
            if self.katsoneet:
                self.katsoneet = []
                self.nappi_pilperi.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_0))
                self.nappi_haider.setIcon(QtGui.QIcon(ps.KUVA_HAIDER_0))
                self.nappi_lihakunkari.setIcon(QtGui.QIcon(ps.KUVA_LIHAKUNKARI_0))
                self.nappi_nailo.setIcon(QtGui.QIcon(ps.KUVA_NAILO_0))
                self.nappi_tursake.setIcon(QtGui.QIcon(ps.KUVA_TURSAKE_0))
            # Lisää kaikki hakukriteereihin (kattaa myös NULL-tapauksen ou jes)
            else:
                self.katsoneet = ["Pilperi", "Haider", "Lihakunkari", "Nailo", "Tursake"]
                self.nappi_pilperi.setIcon(QtGui.QIcon(ps.KUVA_PILPERI_1))
                self.nappi_haider.setIcon(QtGui.QIcon(ps.KUVA_HAIDER_1))
                self.nappi_lihakunkari.setIcon(QtGui.QIcon(ps.KUVA_LIHAKUNKARI_1))
                self.nappi_nailo.setIcon(QtGui.QIcon(ps.KUVA_NAILO_1))
                self.nappi_tursake.setIcon(QtGui.QIcon(ps.KUVA_TURSAKE_1))

if __name__ == "__main__":
    '''
    Testaamiseen
    '''
    app = QtWidgets.QApplication([])
    Dialog = QtWidgets.QDialog()
    sarja = cp.Piirretty()
    ui = Ui_Dialog()
    ui.setupUi(Dialog, sarja)
    paluuarvo = Dialog.exec()
    if paluuarvo:
        print("Muuttunut")
        sarja.katsoneet = ui.katsoneet
    else:
        print("Peruttu")
    print(paluuarvo)
    print(sarja)
