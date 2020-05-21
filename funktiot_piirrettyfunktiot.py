import os
import sys
import json
import xml.etree.ElementTree as ET
import urllib.request
import funktiot_kansiofunktiot as kfun
import vakiot_kansiovakiot as kvak
from class_piirretyt import *

TUNNISTEET = ["[OVA]", "[MOV]", "[RAW]"]
PIIRRETTYDIKTI =	{
					kvak.KANSIO_AURINKOKALA:	[],
					kvak.KANSIO_REDRUM:			[],
					kvak.KANSIO_MICHIRU:		[],
					kvak.KANSIO_SUZUYA:			[],
					kvak.KANSIO_NUHMU:			[]
					}

MANUAALIDIKTI		= {}
if os.path.exists(kvak.MANUAALISARJAT):
	f = open(kvak.MANUAALISARJAT, "r")
	diktiversio = json.load(f)
	f.close()
	for kansio in diktiversio:
		MANUAALIDIKTI[kansio] = []
		for sarja in diktiversio[kansio]:
			MANUAALIDIKTI[kansio].append(Piirretty(sarja))


def jarjesta(sarjalista):
	# Laittaa sarjat järjestykseen
	zipattu = zip([sarja.nimi for sarja in sarjalista], sarjalista)
	jarkassa = [a for _,a in sorted(zipattu, key=lambda s: s[0])]
	return(jarkassa)

def tarkasta_puuttuvat(sarjalista):
	'''
	Tarkastaa kustakin piirretystä, onko määritelty kansiopolku vielä olemassa.
	'''

	# Katsotaan, olisiko sarjat siirretty jonnekin muualle:
	# yleensä tämä on tehty niin, että kansion nimi pysyy samana mutta sen sijainti on muuttunut
	indeksit = []
	ehdotukset = []
	for indeksi,sarja in enumerate(sarjalista):
		if not os.path.exists(sarja.tiedostosijainti):
			kansionimi = os.path.basename(sarja.tiedostosijainti)
			ehdokas = ""

			# Käydään tunnetut piirrettykansiot läpi ja katsotaan
			# olisiko siellä kansioita joilla puuttuvan nimi ja jotka eivät ole tietokannassa
			for piirrettykansio in PIIRRETTYDIKTI:
				for kansioehdokas in [alikansio for alikansio in kfun.kansion_sisalto(piirrettykansio)[1] if kansionimi in alikansio]:
					# tarkastetaan, onko sarjalistalla jo kansio jolla saman niminen kansio ja joka ei ole sarja itse
					# (tavallaan vähän huolestuttavaa jos on sama sarja moneen kertaan)
					if not any([muusarja.tiedostosijainti == sarja.tiedostosijainti for muusarja in sarjalista if muusarja is not sarja]):
						ehdokas = os.path.join(piirrettykansio, kansioehdokas)
						break
				if ehdokas:
					break
			ehdotukset.append(ehdokas)
			indeksit.append(indeksi)
			print(f"puuttuva: {sarja.tiedostosijainti}")
			print(f"ehdotus:  {ehdokas}")
	return(indeksit, ehdotukset)

def tarkasta_uudet(tunnetutsarjat):
	'''
	Tarkastaa, onko tunnetuihin piirrettykansioihin ilmaantunut kansioita,
	joita ei ole liitetty mihinkään tietokannan piirrossarjaan
	('tunnetutsarjat', lista Piirrettyjä)
	'''
	uudetkansiot = []
	for ylakansio in [kvak.KANSIO_AURINKOKALA, kvak.KANSIO_REDRUM, kvak.KANSIO_MICHIRU, kvak.KANSIO_SUZUYA, kvak.KANSIO_NUHMU]:
		for alikansio in kfun.kansion_sisalto(ylakansio)[1]:
			# Katsotaan, onko kansiota merkattu mihinkään sarjaan tiedostosijainniksi.
			# voisi olla "/tiedosto/polku in sarja.tiedostosijainti", mutta joskus on hankalia alikansio_settejä
			merkattu = False
			if any([sarja.tiedostosijainti == os.path.join(ylakansio,alikansio) for sarja in tunnetutsarjat]):
				merkattu = True
			# Jos kansiota ei ole merkattu mihinkään sarjaan, tarkistetaan vielä onko se sorttia
			# /kansio/jaksot.mkv vai /kansio/ekakausi/ekanjaksot.mkv + /kansio/tokakausi/tokanjaksot.mkv
			# Nää on ikäviä ja niistä pitäis päästä eroon, mutta bakabt rajoittaa...
			if not merkattu:
				for alialikansio in kfun.kansion_sisalto(os.path.join(ylakansio, alikansio))[1]:
					if any([sarja.tiedostosijainti==os.path.join(ylakansio,alikansio,alialikansio) for sarja in tunnetutsarjat]):
						merkattu = True
			# Jos ei alikansiotarkastelullakaan löytynyt mitään, kansio on tuntematon
			if not merkattu:
				print("Kansio {} ei ole tietokannassa".format(os.path.join(ylakansio, alikansio)))
				uudetkansiot.append(os.path.join(ylakansio, alikansio))
	return(uudetkansiot)

def poista_diktista(dikti, sarja):
	'''
	Poistaa sarjan diktistä, jotta tietokantaa voidaan päivittää.
	Joo, uniikit ID:t ois ihan näppäriä...
	'''
	for kansio in dikti:
		for d,diktisarja in enumerate(dikti[kansio]):
			if sarja is diktisarja:
				# Sarjat on samoja jos niiden tietokentät ovat samoja
				print("{} on {}".format(sarja.nimi, diktisarja.nimi))
				dikti[kansio].pop(d)
				break

def siisti_nimi(kansionimi):
	'''
	Muodostaa siivotun version sarjan nimestä,
	poistamalla tunnisteet ([OVA], [RAW] ymv)
	'''
	teosnimi = kansionimi
	for tunniste in TUNNISTEET:
		teosnimi = teosnimi.replace(tunniste, "")
	i = 0
	while teosnimi[i].isspace():
		i += 1
	j = len(teosnimi)-1
	while teosnimi[j].isspace():
		j -= 1
	return(teosnimi[i:j+1])

def lue_piirretyt():
	'''
	Lue piirretyt ennalta määrätyistä kansioista ja arvaa niille arvot
	'''
	for kansio in PIIRRETTYDIKTI:
		alikansiot = kfun.kansion_sisalto(kansio)[1]
		for teos in alikansiot:
			piirrossarja = Piirretty()
			piirrossarja.nimi = siisti_nimi(teos)

			piirrossarja.jaksoja = len([a for a in kfun.kansion_sisalto(os.path.join(kansio, teos))[0] if a.split(".")[-1].lower() in ["mkv", "avi"]])
			piirrossarja.tiedostosijainti = os.path.join(kansio, teos)

			if kansio is kvak.KANSIO_AURINKOKALA:
				piirrossarja.tagit.append("bakaBT")
			if kansio is kvak.KANSIO_MICHIRU or kansio is kvak.KANSIO_SUZUYA or kansio is kvak.KANSIO_NUHMU:
				piirrossarja.katsoneet.append("Pilperi")

			if "[RAW]" in teos:
				piirrossarja.tagit.append("RAW")

			if "[MOV]" in teos:
				piirrossarja.tyyppi.append("MOV")
			if "[OVA]" in teos:
				piirrossarja.tyyppi.append("OVA")
			if "[MOV]" not in teos and "OVA" not in teos:
				piirrossarja.tyyppi.append("TV")
			if piirrossarja.jaksoja > 0:
				PIIRRETTYDIKTI[kansio].append(piirrossarja)
			else:
				for alikansioteos in kfun.kansion_sisalto(os.path.join(kansio, teos))[1]:
					piirrossarja = Piirretty()
					

					piirrossarja.jaksoja = len([a for a in kfun.kansion_sisalto(os.path.join(kansio, teos, alikansioteos))[0] if a.split(".")[-1].lower() in ["mkv", "avi"]])
					piirrossarja.tiedostosijainti = os.path.join(kansio, teos, alikansioteos)
					piirrossarja.tagit = ["bakaBT"]
					if "MOV" in teos or "MOV" in alikansioteos:
						piirrossarja.tyyppi.append("MOV")
					if "OVA" in teos or "OVA" in alikansioteos:
						piirrossarja.tyyppi.append("OVA")
					if "MOV" not in teos and "OVA" not in teos and "MOV" not in alikansioteos and "OVA" not in alikansioteos:
						piirrossarja.tyyppi.append("TV")
					PIIRRETTYDIKTI[kansio].append(piirrossarja)	

def lue_piirretyt_mal_xml(xml=kvak.MAL_JOUNI):
	'''
	Lukee XML-tiedostosta sarjat Piirretty-entryiksi
	'''
	piirrettylista = []
	if os.path.exists(xml):
		puu = ET.parse(xml)
		juuri = puu.getroot()
		tyyppi = ""
		for sarja in juuri:
			# Kenen lista
			if sarja.tag == "myinfo":
				tyyppi = sarja.find("user_name").text
			# Piirrossarja
			elif sarja.tag == "anime":
				piirretty = Piirretty() # init
				# Lue MAL:ista luettavissa olevat kentät
				piirretty.nimi				= sarja.find("series_title").text
				piirretty.tyyppi			= [sarja.find("series_type").text]
				piirretty.jaksoja			= int(sarja.find("series_episodes").text)
				piirretty.kuvake			= sarja.find("series_animedb_id").text
				# piirretty.tagit				= sarja.find("series_title").text
				piirretty.mal 				= "https://myanimelist.net/anime/{}".format(piirretty.kuvake)
				if sarja.find("my_status").text == "Completed":
					piirretty.katsoneet = [tyyppi]
				# Lisää listan jatkoksi
				piirrettylista.append(piirretty)
	return(piirrettylista)

def taydenna_sarjatiedot_malilla(lokaalitiedot, malitiedot):
	'''
	Täydentää lokaaleja kovalevyjä lukemalla saadut sarjatiedot
	MAL-listasta napatuilla tiedoilla, koska kaikkea ei voi arvata lokaaleista
	tiedostoista ja kansioista. Läh. jaksomäärät on arvailua (OPED erikseen jne),
	katsomisstatus, MAL-URL (sarjaindeksi, joka myös kuvakkeen tiedostonimi)
	'''
	silti_vajaat = []
	for sarja in lokaalitiedot:
		sarjannimi = sarja.nimi.lower()
		taytetty = False
		for malisarja in malitiedot:
			if malisarja.nimi.lower() == sarjannimi or malisarja.nimi.lower() in [a.lower() for a in sarja.aliakset]:
				taytetty = True
				print(sarja, malisarja)
				sarja.tyyppi 	= malisarja.tyyppi
				sarja.jaksoja	= malisarja.jaksoja
				sarja.kuvake	= malisarja.kuvake
				sarja.mal		= malisarja.mal
				for katsoja in malisarja.katsoneet:
					if katsoja not in sarja.katsoneet:
						sarja.katsoneet.append(katsoja)
		if not taytetty:
			sarja.mal = "https://myanimelist.net/anime.php?q={}&type=0".format(sarjannimi.replace(" ", "+"))
			silti_vajaat.append(sarja)
	return(silti_vajaat)

def kirjoita_dikti(dikti=PIIRRETTYDIKTI, kohde=kvak.TIETOKANTATIEDOSTO):
	tiedosto = open(kohde, "w+", encoding="utf8")
	tiedosto.write("{\n")
	kansioita = len(dikti)-1
	for i,kansio in enumerate(dikti):
		tiedosto.write(f"\"{kansio}\":[\n")
		sarjoja = len(dikti[kansio])-1
		for j,sarja in enumerate(dikti[kansio]):
			tiedosto.write(str(sarja))
			tiedosto.write("{:s}\n".format(","*(j<sarjoja)))
		tiedosto.write("\t]{:s}\n".format(","*(i<kansioita)))
	tiedosto.write("}\n")
	tiedosto.close()

def taydenna(referenssitiedosto):
	'''
	Täydentää tietokannat vanhoilla backupeilla ('referenssitiedosto')
	'''
	if os.path.exists(referenssitiedosto):
		# Luetaan referenssitiedosto sarjadiktiksi
		f = open(referenssitiedosto, "r")
		refdikt = json.load(f)
		f.close()
		for kansio in refdikt:
			for i,refsarj in enumerate(refdikt[kansio]):
				refdikt[kansio][i] = Piirretty(refsarj)
		# Käydään itse muodostettu lista läpi ja katsotaan mitkä on korjattu
		for kansio in PIIRRETTYDIKTI:
			if kansio in refdikt.keys():
				for i,sarja in enumerate(PIIRRETTYDIKTI[kansio]):
					# Sarjan MAL-jutut puutteelliset, oisko toisessa
					if sarja.kuvake == "oletus":
						for j,refsarja in enumerate(refdikt[kansio]):
							# Löytyykö sarja jolla olisi sama tiedostosijainti mutta enemmän tietoa?
							if sarja.tiedostosijainti == refsarja.tiedostosijainti and refsarja.kuvake != "oletus":
								print("Sarjalle {} löytyi vastine, id {}".format(sarja.nimi, refsarja.kuvake))
								PIIRRETTYDIKTI[kansio][i] = refsarja
								if kansio in MANUAALIDIKTI.keys():
									poistettavat = []
									for k,manuaalisarja in enumerate(MANUAALIDIKTI[kansio]):
										if manuaalisarja.tiedostosijainti == refsarja.tiedostosijainti:
											poistettavat.append(k)
										poistettavat.reverse()
										for p in poistettavat:
											MANUAALIDIKTI[kansio].pop(p)
								break
	# rautalankaa koska jokin hassusti enkä jaksa setviä
	for kansio in PIIRRETTYDIKTI:
		for sarja in PIIRRETTYDIKTI[kansio]:
			if sarja.kuvake != "oletus" and "?q=" in sarja.mal:
				print(sarja)
				sarja.mal = "https://myanimelist.net/anime/{}".format(str(sarja.kuvake))
				print(sarja)
				# input()
	for kansio in MANUAALIDIKTI:
		poistettavat = []
		for p,sarja in enumerate(MANUAALIDIKTI[kansio]):
			if sarja.kuvake != "oletus" and "?q=" in sarja.mal:
				poistettavat.append(p)
		poistettavat.reverse()
		for p in poistettavat:
			MANUAALIDIKTI[kansio].pop(p)

def lataa_kuvat_urleista(dikti=PIIRRETTYDIKTI):
	korjattavaa = {}
	if os.path.exists(kvak.KUVAKANSIO):
		# lataa kuvien rungot (jo löytyvät sarjojen id:t)
		kuvat = [kfun.paate(a)[0] for a in kfun.kansion_sisalto(kvak.KUVAKANSIO)[0]]
		try:
			for kansio in PIIRRETTYDIKTI:
				print(kansio)
				for sarja in PIIRRETTYDIKTI[kansio]:
					if sarja.kuvake not in kuvat and "?q=" not in sarja.mal:
						# Jos kuvaa ei vielä löydy, lataa html:stä kiskottavalla urlilla
						print(sarja.nimi)
						print(sarja.mal)
						fp = urllib.request.urlopen(sarja.mal)
						htmltavut = fp.read()
						htmlstring = htmltavut.decode("utf8")
						# Sarjakuvat html:ssä lainausmerkeissä ja samalla etuliitteellä
						kuvaurl = htmlstring.split("https://cdn.myanimelist.net/images/anime/")[1].split("\"")[0]
						kuvaurl = "https://cdn.myanimelist.net/images/anime/{}".format(kuvaurl)
						paate = kfun.paate(kuvaurl)[1]
						print(kuvaurl)
						# tallenna kuva (jos pääte vaikuttaa järkevältä, pisin varmaan jpeg)
						if paate and len(paate) < 5:
							urllib.request.urlretrieve(kuvaurl, "{}{}.{}".format(kvak.KUVAKANSIO, sarja.kuvake, paate))
							kuvat.append(sarja.kuvake)
		except urllib.request.HTTPError as err:
			print("MAL nurin, ei saada kuvaa ladattua\n({})".format(err))

# Tietokantaa ei ole: lue vakiokansiot ja arvaa sarjojen ominaisuudet
# vähän riski ?
if not os.path.exists(kvak.TIETOKANTATIEDOSTO):
	lue_piirretyt()
	kirjoita_dikti()

# Tietokanta on jo olemassa: lue diktiksi ja diktiarvot piirretyiksi
else:
	f = open(kvak.TIETOKANTATIEDOSTO, "r")
	diktiversio = json.load(f)
	f.close()
	for kansio in diktiversio:
		PIIRRETTYDIKTI[kansio] = []
		for sarja in diktiversio[kansio]:
			piirretty = Piirretty(sarja)
			PIIRRETTYDIKTI[kansio].append(piirretty)

if "mal" in sys.argv:
	malipiirretyt	= lue_piirretyt_mal_xml(kvak.MAL_JOUNI)
	kvak.MAL_HAIKKU		= lue_piirretyt_mal_xml(kvak.MAL_HAIKKU)
	kvak.MAL_TOMI		= lue_piirretyt_mal_xml(kvak.MAL_TOMI)
	kvak.MAL_TURSA		= lue_piirretyt_mal_xml(kvak.MAL_TURSA)
	manuaalisesti = {}
	for kansio in PIIRRETTYDIKTI:
		vajaat = taydenna_sarjatiedot_malilla(PIIRRETTYDIKTI[kansio], malipiirretyt)
		vajaat_haik = taydenna_sarjatiedot_malilla(PIIRRETTYDIKTI[kansio], kvak.MAL_HAIKKU)
		for a in vajaat_haik:
			if a not in vajaat:
				vajaat.append(a)
		vajaat_tomi = taydenna_sarjatiedot_malilla(PIIRRETTYDIKTI[kansio], kvak.MAL_TOMI)
		for a in vajaat_tomi:
			if a not in vajaat:
				vajaat.append(a)
		vajaat_tursa = taydenna_sarjatiedot_malilla(PIIRRETTYDIKTI[kansio], kvak.MAL_TURSA)
		for a in vajaat_tursa:
			if a not in vajaat:
				vajaat.append(a)
		manuaalisesti[kansio] = vajaat
	kirjoita_dikti(manuaalisesti, kvak.MANUAALISARJAT)
	kirjoita_dikti()

# korjaa
# if "tilkitse" in sys.argv:
if False:
	if len(sys.argv) > 2:
		referenssitiedosto = os.path.join("/home/pilperi/Tietokannat/Piirretyt/", sys.argv[2])
	else:
		referenssitiedosto = "/home/pilperi/Tietokannat/Piirretyt/piirrossarjat-bk.json"
	print("Päivitä tiedostolla {}".format(referenssitiedosto))
	taydenna(referenssitiedosto)
	kirjoita_dikti(MANUAALIDIKTI, kvak.MANUAALISARJAT)
	kirjoita_dikti()
