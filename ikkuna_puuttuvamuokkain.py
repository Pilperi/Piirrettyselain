import os
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Puuttuvatsarjat(object):
	def setupUi(self, Puuttuvatsarjat, Paaikkuna):
		Puuttuvatsarjat.setObjectName("Puuttuvatsarjat")
		self.MARGINAALIT = [10,10]
		self.MITAT       = [850,220]
		Puuttuvatsarjat.resize(self.MITAT[0], self.MITAT[1])
		Puuttuvatsarjat.setMinimumSize(self.MITAT[0], self.MITAT[1])
		Puuttuvatsarjat.setMaximumSize(self.MITAT[0], self.MITAT[1])

		# font = QtGui.QFont()
		# font.setPointSize(12)

		self.sarjalista = QtWidgets.QListWidget(Puuttuvatsarjat)
		self.sarjalista.setGeometry(QtCore.QRect(self.MARGINAALIT[0], self.MARGINAALIT[1], 210, 200))
		self.sarjalista.setObjectName("sarjalista")
		self.sarjalista.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
		self.sarjalista.selectionModel().selectionChanged.connect(self.nayta_tiedot)

		self.Paaikkuna  = Paaikkuna
		self.sarjat     = Paaikkuna.SARJAT                  # lista kaikista sarjoista
		self.indeksit   = Paaikkuna.muuttuneetindeksit      # puuttuvien indeksit
		self.ehdotukset = Paaikkuna.ehdotukset              # kansioehdotukset

		self.label_vanhapolku = QtWidgets.QLabel(Puuttuvatsarjat)
		self.label_vanhapolku.setGeometry(QtCore.QRect(self.MARGINAALIT[0]*2+210, 5, 600, 30))
		self.label_vanhapolku.setObjectName("label_vanhapolku")

		self.teksti_vanhapolku = QtWidgets.QLineEdit(Puuttuvatsarjat)
		self.teksti_vanhapolku.setGeometry(QtCore.QRect(self.MARGINAALIT[0]*2+210, 30, 600, 30))
		# self.teksti_vanhapolku.setFont(font)
		self.teksti_vanhapolku.setText("")
		self.teksti_vanhapolku.setReadOnly(True)
		self.teksti_vanhapolku.setObjectName("teksti_vanhapolku")

		self.label_uusipolku = QtWidgets.QLabel(Puuttuvatsarjat)
		self.label_uusipolku.setGeometry(QtCore.QRect(self.MARGINAALIT[0]*2+210, 60, 600, 30))
		self.label_uusipolku.setObjectName("label_uusipolku")

		self.teksti_uusipolku = QtWidgets.QLineEdit(Puuttuvatsarjat)
		self.teksti_uusipolku.setGeometry(QtCore.QRect(self.MARGINAALIT[0]*2+210, 85, 600, 30))
		# self.teksti_uusipolku.setFont(font)
		self.teksti_uusipolku.setText("")
		self.teksti_uusipolku.setObjectName("teksti_uusipolku")
		self.teksti_uusipolku.textChanged.connect(self.tarkistakansio)
		completer = QtWidgets.QCompleter()
		completer.setModel(QtWidgets.QDirModel(completer))
		self.teksti_uusipolku.setCompleter(completer)

		self.Aseta = QtWidgets.QPushButton(Puuttuvatsarjat)
		# self.Aseta.setGeometry(QtCore.QRect(230, 170, 50, 40))
		self.Aseta.setGeometry(QtCore.QRect(230, 125, 600, 40))
		self.Aseta.setObjectName("Aseta")
		self.Aseta.clicked.connect(self.aseta_uusikansio)
		self.Aseta.setStyleSheet("background-color: #4682B4; color: white")
		self.Aseta.setShortcut("Return")

		self.Poista = QtWidgets.QPushButton(Puuttuvatsarjat)
		self.Poista.setGeometry(QtCore.QRect(230, 170, 50, 40))
		# self.Poista.setGeometry(QtCore.QRect(290, 170, 50, 40))
		self.Poista.setObjectName("Poista")
		self.Poista.clicked.connect(self.poistasarja)

		self.Kansio = QtWidgets.QPushButton(Puuttuvatsarjat)
		# self.Kansio.setGeometry(QtCore.QRect(350, 170, 50, 40))
		self.Kansio.setGeometry(QtCore.QRect(290, 170, 50, 40))
		self.Kansio.setObjectName("Kansio")
		self.Kansio.clicked.connect(self.avaa_ehdotuskansio)

		self.buttonBox = QtWidgets.QDialogButtonBox(Puuttuvatsarjat)
		self.buttonBox.setGeometry(QtCore.QRect(370, 170, self.MITAT[0]-370-20, 40))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		# self.buttonBox.setLayoutDirection(1)
		self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
		# self.buttonBox.setCenterButtons(True)
		self.buttonBox.setObjectName("buttonBox")

		self.retranslateUi(Puuttuvatsarjat)
		self.buttonBox.accepted.connect(Puuttuvatsarjat.accept)
		self.buttonBox.rejected.connect(Puuttuvatsarjat.reject)
		QtCore.QMetaObject.connectSlotsByName(Puuttuvatsarjat)

	def retranslateUi(self, Puuttuvatsarjat):
		_translate = QtCore.QCoreApplication.translate
		Puuttuvatsarjat.setWindowTitle(_translate("Puuttuvatsarjat", "Puuttuvia sarjoja"))
		self.label_vanhapolku.setText(_translate("Puuttuvatsarjat", "Vanha polku"))
		self.label_uusipolku.setText(_translate("Puuttuvatsarjat", "Uusi polku"))
		self.Aseta.setText(_translate("Puuttuvatsarjat", "Aseta"))
		self.Poista.setText(_translate("Puuttuvatsarjat", "Poista"))
		self.Kansio.setText(_translate("Puuttuvatsarjat", "Kansio"))

	def sarjannimet(self):
		'''
		Lisää sarjojen nimet listaan, mikäli sarjalle
		ei ole vielä asetettu uutta kansiota
		'''
		nimet = []
		self.sarjalista.clear()
		for indeksi in self.indeksit:
			nimet.append(self.sarjat[indeksi].nimi)
		self.sarjalista.addItems(nimet)
		self.sarjalista.show()

	def nayta_tiedot(self):
		'''
		Asettaa valitun sarjan tiedot (vanhan kansion ja ehdotuksen) näkyville
		'''
		if self.indeksit:
			valittu = self.sarjalista.currentRow()
			if valittu != -1:
				sarja = self.sarjat[self.indeksit[valittu]]
				self.teksti_vanhapolku.setText(sarja.tiedostosijainti)
				self.teksti_uusipolku.setText(self.ehdotukset[valittu])
			else:
				self.teksti_vanhapolku.setText("")
				self.teksti_uusipolku.setText("")
		else:
			self.teksti_vanhapolku.setText("")
			self.teksti_uusipolku.setText("")

	def tarkistakansio(self):
		'''
		Tarkistaa, onko ehdotettu uusi kansio olemassa vai ei
		'''
		if self.teksti_uusipolku.text():
			if os.path.exists(self.teksti_uusipolku.text()):
				self.teksti_uusipolku.setStyleSheet("background-color: #228B22; color: white") # vihreä ruutu
			else:
				self.teksti_uusipolku.setStyleSheet("background-color: #B22222; color: white") # punainen ruutu
		else:
			self.teksti_uusipolku.setStyleSheet("background-color: grey") # normiruutu

	def aseta_uusikansio(self):
		'''
		Asettaa uuden kansion sarjan tietoihin
		'''
		valittu = self.sarjalista.currentRow()
		if valittu != -1 and self.teksti_uusipolku.text():
			sarja = self.sarjat[self.indeksit[valittu]]
			uusisijainti = self.teksti_uusipolku.text()
			# Ei kautta- tai kenoviivaan päättyviä polkuja
			if uusisijainti[-1] in ["/", "\\"]:
				uusisijainti = uusisijainti[:-1]
			sarja.tiedostosijainti = uusisijainti
			# sarja.tiedostosijainti = self.ehdotukset[valittu]
			self.indeksit.pop(valittu)
			self.ehdotukset.pop(valittu)
			self.sarjannimet()
			if self.indeksit:
				self.sarjalista.setCurrentRow(0)

	def poistasarja(self):
		'''
		Poistetaan sarja tietokannasta, koska se on poistettu kovalevyltä
		'''
		valittu = self.sarjalista.currentRow()
		if self.indeksit and valittu != -1:
			self.Paaikkuna.poistetutsarjat.append(self.indeksit[valittu])
			self.indeksit.pop(valittu)
			self.ehdotukset.pop(valittu)
			self.sarjannimet()
			if self.indeksit:
				self.sarjalista.setCurrentRow(0)

	def avaa_ehdotuskansio(self):
		'''
		Avaa ehdotetun kansion jotta käyttäjä voi katsoa näyttääkö oikealta
		'''
		valittu = self.sarjalista.currentRow()
		if valittu != -1:
			uusisijainti = self.teksti_uusipolku.text()
			if os.path.exists(uusisijainti):
				subprocess.run(["dolphin", uusisijainti], stdin=None, stdout=None, stderr=None)


if __name__ == "__main__":
	# tuuraajaluokka jonne dumpata tavaraa
	class Dummy:
		def __init__(self):
			self.poistetutsarjat = []
			self.SARJAT = []
			self.muuttuneetindeksit = []
			self.ehdotukset = []

	app = QtWidgets.QApplication([])
	tuuraaja = Dummy()
	Dialog = QtWidgets.QDialog()
	print(Dialog)
	ui = Ui_Puuttuvatsarjat()
	ui.setupUi(Dialog, tuuraaja)
	ui.sarjannimet()
	paluuarvo = Dialog.exec()
	app.exec()