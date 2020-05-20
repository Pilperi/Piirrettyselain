import os
import time
import json
import requests
import class_piirretyt as cp
import vakiot_kansiovakiot as kvak

# AniList API-osoite
url = 'https://graphql.anilist.co'

# Haetut käyttäjä-ID:t (Anilist)
ID_PILPERI		= 100202
ID_HAIDER		= 673
ID_LIHAKUNKARI	= 136448
ID_NAILO		= 1087
ID_TURSAKE		= 54882
KATSOJAT_ID		= [ID_PILPERI, ID_HAIDER, ID_LIHAKUNKARI, ID_NAILO, ID_TURSAKE]
KATSOJAT_NIMI	= {
					ID_PILPERI: "Pilperi",
					ID_HAIDER: "Haider",
					ID_LIHAKUNKARI: "Lihakunkari",
					ID_NAILO: "Nailo",
					ID_TURSAKE: "Tursake"
					}


def kayttajan_id(kayttajanimi):
	'''
	Hakee käyttäjän ID:n nimimerkin perusteella
	(kirjataan ylös kerran, niin ei tarvitse aina haeskella)
	'''
	query = '''
	query ($name: String) {
	  User (name: $name) {
		id
	  }
	}
	'''
	variables = {
		'name': kayttajanimi
	}

	# Tökitään anilistin API:a
	response = requests.post(url, json={'query': query, 'variables': variables}, timeout=5)
	response = response.json()
	print(response)
	kayttaja_id = -1
	if response.get("data"):
		kayttaja_id = response["data"]["User"]["id"]
	return(kayttaja_id)


def etsi_sarjaa(kansionimi, jaksoja=None, kielletyt=[]):
	'''
	Etsii sarjaa kansionnimen ja löydetyn jaksomäärän perusteella,
	(sarjannimi, MAL-ID, tyyppi, jaksomäärä)-tuplen kerrallaan, kriteerinä että sarjan MAL-ID
	ei ole annettujen listassa
	(ts. jos haluaa 10 hakutulosta, pitää funktiota kutsua kymmenen kertaa
	niin että edellisen kutsun paluu-ID lisätään kiellettyjen listaan)
	'''
	lista_sarjoista = []
	# Etsitään niin että jaksojen määrä on rajattu
	if jaksoja is not None:
		query = '''
		query ($nimi: String, $jaksoja: Int, $kielletyt: [Int]) {
		  Media (type: ANIME, search: $nimi, episodes_lesser: $jaksoja, idMal_not_in: $kielletyt) {
			title {romaji}		# Sarjan nimi roomautettuna
			idMal				# MAL-ID (kiitos Ailist)
			format				# TV, TV_SHORT, MOVIE, SPECIAL, OVA, ONA, MUSIC
			episodes			# Jaksomäärä
		  }
		}
		'''
		variables = {
			'nimi':			kansionimi,	# siivotussa muodossa, ts. ei [RAW] [OVA] ymv
			'jaksoja':		jaksoja-1,	# korkeintaan
			'kielletyt':	kielletyt   # kielletyt ID:t
		}
	# Ei rajoiteta jaksomäärän perusteella
	else:
		query = '''
		query ($nimi: String, $kielletyt: [Int]) {
		  Media (type: ANIME, search: $nimi, idMal_not_in: $kielletyt) {
			title {romaji}		# Sarjan nimi roomautettuna
			idMal				# MAL-ID (kiitos Ailist)
			format				# TV, TV_SHORT, MOVIE, SPECIAL, OVA, ONA, MUSIC
			episodes			# Jaksomäärä
		  }
		}
		'''
		variables = {
			'nimi':			kansionimi,	# siivotussa muodossa, ts. ei [RAW] [OVA] ymv
			'kielletyt':	kielletyt   # kielletyt ID:t
		}

	# Make the HTTP Api request
	try:
		response = requests.post(url, json={'query': query, 'variables': variables}, timeout=5)
	except ConnectionError:
		# Joskus yhteys ei pelaa
		time.sleep(10)
		response = requests.post(url, json={'query': query, 'variables': variables}, timeout=5)
	response = response.json()
	# print(response)

	nimi 			= ""
	malid			= 0
	sarjan_tyyppi 	= []
	jaksot  		= 0

	if response.get("data") and not response.get("errors"):
		nimi   = response["data"]["Media"]["title"]["romaji"]
		malid  = response["data"]["Media"]["idMal"]
		jaksot = response["data"]["Media"]["episodes"]
		sarjan_tyyppi = response["data"]["Media"]["format"]
		if sarjan_tyyppi in ["TV", "TV_SHORT", "ONA"]:
			sarjan_tyyppi = ["TV"]
		elif sarjan_tyyppi in ["SPECIAL", "MUSIC"]:
			sarjan_tyyppi = ["SP"]
		elif sarjan_tyyppi == "MOVIE":
			sarjan_tyyppi = ["MOV"]
		else:
			sarjan_tyyppi = ["OVA"]
	return((nimi, malid, sarjan_tyyppi, jaksot))


def etsi_sarjoja(kansionimi, jaksoja=None, lukumaara=10, isanta=None):
	'''
	Etsii lukumaara verran kansionimeä ja jaksomäärää
	vastaavia sarjoja, kutsumalla etsi_sarjaa() toistuvasti.
	Jos 'ikkuna', näytä popup-ikkuna
	'''
	tulossarjat = []
	kielletyt = []
	for i in range(lukumaara):
		if isanta:
			isanta.setWindowTitle("Etsitään Anilistista ehdokkaita... {}/{}".format(i, lukumaara))
		hakutulos = etsi_sarjaa(kansionimi, jaksoja, kielletyt)
		# Validin hakutuloksen voi tunnistaa vaikka sarjan nimestä,
		# joka on ei-tyhjä stringi jos jotain löytyi
		if hakutulos[0]:
			tulossarjat.append(hakutulos)
			print(hakutulos)
			kielletyt.append(hakutulos[1])
			time.sleep(0.05) # ei kiusata ihan liikaa, 50 ms+ hakujen välissä
		else:
			break
	return(tulossarjat)

def hae_malidilla(ID):
	'''
	Hakee sarjan tiedot tämän MAL-ID:llä,
	paluuarvo etsi_sarjaa()-yhteensopivassa muodossa
	(sarjannimi, MAL-ID, tyyppi, jaksomäärä)
	'''
	nimi 			= ""
	malid			= 0
	sarjan_tyyppi 	= []
	jaksot  		= 0

	if type(ID) == int and ID > 0:
		query = '''
		query ($id: Int) {
		  Media (idMal: $id) {
			title {romaji}		# Sarjan nimi roomautettuna
			idMal				# MAL-ID (kiitos Ailist)
			format				# TV, TV_SHORT, MOVIE, SPECIAL, OVA, ONA, MUSIC
			episodes			# Jaksomäärä
		  }
		}
		'''
		variables = {
			'id': ID
		}

		# Make the HTTP Api request
		response = requests.post(url, json={'query': query, 'variables': variables}, timeout=5)
		response = response.json()
		# print(response)

		if response.get("data") and not response.get("errors"):
			nimi   = response["data"]["Media"]["title"]["romaji"]
			malid  = response["data"]["Media"]["idMal"]
			jaksot = response["data"]["Media"]["episodes"]
			sarjan_tyyppi = response["data"]["Media"]["format"]
			if sarjan_tyyppi in ["TV", "TV_SHORT", "ONA"]:
				sarjan_tyyppi = ["TV"]
			elif sarjan_tyyppi in ["SPECIAL", "MUSIC"]:
				sarjan_tyyppi = ["SP"]
			elif sarjan_tyyppi == "MOVIE":
				sarjan_tyyppi = ["MOV"]
			else:
				sarjan_tyyppi = ["OVA"]
	return((nimi, malid, sarjan_tyyppi, jaksot))


def kayttajan_completedit(ID):
	'''
	Hakee käyttäjän completedien lukumäärän ID:n perusteella
	(voidaan katsoa onko tullut lisää completedeja)
	'''
	
	lista_sarjoista = [] # jos asiat on hassusti niin haeteaan lista sarjoista ja lasketaan siitä
	query = '''
	query ($id: Int) {
	  User (id: $id) {
		name
		statistics {
					anime {
							statuses(sort: [ID]) {count}		# [completed, paused, dropped, planning]
							}
							
		}
	  }
	}
	'''
	variables = {
		'id': ID
	}

	# Make the HTTP Api request
	response = requests.post(url, json={'query': query, 'variables': variables}, timeout=5)
	response = response.json()
	# print(response)
	katsottuja = -1
	katsoja = ""
	# print(KATSOJAT_NIMI[ID])
	print(response["data"]["User"]["name"])
	if response.get("data") and response["data"]["User"]["statistics"]["anime"]["statuses"]:
		katsottuja = response["data"]["User"]["statistics"]["anime"]["statuses"][0]["count"]

	# Joskus kun käyttäjä ollut tarpeeksi pitkään epäaktiivisena, AL nullaa tämän statistiikkasivun,
	# jolloin ei saa katsomismäärätilastoja mutta saa kyllä katsottujen sarjojen listan.
	# Lasketaan näissä tapauksissa katsottujen määrä sillä raskaalla tavalla, eli kiskomalla koko
	# sarjalista ja laskemalla sen pituus
	elif response.get("data"):
		lista_sarjoista = hae_sarjalista(ID)
		katsottuja = len(lista_sarjoista)
	return(katsottuja, lista_sarjoista)


def muunna_piirroslistaksi(response):
	'''
	Ottaa sisään anilistin palauttaman JSON-vastauksen,
	jossa (yleensä) yhden käyttäjän kaikki completedit,
	ja muuntaa tämän diktihässäkän listaksi Piirrossarja-olioita.
	'''
	paluuarvo = []
	# Kai data on ylipäätään jokseenkin oikeaa sorttia
	if "data" in response and 'MediaListCollection' in response["data"]:
		# Sarjat omina listoinaan teostyypin mukaan, rullataan näiden läpi
		for tyyppilista in response["data"]["MediaListCollection"]["lists"]:
			sarjalista = tyyppilista["entries"]
			for sarja in sarjalista:
				# print(sarja["media"])
				sarjan_nimi 	= sarja["media"]["title"]["romaji"]
				sarjan_id		= sarja["media"]["idMal"]
				sarjan_tyyppi	= sarja["media"]["format"]
				sarjan_jaksoja	= sarja["media"]["episodes"]

				# supistetaan sarjan tyyppi, ei olla niin tarkkoja
				if sarjan_tyyppi in ["TV", "TV_SHORT", "ONA"]:
					sarjan_tyyppi = ["TV"]
				elif sarjan_tyyppi in ["SPECIAL", "MUSIC"]:
					sarjan_tyyppi = ["SP"]
				elif sarjan_tyyppi == "MOVIE":
					sarjan_tyyppi = ["MOV"]
				else:
					sarjan_tyyppi = ["OVA"]

				# Kasataan Piirretty-olion pohjustamiseen sopivan mallinen dikti
				sarjadikti	=	{
								"nimi": 	sarjan_nimi,
								"tyyppi":	[sarjan_tyyppi],
								"jaksoja":	sarjan_jaksoja,
								"mal":		"https://myanimelist.net/anime/{}".format(sarjan_id)
								}
				
				# Jos sarjalla jotenkin ei ole MAL-id:tä, paluuarvo lienee
				# jotain hassua. Korvataan nimihaulla
				if type(sarjan_id) is not int or sarjan_id <= 0:
					sarjadikti["mal"] = "https://myanimelist.net/anime.php?q={}&type=0".format(sarjan_nimi.replace(" ", "+"))

				# Muodostetaan olio
				piirretty = cp.Piirretty(sarjadikti)
				paluuarvo.append(piirretty)
				# print(piirretty)
	return(paluuarvo)


def hae_sarjalista(ID, piirroslistana=True):
	'''
	Hakee käyttäjän sarjalistan tämän ID:n perusteella.
	Sarjoista niiden nimet, tyypit, jaksomäärät, MAL-id:t sekä tyypit.
	Yleensä halutaan nimenomaan Piirretty-olioiden muodossa,
	mutta jos jostain syystä ei niin voi laittaa piirroslistana=False
	'''
	query = '''
	query ($id: Int) {
	  MediaListCollection (userId: $id, status: COMPLETED, type: ANIME) {
	  lists {
	  		entries {
	  				media {
							title {romaji}		# Sarjan nimi roomautettuna
							idMal				# MAL-ID (kiitos Ailist)
							format				# TV, TV_SHORT, MOVIE, SPECIAL, OVA, ONA, MUSIC
							episodes			# Jaksomäärä
							}
					}
	  }
	}
	}
	'''
	variables = {
		'id': ID
	}

	response = requests.post(url, json={'query': query, 'variables': variables}, timeout=5)
	response = response.json()
	if piirroslistana:
		response = muunna_piirroslistaksi(response)
	return(response)


def kirjaa_tiedot_anilist(ID, sarjat):
	'''
	Kirjaa käyttäjän anilist-tiedot tietokantatiedostoon.
	Ensimmäiselle riville pelkkä sarjojen lukumäärä (nopeuttaa statuksen tarkistamista)
	ja sen jälkeen itse sarjalista
	'''
	if ID in kvak.ANILIST:
		lukumaara = len(sarjat)
		kohdetiedosto = kvak.ANILIST[ID]
		f = open(kohdetiedosto, "w+", encoding="utf8")
		# Kirjataan ekalle riville sarjojen lukumäärä. Täten ei tarvitse joka kerta repiä koko sarjalistaa RAM:iin
		f.write(f"{lukumaara}\n[")

		# Kirjataan sarjat
		lukumaara -= 1 # määrä ei muuttunut, mutta käytetään indeksointiin tässä muodossa
		for s,sarja in enumerate(sarjat):
			f.write("{}{}\n".format(str(sarja), ","*(s<lukumaara)))
		f.write("]")
		f.close()
	else:
		print(f"ID {ID} ei ole tunnettu käyttäjä-ID")


def lue_sarjat_tietokannasta(ID, piirrettyina=False):
	'''
	Lukee sarjalistan tietokantatiedostosta.
	'''
	paluuarvo = []
	if ID in kvak.ANILIST and os.path.exists(kvak.ANILIST[ID]):
		# Luetaan rivit alkaen toisesta rivistä, yhdistetään stringiksi
		f = open(kvak.ANILIST[ID], "r")
		rivilista = f.readlines()[1:]
		f.close()
		s = ""
		for rivi in rivilista:
			s += rivi

		# Lyödään stringi json-kääntäjään
		paluuarvo = json.loads(s)
		if piirrettyina:
			paluuarvo = [cp.Piirretty(arvo) for arvo in paluuarvo]
	return(paluuarvo)


def paivita_anilist_tietokannat():
	'''
	Päivittää käyttäjien AniList-tietokantatiedot, mikäli tarvetta ilmenee.
	Tarve ilmenee jos AL:n tietokannassa oleva katsottujen sarjojen määrä on suurempi
	kuin tietokantatiedostoon kirjattu.
	'''

	uudetkatsotut = {}
	for kayttaja_id in KATSOJAT_ID:
		uudetkatsotut[kayttaja_id] = []
		# Tietokantatiedosto on olemassa: luetaan tiedost sieltä ja verrataan verkkotietoihin
		if os.path.exists(kvak.ANILIST[kayttaja_id]):
			f = open(kvak.ANILIST[kayttaja_id], "r")
			tietokantasarjoja = int(f.readline())
			f.close()
			completedeja, sarjalista = kayttajan_completedit(kayttaja_id)

			# Jos luvut eivät täsmää, päivitetään
			if completedeja > tietokantasarjoja:
				print("Tietokannassa {} sarjaa ja verkossa {}, päivitetään tietokanta".format(tietokantasarjoja, completedeja))
				# Haetaan anilist-data
				if not sarjalista:
					sarjalista = hae_sarjalista(kayttaja_id)
				lokaalilista = lue_sarjat_tietokannasta(kayttaja_id, piirrettyina=True)

				# Sarjat oliomuodossa ja molemmat luettu anilistista, joten voidaan verrata vaikka mal-id:n perusteella
				# (nämä harvemmin muuttuvat sarjoissa jotka on jo tullu loppuun)
				for sarja in sarjalista:
					print(sarja)
					pari_on = False
					for lokaalisarja in lokaalilista:
						if sarja.mal == lokaalisarja.mal:
							pari_on = True
							break
					if not pari_on:
						print("{} ei ollut paikallisessa tietokannassa".format(sarja.nimi))
						uudetkatsotut[kayttaja_id].append(sarja)

				# Kirjataan tiedot tietokantaan
				kirjaa_tiedot_anilist(kayttaja_id, sarjalista)
			else:
				print("Luvut täsmäävät, molempien mukaan {} on katsonut {} sarjaa".format(KATSOJAT_NIMI[kayttaja_id], tietokantasarjoja))

		# Tietokantatiedostoa ei ole: luodaan
		else:
			print("Käyttäjän {} tietokantatiedostoa ei ole, luodaan".format(KATSOJAT_NIMI[kayttaja_id]))
			sarjalista = hae_sarjalista(kayttaja_id)
			uudetkatsotut[kayttaja_id] = sarjalista
			kirjaa_tiedot_anilist(kayttaja_id, sarjalista)
			print("Luotu, sarjoja {}".format(len(sarjalista)))
	return(uudetkatsotut)


def vertaa_katsoneita(uudetkatsotut=None, lokaalisarjat=[]):
	'''
	Ottaa paivita_anilist_tietokannat() palauttaman listan uusista katsotuista sarjoista,
	ja täydentää sen perusteella lokaalin kirjaston sarjojen tietoja,
	ts. jos käyttäjä on AniListin viimeisimpien tietojen mukaan katsonut sarjan, jota tämä
	ei paikallisten tietoejen mukaan ollut vielä katsonut, muutetaan paikalliset tiedot
	muotoon jossa kyseinen tyyppi on sarjan nähnyt
	'''

	# Tapauksessa None luetaan paikallisesta AL-tietokantatiedostosta
	if uudetkatsotut is None:
		uudetkatsotut = {}
		for kayttaja_id in KATSOJAT_ID:
			uudetkatsotut[kayttaja_id] = lue_sarjat_tietokannasta(kayttaja_id, piirrettyina=True)
	muuttunut = False # paluuarvo kertoo kutsujaikkunalle, pitääkö tietokantatiedostot päivittää
	for katsoja in uudetkatsotut:
		for anilistsarja in uudetkatsotut[katsoja]:
			print(anilistsarja)
			for lokaalisarja in lokaalisarjat:
				print(lokaalisarja)
				# Sarjat on samoja jos niillä on sama MAL-id.
				# Jos katsoja ei ole katsoneiden listalla, lisätään se sinne.
				if anilistsarja.mal == lokaalisarja.mal and KATSOJAT_NIMI[katsoja] not in lokaalisarja.katsoneet:
					lokaalisarja.katsoneet.append(KATSOJAT_NIMI[katsoja])
					print("Lisätty {} sarjan {} katsoneiden listalle".format(KATSOJAT_NIMI[katsoja], lokaalisarja.nimi))
					muuttunut = True
	return(muuttunut)


def printtaa_kayttajien_sarjat():
	'''
	Lähinnä protoiluun, printtaa ruudulle käyttäjien tiedot
	'''
	for kayttaja_id in KATSOJAT_ID:
		katsoja = KATSOJAT_NIMI[kayttaja_id]
		completedeja, sarjalista = kayttajan_completedit(kayttaja_id)
		if completedeja != -1:
			print("\n{} on katsonut {} sarjaa".format(katsoja, completedeja))
		else:
			print("\nKäyttäjän {} kohdalla jokin meni hassusti".format(kayttaja_id))
		print("\n\n")
		
		# Jos käyttäjän profiilissa on asiat hassusti, sarjalista on haettu jo lukumäärää hakiessa
		if not sarjalista:
			sarjalista = hae_sarjalista(kayttaja_id)
		for sarja in sarjalista:
			print(sarja)


# tulokset = etsi_sarjoja("Koi koi seven", 52, 10)
# print("Löytyi {} sarjaa".format(len(tulokset)))