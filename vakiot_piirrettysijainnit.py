import os
import sys
import json
import xml.etree.ElementTree as ET
import urllib.request
import funktiot_kansiofunktiot as kfun
from class_piirretyt import *

# Mikä kone kyseessä, missä asiat sijaitsevat?
kone = kvak.LOKAALI_KONE.lower()

konevaihtoehdot = ["olkkari", "murakumo"]
for arg in sys.argv:
	if "--kone=" in arg and arg.split("--kone=")[-1].lower() in konevaihtoehdot:
		kone = arg.split("--kone=")[-1]

if kone == "murakumo" and kvak.linux_murakumo:
	KANSIO_AURINKOKALA	= "/mnt/Olkkari/Aurinkokala/Animea/"
	KANSIO_REDRUM		= "/mnt/Olkkari/redrum/Anime/"
	KANSIO_MICHIRU		= "/mnt/Olkkari/Michiru/Anime/"
	KANSIO_SUZUYA		= "/mnt/Suzuya/Suzuyajako/Anime/"
	KANSIO_NUHMU		= "/mnt/Nuhmu/Nuhmujako/Anime/"

	TIETOKANTATIEDOSTO	= "/home/pilperi/Tietokannat/Piirretyt/piirrossarjat.json"
	KUVAKANSIO			= "/home/pilperi/Tietokannat/Piirretyt/Kuvat/"
	MAL_JOUNI				= "/home/pilperi/Tietokannat/Piirretyt/mal_jouni.xml"
	MAL_HAIKKU				= "/home/pilperi/Tietokannat/Piirretyt/mal_haikku.xml"
	MAL_TOMI				= "/home/pilperi/Tietokannat/Piirretyt/mal_tomi.xml"
	MAL_TURSA				= "/home/pilperi/Tietokannat/Piirretyt/mal_tursa.xml"

	MANUAALISARJAT		= "/home/pilperi/Tietokannat/Piirretyt/manuaalisesti.json"

# as in, olkkarikone
else:
	KANSIO_AURINKOKALA	= "/mnt/Aurinkokala/Animea/"
	KANSIO_REDRUM		= "/mnt/redrum/Anime/"
	KANSIO_MICHIRU		= "/mnt/Michiru/Anime/"
	KANSIO_SUZUYA		= "/mnt/Murakumo/Suzuyajako/Anime/"
	KANSIO_NUHMU		= "/mnt/Murakumo/Nuhmujako/Anime/"

	TIETOKANTATIEDOSTO	= "/home/olkkari/Tietokannat/Piirretyt/piirrossarjat.json"
	KUVAKANSIO			= "/home/olkkari/Tietokannat/Piirretyt/Kuvat/"
	MAL_JOUNI				= "/home/olkkari/Tietokannat/Piirretyt/mal_jouni.xml"
	MAL_HAIKKU				= "/home/olkkari/Tietokannat/Piirretyt/mal_haikku.xml"
	MAL_TOMI				= "/home/olkkari/Tietokannat/Piirretyt/mal_tomi.xml"
	MAL_TURSA				= "/home/olkkari/Tietokannat/Piirretyt/mal_tursa.xml"

	MANUAALISARJAT		= "/home/olkkari/Tietokannat/Piirretyt/manuaalisesti.json"

# Kuvakkeet
KUVA_PILPERI_0		= "Matskut/kuva_pilperi_0.png"
KUVA_PILPERI_1		= "Matskut/kuva_pilperi_1.png"
KUVA_HAIDER_0		= "Matskut/kuva_haider_0.jpg"
KUVA_HAIDER_1		= "Matskut/kuva_haider_1.jpg"
KUVA_NAILO_0		= "Matskut/kuva_nailo_0.jpg"
KUVA_NAILO_1		= "Matskut/kuva_nailo_1.jpg"
KUVA_LIHAKUNKARI_0	= "Matskut/kuva_lihakunkari_0.jpg"
KUVA_LIHAKUNKARI_1	= "Matskut/kuva_lihakunkari_1.jpg"
KUVA_TURSAKE_0		= "Matskut/kuva_tursake_0.png"
KUVA_TURSAKE_1		= "Matskut/kuva_tursake_1.png"
KUVA_NULL_0			= "Matskut/kuva_null_0.jpg"
KUVA_NULL_1			= "Matskut/kuva_null_1.jpg"

TUNNISTEET = ["[OVA]", "[MOV]", "[RAW]"]
PIIRRETTYDIKTI =	{
					KANSIO_AURINKOKALA:	[],
					KANSIO_REDRUM:		[],
					KANSIO_MICHIRU:		[],
					KANSIO_SUZUYA:		[],
					KANSIO_NUHMU:		[]
					}

MANUAALIDIKTI		= {}
if os.path.exists(MANUAALISARJAT):
	f = open(MANUAALISARJAT, "r")
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

def tarkasta_uudet():
	pass

def lue_piirretyt():
	'''
	Lue piirretyt ennalta määrätyistä kansioista ja arvaa niille arvot
	'''
	for kansio in PIIRRETTYDIKTI:
		if os.path.exists(kansio):
			alikansiot = kfun.kansion_sisalto(kansio)[1]
			for teos in alikansiot:
				piirrossarja = Piirretty()
				teosnimi = teos
				for tunniste in TUNNISTEET:
					teosnimi = teosnimi.replace(tunniste, "")
				i = 0
				while teosnimi[i].isspace():
					i += 1
				j = len(teosnimi)-1
				while teosnimi[j].isspace():
					j -= 1
				piirrossarja.nimi = teosnimi[i:j+1]

				piirrossarja.jaksoja = len([a for a in kfun.kansion_sisalto(os.path.join(kansio, teos))[0] if a.split(".")[-1].lower() in ["mkv", "avi"]])
				piirrossarja.tiedostosijainti = os.path.join(kansio, teos)

				if kansio is KANSIO_AURINKOKALA:
					piirrossarja.tagit.append("bakaBT")
				if kansio is KANSIO_MICHIRU or kansio is KANSIO_SUZUYA or kansio is KANSIO_NUHMU:
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
						teosnimi = alikansioteos
						for tunniste in TUNNISTEET:
							teosnimi = teosnimi.replace(tunniste, "")
						i = 0
						while teosnimi[i].isspace():
							i += 1
						j = len(teosnimi)-1
						while teosnimi[j].isspace():
							j -= 1
						piirrossarja.nimi = teosnimi[i:j+1]

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

def lue_piirretyt_mal_xml(xml=MAL_JOUNI):
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

def kirjoita_dikti(dikti=PIIRRETTYDIKTI, kohde=TIETOKANTATIEDOSTO):
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
	if os.path.exists(KUVAKANSIO):
		# lataa kuvien rungot (jo löytyvät sarjojen id:t)
		kuvat = [kfun.paate(a)[0] for a in kfun.kansion_sisalto(KUVAKANSIO)[0]]
		for kansio in PIIRRETTYDIKTI:
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
						urllib.request.urlretrieve(kuvaurl, "{}{}.{}".format(KUVAKANSIO, sarja.kuvake, paate))
						kuvat.append(sarja.kuvake)

# Tietokantaa ei ole: lue vakiokansiot ja arvaa sarjojen ominaisuudet
if not os.path.exists(TIETOKANTATIEDOSTO):
	lue_piirretyt()
	kirjoita_dikti()

# Tietokanta on jo olemassa: lue diktiksi ja diktiarvot piirretyiksi
else:
	f = open(TIETOKANTATIEDOSTO, "r")
	diktiversio = json.load(f)
	f.close()
	for kansio in diktiversio:
		PIIRRETTYDIKTI[kansio] = []
		for sarja in diktiversio[kansio]:
			piirretty = Piirretty(sarja)
			PIIRRETTYDIKTI[kansio].append(piirretty)

if "mal" in sys.argv:
	malipiirretyt	= lue_piirretyt_mal_xml(MAL_JOUNI)
	mal_haikku		= lue_piirretyt_mal_xml(MAL_HAIKKU)
	mal_tomi		= lue_piirretyt_mal_xml(MAL_TOMI)
	mal_tursa		= lue_piirretyt_mal_xml(MAL_TURSA)
	manuaalisesti = {}
	for kansio in PIIRRETTYDIKTI:
		vajaat = taydenna_sarjatiedot_malilla(PIIRRETTYDIKTI[kansio], malipiirretyt)
		vajaat_haik = taydenna_sarjatiedot_malilla(PIIRRETTYDIKTI[kansio], mal_haikku)
		for a in vajaat_haik:
			if a not in vajaat:
				vajaat.append(a)
		vajaat_tomi = taydenna_sarjatiedot_malilla(PIIRRETTYDIKTI[kansio], mal_tomi)
		for a in vajaat_tomi:
			if a not in vajaat:
				vajaat.append(a)
		vajaat_tursa = taydenna_sarjatiedot_malilla(PIIRRETTYDIKTI[kansio], mal_tursa)
		for a in vajaat_tursa:
			if a not in vajaat:
				vajaat.append(a)
		manuaalisesti[kansio] = vajaat
	kirjoita_dikti(manuaalisesti, MANUAALISARJAT)
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
	kirjoita_dikti(MANUAALIDIKTI, MANUAALISARJAT)
	kirjoita_dikti()