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
	SCREENSHOT_FOLDER			= "/mnt/Suzuya/Suzuyajako/Screenshots/Jaottelemattomat/"
	SCREENSHOT_DEST_FOLDER		= "/mnt/Suzuya/Suzuyajako/Screenshots/Jaotellut/"
	SCREENSHOT_BACKUP_FOLDER	= "/mnt/Faust/Screenshot backup/Jaotellut/"

	MURAKUMO_INTERNET			= "/mnt/Norot/Data/INTERNET/"
	MURAKUMO_SCREENSHOTS		= "/mnt/Suzuya/Suzuyajako/Screenshots/Jaottelemattomat/"
	INTERNET_FOLDER				= MURAKUMO_INTERNET

	# Winukalla kukin oman levykirjaimen alla
	PETTAN_FOLDER				= "/mnt/Taira/Inbox/"
	PETTAN_MUSIIKKI 			= "/mnt/Taira/Musiikki/"
	PETTAN_KUVAT				= "/mnt/Taira/Kuvat/"
	PETTAN_HASHIT				= "/mnt/Taira/Inbox/Hashikirjasto/"
	
	# Hashikirjastot
	LOKAALIT_HASHIT				= "/mnt/Norot/Data/Hashikirjasto/"

	GEEQUIETIEDOSTO				= "/mnt/Suzuya/Suzuyajako/Scripts/kuvalista_geequie.gqv"
	IRFANTIEDOSTO				= "/mnt/Suzuya/Suzuyajako/Scripts/kuvalista_irfan.txt"
	RAAKATIEDOSTO				= "/mnt/Suzuya/Suzuyajako/Scripts/kuvalista_raaka"

	LOGFILE						= "/mnt/Suzuya/Privaatti/Projektit/Koodaushommat/Synkka/filecheck_log.log"
	READMEFILE					= "/mnt/Suzuya/Suzuyajako/Scripts/readme"

	MURAKUMO_MUSIIKKI			= "/mnt/Suzuya/Suzuyajako/Musiikki/"
	MUSIIKKI_FOLDER				= MURAKUMO_MUSIIKKI

	# Pettankoneen kansiot
	NIPAMUSA_FOLDER				= "/mnt/Taira/Musiikki/Nipa/"
	NIPAKUVA_FOLDER				= "/mnt/Taira/Kuvat/Nipa/"
	JOUNIMUSA_FOLDER			= MUSIIKKI_FOLDER
	JOUNIKUVA_FOLDER			= INTERNET_FOLDER
	MUUMUSA_FOLDER				= "/mnt/Taira/Musiikki/Muut/"
	MUUKUVA_FOLDER				= "/mnt/Taira/Kuvat/Muut/"

	SOITTOLISTA					= "/mnt/Suzuya/Suzuyajako/Scripts/soittolista.m3u8"
	SOITTOLISTA_KAIKKI			= "/mnt/Suzuya/Suzuyajako/Scripts/kaikkimusiikki.m3u8"

	MUSAKANSIO_JSON				= "/mnt/Suzuya/Suzuyajako/Scripts/musalistan_kansiot.json"
	
	# Vertailtavat hashikirjastot ja mitä verrataan mihinkin
	HASHIT =					{
								"HASHIT_LOKAALIT": 	"/mnt/Norot/Data/Hashikirjasto/Murakumo/",

								"Musiikki":			False,
								"Kuvat":			False,
								"Screenshots":		"/mnt/Norot/Data/Hashikirjasto/Olkkari/"
								}
	TIEDOSTOPOLUT = {
								"Lokaalit":	{
											"Musiikki":     "/mnt/Suzuya/Suzuyajako/Musiikki/",
											"Kuvat":        "/mnt/Norot/Data/INTERNET/",
											"Screenshots":  "/mnt/Suzuya/Suzuyajako/Screenshots/Jaotellut/"
											},
								"Etät":		{
											"Musiikki":     False,
											"Kuvat":        False,
											"Screenshots":  False
											}
								}

# Murakumon winukkaversio
elif LOKAALI_KONE == "Murakumo":
	SCREENSHOT_FOLDER			= "S:/Suzuyajako/Screenshots/Jaottelemattomat/"
	SCREENSHOT_DEST_FOLDER		= "S:/Suzuyajako/Screenshots/Jaotellut/"
	SCREENSHOT_BACKUP_FOLDER	= "F:/Screenshot backup/Jaotellut/"

	MURAKUMO_INTERNET			= "S:/Suzuyajako/INTERNET/"
	MURAKUMO_SCREENSHOTS		= "S:/Suzuyajako/Screenshots/Jaottelemattomat/"
	INTERNET_FOLDER				= MURAKUMO_INTERNET

	# Winukalla kukin oman levykirjaimen alla
	PETTAN_FOLDER				= "X:/"
	PETTAN_MUSIIKKI 			= "Y:/"
	PETTAN_KUVAT				= "Z:/"
	PETTAN_HASHIT				= "X:/Hashikirjasto/"
	
	# Hashikirjastot
	LOKAALIT_HASHIT				= "C:/Data/Hashikijasto/"

	GEEQUIETIEDOSTO				= "S:/Suzuyajako/Scripts/kuvalista_geequie.gqv"
	IRFANTIEDOSTO				= "S:/Suzuyajako/Scripts/kuvalista_irfan.txt"
	RAAKATIEDOSTO				= "S:/Suzuyajako/Scripts/kuvalista_raaka"

	LOGFILE						= "S:/Suzuyajako/Scripts/filecheck_log.log"
	READMEFILE					= "S:/Suzuyajako/Scripts/readme"

	MURAKUMO_MUSIIKKI			= "S:/Suzuyajako/Musiikki/"
	MUSIIKKI_FOLDER				= MURAKUMO_MUSIIKKI

	# Pettankoneen kansiot
	NIPAMUSA_FOLDER				= "Y:/Nipa/"
	NIPAKUVA_FOLDER				= "Z:/Nipa/"
	JOUNIMUSA_FOLDER			= MUSIIKKI_FOLDER
	JOUNIKUVA_FOLDER			= INTERNET_FOLDER
	MUUMUSA_FOLDER				= "Y:/Muut/"
	MUUKUVA_FOLDER				= "Z:/Muut/"

	SOITTOLISTA					= "S:/Suzuyajako/Scripts/soittolista.m3u8"
	SOITTOLISTA_KAIKKI			= "S:/Suzuyajako/Scripts/kaikkimusiikki.m3u8"

	MUSAKANSIO_JSON				= "S:/Suzuyajako/Scripts/musalistan_kansiot.json"
	
	# Vertailtavat hashikirjastot ja mitä verrataan mihinkin
	HASHIT =					{
								"HASHIT_LOKAALIT": 	"C:/Data/Hashikirjasto/Murakumo/",

								"Musiikki":			False,
								"Kuvat":			False,
								"Screenshots":		"C:/Data/Hashikirjasto/Olkkari/"
								}
	TIEDOSTOPOLUT = {
								"Lokaalit":	{
											"Musiikki":     "S:/Suzuyajako/Musiikki/",
											"Kuvat":        "S:/Suzuyajako/INTERNET/",
											"Screenshots":  "S:/Suzuyajako/Screenshots/Jaotellut/"
											},
								"Etät":		{
											"Musiikki":     False,
											"Kuvat":        False,
											"Screenshots":  False
											}
								}

# Pettankoneen tiedostosijainnit
elif LOKAALI_KONE == "Pettankone":
	SCREENSHOT_FOLDER			= "S:/Suzuyajako/Screenshots/Jaottelemattomat/"
	SCREENSHOT_DEST_FOLDER		= "S:/Suzuyajako/Screenshots/Jaotellut/"
	SCREENSHOT_BACKUP_FOLDER	= "F:/Screenshot backup/Jaotellut/"

	MURAKUMO_INTERNET			= "S:/Suzuyajako/INTERNET/"
	MURAKUMO_SCREENSHOTS		= "S:/Suzuyajako/Screenshots/"
	INTERNET_FOLDER				= MURAKUMO_INTERNET

	# Winukalla kukin oman levykirjaimen alla
	PETTAN_FOLDER				= "X:/"
	PETTAN_MUSIIKKI 			= "Y:/"
	PETTAN_KUVAT				= "Z:/"
	PETTAN_HASHIT				= "X:/Hashikirjasto/"
	
	# Hashikirjastot
	LOKAALIT_HASHIT				= "C:/Data/Hashikijasto/"

	GEEQUIETIEDOSTO				= "S:/Suzuyajako/Scripts/kuvalista_geequie.gqv"
	IRFANTIEDOSTO				= "S:/Suzuyajako/Scripts/kuvalista_irfan.txt"
	RAAKATIEDOSTO				= "S:/Suzuyajako/Scripts/kuvalista_raaka"

	LOGFILE						= "S:/Suzuyajako/Scripts/filecheck_log.log"
	READMEFILE					= "S:/Suzuyajako/Scripts/readme"

	MURAKUMO_MUSIIKKI			= "S:/Suzuyajako/Musiikki/"
	MUSIIKKI_FOLDER				= MURAKUMO_MUSIIKKI

	# Pettankoneen kansiot
	NIPAMUSA_FOLDER				= "Y:/Nipa/"
	NIPAKUVA_FOLDER				= "Z:/Nipa/"
	JOUNIMUSA_FOLDER			= MUSIIKKI_FOLDER
	JOUNIKUVA_FOLDER			= INTERNET_FOLDER
	MUUMUSA_FOLDER				= "Y:/Muut/"
	MUUKUVA_FOLDER				= "Z:/Muut/"

	SOITTOLISTA					= "S:/Suzuyajako/Scripts/soittolista.m3u8"
	SOITTOLISTA_KAIKKI			= "S:/Suzuyajako/Scripts/kaikkimusiikki.m3u8"

	MUSAKANSIO_JSON				= "S:/Suzuyajako/Scripts/musalistan_kansiot.json"
	
	# Vertailtavat hashikirjastot ja mitä verrataan mihinkin
	HASHIT =					{
								"HASHIT_LOKAALIT": 	"C:/Data/Hashikirjasto/Murakumo/",

								"Musiikki":			False,
								"Kuvat":			False,
								"Screenshots":		"C:/Data/Hashikirjasto/Olkkari/"
								}
	TIEDOSTOPOLUT = {
								"Lokaalit":	{
											"Musiikki":     "S:/Suzuyajako/Musiikki/",
											"Kuvat":        "S:/Suzuyajako/INTERNET/",
											"Screenshots":  "S:/Suzuyajako/Screenshots/Jaotellut/"
											},
								"Etät":		{
											"Musiikki":     False,
											"Kuvat":        False,
											"Screenshots":  False
											}
								}

# Olkkarikoneen tiedostosijainnit
elif LOKAALI_KONE == "Olkkari":
	SCREENSHOT_FOLDER			= "/home/olkkari/Pictures/Screenshots/Jaottelemattomat/"
	SCREENSHOT_DEST_FOLDER		= "/mnt/Data/Jouni/Screenshots/Jaotellut/"
	SCREENSHOT_BACKUP_FOLDER	= "/mnt/redrum/Screenshots/Jaotellut/"

	#MURAKUMO_INTERNET			= "/mnt/Murakumo/Suzuyajako/INTERNET/"
	MURAKUMO_INTERNET			= "/mnt/Murakumo/INTERNET/"
	MURAKUMO_SCREENSHOTS		= "/mnt/Murakumo/Suzuyajako/Screenshots/Jaottelemattomat/"
	INTERNET_FOLDER				= "/home/olkkari/Pictures/INTERNET/"

	# Winukalla kukin oman levykirjaimen alla
	PETTAN_FOLDER				= "/mnt/Taira/Inbox/"
	PETTAN_MUSIIKKI 			= "/mnt/Taira/Musiikki/Jouni/"
	PETTAN_KUVAT				= "/mnt/Taira/Kuvat/Jouni/INTERNET/"
	PETTAN_HASHIT				= "/mnt/Taira/Inbox/Hashikirjasto/"
	
	# Hashikirjastot
	LOKAALIT_HASHIT				= "/home/olkkari/Tietokannat/Hashikirjasto/"

	GEEQUIETIEDOSTO				= "/home/olkkari/Tietokannat/kuvalista_geequie.gqv"
	IRFANTIEDOSTO				= "/home/olkkari/Tietokannat/kuvalista_irfan.txt"
	RAAKATIEDOSTO				= "/home/olkkari/Tietokannat/kuvalista_raaka"

	LOGFILE						= "/home/olkkari/Tietokannat/filecheck_log.log"
	READMEFILE					= "/home/olkkari/Tietokannat/readme"

	#MURAKUMO_MUSIIKKI			= "/mnt/Murakumo/Suzuyajako/Musiikki/"
	MURAKUMO_MUSIIKKI			= "/mnt/Murakumo/Suzuyajako/Musiikki/"
	MUSIIKKI_FOLDER				= "/mnt/Data/Jouni/Musiikki/"

	# Pettankoneen kansiot
	NIPAMUSA_FOLDER				= "/mnt/Taira/Musiikki/Nipa/"
	NIPAKUVA_FOLDER				= "/mnt/Taira/Kuvat/Nipa/"
	JOUNIMUSA_FOLDER			= MURAKUMO_MUSIIKKI
	JOUNIKUVA_FOLDER			= MURAKUMO_INTERNET
	MUUMUSA_FOLDER				= "/mnt/Taira/Musiikki/Muut/"
	MUUKUVA_FOLDER				= "/mnt/Taira/Kuvat/Muut/"

	SOITTOLISTA					= "/home/olkkari/Tietokannat/soittolista.m3u8"
	SOITTOLISTA_KAIKKI			= "/home/olkkari/Tietokannat/kaikkimusiikki.m3u8"

	MUSAKANSIO_JSON				= "/home/olkkari/Tietokannat/musalistan_kansiot.json"
	
	# Vertailtavat hashikirjastot ja mitä verrataan mihinkin
	HASHIT =					{
								"HASHIT_LOKAALIT":	"/home/olkkari/Tietokannat/Hashikirjasto/Olkkari/",

								"Musiikki":			"/home/olkkari/Tietokannat/Hashikirjasto/Murakumo/Musiikki/",
								"Kuvat":			"/home/olkkari/Tietokannat/Hashikirjasto/Murakumo/Kuvat/",
								"Screenshots":		False
								}
	TIEDOSTOPOLUT = {
								"Lokaalit":	{
											"Musiikki":     "/mnt/Data/Jouni/Musiikki/",
											"Kuvat":        "/home/olkkari/Pictures/INTERNET/",
											"Screenshots":  "/mnt/Data/Jouni/Screenshots/Jaotellut/"
											},
								"Etät":		{
											"Musiikki":     MURAKUMO_MUSIIKKI,
											"Kuvat":        MURAKUMO_INTERNET,
											"Screenshots":  False
											}
								}

	# Jos ei ole yhteyttä Murakumoon, käytä pettania
	#if not os.listdir(MURAKUMO_INTERNET):
	#	print("Murakumo INTERNET offline(?), käytä Pettania")
	#	TIEDOSTOPOLUT["Etät"]["Kuvat"]		= PETTAN_KUVAT
	#if not os.listdir(MURAKUMO_MUSIIKKI):
	#	print("Murakumo Musiikki offline(?), käytä Pettania")
	#	TIEDOSTOPOLUT["Etät"]["Musiikki"]	= PETTAN_MUSIIKKI
	#input("Kuittaus")

# Asiat jotka eivät riipu käytettävästä tietokoneesta vaan edellisistä vakioista
# Musiikkidikti
MUSADIKTI = {}
KIELLETYT = []
TIEDOSTOMUODOT = []
if os.path.exists(MUSAKANSIO_JSON):
	MUSADIKTI = json.load(open(MUSAKANSIO_JSON, 'r'))
	if "Sivuuta" in MUSADIKTI.keys() and "Tiedostomuodot" in MUSADIKTI.keys():
		KIELLETYT		= MUSADIKTI.get("Sivuuta")
		TIEDOSTOMUODOT	= MUSADIKTI.get("Tiedostomuodot")

# Kansiot joista haetaan kuvat kuvaesitykseen
DIAESITYS_FOLDERS = [
					  'Art (animango)'
					  ,'Art (kankore)'
					  ,'Art (misc)'
					  ,'Art (originaali)'
					  ,'Art (pelit)'
					  ,'Art (touhou)'
					  ,'Art (VN)'
					  ,'Art (vocaloid ym)'
					  ,'Cropit yms'
					  ,'Gifuilut jp'
					  ,'Japanese bird'
					  ,'Jouni Ei Tallentais'
					  ,'jpgen'
					  ,'Kantoku'
					  ,'KIG & nuket'
					  ,'Madotsuki'
					  ,'Mahjong'
					  ,'random'
					  ,'Randomit ja meemut jp'
					  ,'Sekalainen jp'
					  ,'Sekalaisia matskuja'
					  ,'Touhou'
					  ,'VN'
					  ]

# ottaen mukaan vain tiedostomuodot:
KUVA_TIEDOSTOMUODOT = ["jpg", "jpeg", "png", "gif", "bmp", "tiff"]