import json
import piirrettysijainnit as ps

f = open("/home/pilperi/Tietokannat/Piirretyt/piirrossarjat.json", "r")
dikti = json.load(f)
f.close()
for kansio in dikti:
	print(kansio)
	for i,s in enumerate(dikti[kansio]):
		sarja = ps.Piirretty(s)
		try:
			malid = int(sarja.kuvake)
		except ValueError:
			malid = sarja.kuvake
		if type(malid) is int and "q=" in sarja.mal:
			sarja.mal = "https://myanimelist.net/anime/{}".format(malid)
		dikti[kansio][i] = sarja
ps.kirjoita_dikti(dikti, "/home/pilperi/Tietokannat/Piirretyt/piirrossarjat.json")