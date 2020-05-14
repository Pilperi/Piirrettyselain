'''
Piirrettyhaun luokat
'''
NULL = {}.get(0)

class Piirretty:
	def __init__(self, dikti={}):
		if not dikti.keys():
			self.nimi				= ""			# Teoksen nimi
			self.aliakset			= []			# Vaihtoehtoiset nimet
			self.tyyppi				= []			# TV/OVA/MOV
			self.jaksoja			= 0				# Jaksomäärä
			# self.vuosi				= 0				# Alkamisvuosi
			self.kuvake				= "oletus"	# MAL-kuvakkeen nimi
			self.tiedostosijainti	= ""			# Kansion sijainti kovalevyllä
			self.tagit				= []			# Sekalaisia tageja (listasarja, bakaBT etc)
			self.mal 				= ""			# MAL-URL
			self.katsoneet			= []			# Ketkä katsoneet
		else:
			self.nimi				= dikti.get("nimi")
			self.aliakset			= dikti.get("aliakset")
			self.tyyppi				= dikti.get("tyyppi")
			self.jaksoja			= dikti.get("jaksoja")
			self.kuvake				= dikti.get("kuvake")
			self.tiedostosijainti	= dikti.get("tiedostosijainti")
			self.tagit				= dikti.get("tagit")
			self.mal 				= dikti.get("mal")
			self.katsoneet			= dikti.get("katsoneet")

	def __str__(self):
		stringi = "\t{\n"
		stringi += "\t\t\"nimi\":\"{}\",\n".format(self.nimi)
		stringi += "\t\t\"aliakset\":["
		aliaksia = len(self.aliakset)-1
		for i,alias in enumerate(self.aliakset):
			stringi += "\"{}\"{:s}".format(alias.replace("\"", "\\\""), ","*(i<aliaksia))
		stringi += "],\n"
		stringi += "\t\t\"tyyppi\":["
		tyyppei = len(self.tyyppi)-1
		for i,tyyppi in enumerate(self.tyyppi):
			stringi += "\"{}\"{:s}".format(tyyppi, ","*(i<tyyppei))
		stringi += "],\n"
		stringi += "\t\t\"jaksoja\":{},\n".format(self.jaksoja)
		stringi += "\t\t\"kuvake\":\"{}\",\n".format(self.kuvake)
		stringi += "\t\t\"tiedostosijainti\":\"{}\",\n".format(self.tiedostosijainti)
		stringi += "\t\t\"tagit\":["
		tageja = len(self.tagit)-1
		for i,tagi in enumerate(self.tagit):
			stringi += "\"{}\"{:s}".format(tagi, ","*(i<tageja))
		stringi += "],\n"
		stringi += "\t\t\"mal\":\"{}\",\n".format(self.mal)
		stringi += "\t\t\"katsoneet\":["
		katsoneita = len(self.katsoneet)-1
		for i,katsoja in enumerate(self.katsoneet):
			stringi += "\"{}\"{:s}".format(katsoja, ","*(i<katsoneita))
		stringi += "]\n"
		stringi += "\t}"
		return(stringi)



class Hakuparametrit:
	'''
	Luokka hakuparametreille
	'''
	def __init__(self, parametrit={}):
		self.nimessa	= parametrit.get("nimessa")		# sarjan nimessä (tai aliaksessa) str
		self.jaksoja	= parametrit.get("jaksoja")		# sarjassa jaksoja (yli, ali)
		self.katsomatta	= parametrit.get("katsomatta")	# ketkä eivät ole katsoneet sarjaa [u1, u2, ...]
		self.tyyppi		= parametrit.get("tyyppi")		# teos jotain tyypeistä [t1, t2, ...]
		self.tageja		= parametrit.get("tageja")		# teos on/ei ole jollain tagilla, tupleina [(tagi, bool), (tagi, bool), ...]

	def __str__(self):
		paluuarvo = ""
		if self.nimessa:
			paluuarvo += "Nimessä oltava:\t{}\n".format(self.nimessa)

		if self.jaksoja and any([a > 0 for a in self.jaksoja]):
			paluuarvo += "Jaksoja oltava:\t"
			if self.jaksoja[0]:
				paluuarvo += "yli {}".format(self.jaksoja[0])
			if self.jaksoja[1]:
				paluuarvo += "{}alle {}".format((self.jaksoja[0] > 0)*" ja ", self.jaksoja[1])
			paluuarvo += "\n"

		if self.katsomatta:
			paluuarvo += "Sarjaa ei ole nähnyt:"
			for katsoja in self.katsomatta:
				paluuarvo += f"\n\t{katsoja}"
			paluuarvo += "\n"

		if self.tyyppi:
			paluuarvo += "Teos jotain tyypeistä:"
			tyyppeja = len(self.tyyppi)-1
			for t,tyyppi in enumerate(self.tyyppi):
				paluuarvo += "{}{}".format(tyyppi, ", "*(t<tyyppeja))
			paluuarvo += "\n"

		if self.tageja:
			tuleeolla = [a[0] for a in self.tageja if a[1]]
			eisaaolla = [a[0] for a in self.tageja if not(a[1])]
			if tuleeolla:
				paluuarvo =+ "Tageissa tulee olla: "
				tageja = len(tuleeolla)-1
				for t,tagi in tuleeolla:
					paluuarvo += "{}{}".format(tagi, ", "*(t<tageja))
			else:
				if len(tuleeolla):
					paluuarvo += "\n"
				paluuarvo =+ "Tageissa ei saa olla: "
				tageja = len(eisaaolla)-1
				for t,tagi in eisaaolla:
					paluuarvo += "{}{}".format(tagi, ", "*(t<tageja))
			paluuarvo += "\n"
		return(paluuarvo)

	def tarkasta(self, sarja):
		'''
		Tarkastaa, täyttääkö sarja annetut hakukriteerit
		'''

		# nimi ei täsmää
		if (self.nimessa is not NULL) and (self.nimessa.lower() not in sarja.nimi.lower()) and not any([self.nimessa.lower() in alias.lower() for alias in sarja.aliakset]):
				return(False)

		# jaksomäärä ei täsmää
		if (self.jaksoja is not NULL) and (sarja.jaksoja < self.jaksoja[0] or sarja.jaksoja > self.jaksoja[1]):
			return(False)

		# joku on nähnyt sarjan
		if (self.katsomatta is not NULL) and (any([(a in sarja.katsoneet) for a in self.katsomatta])):
			return(False)

		# sarja on väärää tyyppiä
		if (self.tyyppi is not NULL) and not(any([(a not in sarja.tyyppi) for a in self.tyyppi])):
			return(False)

		# sarjalla ei ole haluttuja tageja tai sillä on tageja joita sillä ei pitäisi olla
		if (self.tageja is not NULL) and (any([((a not in sarja.tagit) and a[1]) or ((a in sarja.tagit) and not(a[1])) for a in self.tageja])):
			return(False)

		# Jos ei mitään puutetta löydetty, sarja on ok
		return(True)

	def hae_kriteereilla(self, sarjalista):
		'''
		Palauttaa listan sarjoista, jotka täsmäävät annettuihin hakukriteereihin,
		sekä näiden paikat alkuperäisessä listassa
		'''

		hakutulokset	= []
		indeksit		= []
		for i,sarja in enumerate(sarjalista):
			if self.tarkasta(sarja):
				hakutulokset.append(sarja)
				indeksit.append(i)
		return(hakutulokset, indeksit)