import os
import json

# Katso kansiorakenteesta, mikä kone on käytössä
#LOKAALI_KONE = "Murakumo" # linux-versio, tosin. Älä sekoita
linux_murakumo = False
if os.path.exists("/home/pilperi"):
	LOKAALI_KONE = "Murakumo" # linux-versio, tosin. Älä sekoita
	linux_murakumo = True
elif os.path.exists("/home/olkkari"):
	LOKAALI_KONE = "Olkkari"
elif os.path.exists("/home/pettankone"):
	LOKAALI_KONE = "Pettankone"
else:
	LOKAALI_KONE = "Murakumo"

NULL = {}.get(0)

# Murakumon tiedostosijainnit (linux-versio)
if LOKAALI_KONE == "Murakumo" and linux_murakumo:
	KANSIO_AURINKOKALA	= "/mnt/Olkkari/Aurinkokala/Animea/"
	KANSIO_REDRUM		= "/mnt/Olkkari/redrum/Anime/"
	KANSIO_MICHIRU		= "/mnt/Olkkari/Michiru/Anime/"
	KANSIO_MINT			= "/mnt/Olkkari/Mint/Anime/"
	KANSIO_SUZUYA		= "/mnt/Suzuya/Suzuyajako/Anime/"
	KANSIO_NUHMU		= "/mnt/Nuhmu/Anime/"

	# Lokaalien sarjojen tietokanta
	TIETOKANTATIEDOSTO	= "/home/pilperi/Tietokannat/Piirretyt/piirrossarjat.json"
	KUVAKANSIO			= "/home/pilperi/Tietokannat/Piirretyt/Kuvat/"

	# MAL XML:t
	MAL_JOUNI			= "/home/pilperi/Tietokannat/Piirretyt/mal_jouni.xml"
	MAL_HAIKKU			= "/home/pilperi/Tietokannat/Piirretyt/mal_haikku.xml"
	MAL_TOMI			= "/home/pilperi/Tietokannat/Piirretyt/mal_tomi.xml"
	MAL_TURSA			= "/home/pilperi/Tietokannat/Piirretyt/mal_tursa.xml"

	# Anilist-JSON-kokoelmat, käyttäjä-ID:n perusteella
	ANILIST				=	{
							100202:	"/home/pilperi/Tietokannat/Piirretyt/anilist_pilperi.json",		# Pilperi
							673:	"/home/pilperi/Tietokannat/Piirretyt/anilist_haider.json",		# Haider
							136448:	"/home/pilperi/Tietokannat/Piirretyt/anilist_lihakunkari.json",	# Lihakunkari
							1087:	"/home/pilperi/Tietokannat/Piirretyt/anilist_nailo.json",		# Nailo
							54882:	"/home/pilperi/Tietokannat/Piirretyt/anilist_tursake.json"		# Tursake
							}

	MANUAALISARJAT		= "/home/pilperi/Tietokannat/Piirretyt/manuaalisesti.json"

# Murakumon winukkaversio
elif LOKAALI_KONE == "Murakumo":
	# Murakumon winukkaversiolla ei vielä tarvittavia kalikoita ohjelman pyörittämiseen,
	# täytyy jossain välissä korjata

	KANSIO_AURINKOKALA	= NULL
	KANSIO_REDRUM		= NULL
	KANSIO_MICHIRU		= NULL
	KANSIO_SUZUYA		= NULL
	KANSIO_NUHMU		= NULL

	TIETOKANTATIEDOSTO	= NULL
	KUVAKANSIO			= NULL
	
	MAL_JOUNI			= NULL
	MAL_HAIKKU			= NULL
	MAL_TOMI			= NULL
	MAL_TURSA			= NULL

	# Anilist-JSON-kokoelmat, käyttäjä-ID:n perusteella
	ANILIST				=	{
							100202:	NULL,		# Pilperi
							673:	NULL,		# Haider
							136448:	NULL,		# Lihakunkari
							1087:	NULL,		# Nailo
							54882:	NULL		# Tursake
							}

	MANUAALISARJAT		= NULL


# Olkkarikoneen tiedostosijainnit
elif LOKAALI_KONE == "Olkkari":
	KANSIO_AURINKOKALA	= "/mnt/Aurinkokala/Animea/"
	KANSIO_REDRUM		= "/mnt/redrum/Anime/"
	KANSIO_MICHIRU		= "/mnt/Michiru/Anime/"
	KANSIO_MINT			= "/mnt/Mint/Anime/"
	KANSIO_SUZUYA		= "/mnt/Murakumo/Suzuyajako/Anime/"
	KANSIO_NUHMU		= "/mnt/Murakumo/Nuhmujako/Anime/"

	TIETOKANTATIEDOSTO	= "/home/olkkari/Tietokannat/Piirretyt/piirrossarjat.json"
	KUVAKANSIO			= "/home/olkkari/Tietokannat/Piirretyt/Kuvat/"

	MAL_JOUNI			= "/home/olkkari/Tietokannat/Piirretyt/mal_jouni.xml"
	MAL_HAIKKU			= "/home/olkkari/Tietokannat/Piirretyt/mal_haikku.xml"
	MAL_TOMI			= "/home/olkkari/Tietokannat/Piirretyt/mal_tomi.xml"
	MAL_TURSA			= "/home/olkkari/Tietokannat/Piirretyt/mal_tursa.xml"

	# Anilist-JSON-kokoelmat, käyttäjä-ID:n perusteella
	ANILIST				=	{
							100202:	"/home/olkkari/Tietokannat/Piirretyt/anilist_pilperi.json",		# Pilperi
							673:	"/home/olkkari/Tietokannat/Piirretyt/anilist_haider.json",		# Haider
							136448:	"/home/olkkari/Tietokannat/Piirretyt/anilist_lihakunkari.json",	# Lihakunkari
							1087:	"/home/olkkari/Tietokannat/Piirretyt/anilist_nailo.json",		# Nailo
							54882:	"/home/olkkari/Tietokannat/Piirretyt/anilist_tursake.json"		# Tursake
							}

	MANUAALISARJAT		= "/home/olkkari/Tietokannat/Piirretyt/manuaalisesti.json"


# Yhteiset
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
