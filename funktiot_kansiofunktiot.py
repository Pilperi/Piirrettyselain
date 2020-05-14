import os
import shutil
import vakiot_kansiovakiot as kvak

MURAKUMO_MUSIIKKI	= kvak.MURAKUMO_MUSIIKKI
MURAKUMO_INTERNET	= kvak.MURAKUMO_INTERNET
TIEDOSTOMUODOT		= kvak.TIEDOSTOMUODOT
#------------Funktiot kansiorakenteiden läpikäymiseen--------------------------
def paate(tiedosto):
	'''
	Pilkkoo tiedoston filu.pääte osiin 'filu' ja 'pääte'
	'''
	paate = tiedosto.split(".")[-1]
	if len(paate) < len(tiedosto):
		alkuosa = tiedosto[:-1*len(paate)-1]
		return(alkuosa, paate)
	else:
		return(tiedosto, "")


def joinittuonko(*lista):
	'''
	Liittää argumenttistringit toisiinsa ja tarkistaa onko lopputulos olemassaoleva kansio.
	Aika tosi usein tarvitsee rakennetta os.path.exists(os.path.join(a,b,c)) eikä
	sitä jaksaisi jok'ikinen kerta naputella uusiksi...
	'''
	joinittu = ""
	for a in lista:
		joinittu = os.path.join(joinittu, a)
	return(os.path.exists(joinittu))

def kansion_sisalto(kansio):
	'''
	Käy kansion läpi ja palauttaa listat
	sen sisältämistä tiedostoista
	sekä alikansioista
	'''
	tiedostot = []
	kansiot = []
	if os.path.exists(kansio):
		asiat = os.listdir(kansio)
		tiedostot = [a for a in asiat if os.path.isfile(os.path.join(kansio,a))]
		kansiot = [a for a in asiat if os.path.isdir(os.path.join(kansio,a))]
	return(tiedostot,kansiot)

def hanki_kansion_tiedostolista(kansio):
	'''
	Palauttaa annetun kansion tiedostolistan,
	ts. listan kaikista tiedostoista kansiossa ja sen alikansioista
	täysinä tiedostopolkuina
	'''
	tiedostolista = []
	if os.path.exists(kansio):
		for tiedosto in os.listdir(kansio):
			# Oikeassa tiedostomuodossa oleva tiedosto:
			if os.path.isfile(os.path.join(kansio, tiedosto)) and tiedosto.split(".")[-1].lower() in TIEDOSTOMUODOT:
				# Käy läpi kielletyt sanat
				ban = False
				for sana in KIELLETYT:
					if sana in tiedosto.lower():
						ban = True
						break
				if not ban:
					tiedostolista.append(os.path.join(kansio, tiedosto))

			# Kansio:
			elif os.path.isdir(os.path.join(kansio, tiedosto)):
				tiedostolista += hanki_kansion_tiedostolista(os.path.join(kansio, tiedosto))
	return(tiedostolista)

def kay_kansio_lapi(source_path, dest_path, level):
	'''
	Käy läpi kansiot 'source_path' ja 'dest_path', ja katsoo mitkä
	source_pathista löytyvät tiedostot ja kansiot puuttuvat dest_pathista.
	Eli ei, tämä ei osaa katsoa, onko tiedostoja tai kansiota uudelleennimetty
	tai siirrelty kansion sisällä toisiin alikansioihin.
	Käy rekursiivisesti läpi myös yhteiset alikansiot.
	'''

	kopioituja = 0
	kopioarvo = 0
	if os.path.exists(source_path) and os.path.exists(dest_path):
		try:
			source_objects = os.listdir(source_path) # Noutokansion tiedostot ja alikansiot, nettikatkeamisvaralla
		except OSError:
			return(-1)
		dest_objects = os.listdir(dest_path) # Kohdekansion tiedostot ja alikansiot

		prlen = max(5, 69 - 15*level)
		i = 0
		j = prlen
		while j < len(str(os.path.basename(source_path))):
			#print("{:s}{:s}".format("\t"*level, str(os.path.basename(source_path))[i:j]))
			i = j
			j += prlen
		#print("{:s}{:s}".format("\t"*level, str(os.path.basename(source_path))[i:]))
		print("{:s}".format(str(os.path.basename(source_path))))
		#print("{:s}|\n{:s}|".format("\t"*(level+1), "\t"*(level+1)))

		# Käydään läpi noutokansion tiedostot ja alikansiot
		for object in source_objects:
			# Kansio joka on molemmissa: käy läpi ja katso löytyykö kaikki tiedostot (ja rekursiivisesti alikansiot
			if os.path.isdir(os.path.join(source_path, object)) and object in dest_objects:
				kopioarvo = kay_kansio_lapi(os.path.join(source_path, object), os.path.join(dest_path, object), level+1)
				if kopioarvo >= 0:
					kopioituja += kopioarvo
				elif not kopioituja:
					kopioituja = -1
					break

			# Kansio tai tiedosto joka ei ole kohdekansiossa: kopsaa kohdekansioon
			elif object not in dest_objects:
				# Puuttuva kansio
				if os.path.isdir(os.path.join(source_path, object)):
					print("\nKopioi kansio: {:s}\n".format(os.path.join(source_path, object)))
					shutil.copytree(os.path.join(source_path, object), os.path.join(dest_path, object))
					kopioituja += 1
				# Puuttuva tiedosto
				elif os.path.isfile(os.path.join(source_path, object)):
					print("\nKopioi tiedosto: {:s}\n".format(os.path.join(source_path, object)))
					shutil.copy2(os.path.join(source_path, object), os.path.join(dest_path, object))
					kopioituja += 1
	else:
		print("Huono polku:\n{:s}\n{:s}".format("[{:s}] Source: {:s}".format(str(os.path.exists(source_path)), source_path), "[{:s}] Dest: {:s}".format(str(os.path.exists(dest_path)), dest_path)))
	return(kopioituja)

def kopioi_etakoneelta(musakansio=MURAKUMO_MUSIIKKI, kuvakansio=MURAKUMO_INTERNET):
	# Kopioi Musiikki
	musiikkistatsit = [0, ""]
	kuvastatsit = [0, ""]
	if PETTAN_FOLDER in musakansio:
		etakoneen_nimi = "Pettankone"
		if "Nipa" in musakansio:
			musa_kohdekansio = NIPAMUSA_FOLDER
			kuva_kohdekansio = NIPAKUVA_FOLDER
		elif "Jouni" in musakansio:
			musa_kohdekansio = JOUNIMUSA_FOLDER
			kuva_kohdekansio = JOUNIKUVA_FOLDER
		else:
			musa_kohdekansio = MUUMUSA_FOLDER
			kuva_kohdekansio = MUUKUVA_FOLDER
	else:
		etakoneen_nimi = "Murakumo"
		musa_kohdekansio = MUSIIKKI_FOLDER
		kuva_kohdekansio = INTERNET_FOLDER
	try:
		if musakansio and os.listdir(musakansio) and os.path.exists(musa_kohdekansio):
			print(f"Kopioi Musiikki ({etakoneen_nimi})")
			musiikkistatsit[0] = kay_kansio_lapi(musakansio, musa_kohdekansio, 0)
			if musiikkistatsit[0] < 0:
				musiikkistatsit[1] = f" (Etäkone {etakoneen_nimi} poissa päältä)"
			print(f"Musiikki kopioitu etäkoneelta ({etakoneen_nimi}).\n")
		else:
			print(f"Etäkoneen {etakoneen_nimi} Musiikki-kansiota ei löytynyt. Liekö poissa päältä?\n")
			musiikkistatsit = [0, f" (Etäkone ({etakoneen_nimi}) poissa päältä)"]

		# Kopioi INTERNET-kansion sisältö
		if kuvakansio and os.listdir(kuvakansio) and os.path.exists(kuva_kohdekansio):
			print(f"Kopioi INTERNET etäkoneelta ({etakoneen_nimi})")
			kuvastatsit[0] = kay_kansio_lapi(kuvakansio, kuva_kohdekansio, 0)
			if kuvastatsit[0] < 0:
				kuvastatsit[1] = f" (Etäkone ({etakoneen_nimi}) poissa päältä)"
			print(f"INTERNET sisältö kopioitu etäkoneelta ({etakoneen_nimi}).\n")
		else:
			print(f"Etäkoneen {etakoneen_nimi} INTERNET-kansiota ei löytynyt. Liekö poissa päältä?\n")
			kuvastatsit = [0, f" (Etäkone ({etakoneen_nimi}) poissa päältä)"]
	except OSError:
		return([[0,f" (Etäkone {etakoneen_nimi} poissa päältä)"], [0,f" (Etäkone {etakoneen_nimi} poissa päältä)"]])
	return([musiikkistatsit, kuvastatsit])

def luo_tiedostolista(kansio):
	tiedostopolkulista = []
	for tiedosto in os.listdir(kansio):
		if os.path.isfile(os.path.join(kansio, tiedosto)):
			tiedostopolkulista.append(os.path.join(kansio,tiedosto))
		else:
			tiedostopolkulista += luo_tiedostolista(os.path.join(kansio, tiedosto))
	return(tiedostopolkulista)
