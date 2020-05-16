import os
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
	response = requests.post(url, json={'query': query, 'variables': variables})
	response = response.json()
	print(response)
	kayttaja_id = -1
	if response.get("data"):
		kayttaja_id = response["data"]["User"]["id"]
	return(kayttaja_id)


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
	response = requests.post(url, json={'query': query, 'variables': variables})
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
				if sarjan_tyyppi in ["SPECIAL", "MUSIC"]:
					sarjan_tyyppi = ["SP"]

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

	response = requests.post(url, json={'query': query, 'variables': variables})
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


def lue_sarjat_tietokannasta(ID):
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
				lokaalilista = lue_sarjat_tietokannasta(kayttaja_id)

				# Sarjat oliomuodossa ja molemmat luettu anilistista, joten voidaan verrata vaikka mal-id:n perusteella
				# (nämä harvemmin muuttuvat sarjoissa jotka on jo tullu loppuun)
				for sarja in sarjalista:
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


def vertaa_katsoneita(uudetkatsotut, lokaalisarjat):
	'''
	Ottaa paivita_anilist_tietokannat() palauttaman listan uusista katsotuista sarjoista,
	ja täydentää sen perusteella lokaalin kirjaston sarjojen tietoja,
	ts. jos käyttäjä on AniListin viimeisimpien tietojen mukaan katsonut sarjan, jota tämä
	ei paikallisten tietoejen mukaan ollut vielä katsonut, muutetaan paikalliset tiedot
	muotoon jossa kyseinen tyyppi on sarjan nähnyt
	'''

	muuttunut = False # paluuarvo kertoo kutsujaikkunalle, pitääkö tietokantatiedostot päivittää
	for katsoja in uudetkatsotut:
		for anilistsarja in uudetkatsotut[katsoja]:
			for lokaalisarja in lokaalisarjat:
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
