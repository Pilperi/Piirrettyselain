# Piirrettyselain
Graafinen ohjelma piirrettykansioiden selaamiseen, Qt5-pohjainen ja pyörii python3.8+:lla.
Aina välillä ollut ongelmana se, että piirrossarjoja on niin monta ja niin monelle kovalevylle hajautettuna, että yksittäisen sarjan sijainnin etsiminen on ollut työn ja tuskan takana. Moni näistä kovalevyistä vieläpä sijaitsee kotiverkon toisella puolella, eli hakeminen on hidasta ja tiedostoselain hyytyy pystyyn kesken homman.

Varsinainen "ajettava" pääikkuna on `main_piirrettyselain.py`, joka kutsuu tarvittaessa esiin muita ikkunoita (`ikkuna_*.py` Tietokannat muodostetaan ja tarkistetaan `vakiot_piirrettysijainnit.py` kutsuttaessa, ja loput tiedostot on aika itseselittäviä kokoelmia luokkia, funktioita, vakioita ja ui-materiaaleja.


**TEHDYT ASIAT:**

	- Tietokantojen kasaus
	- Pääikkuna (lista sarjoista, sarjojen perustiedot ja napit jotka vievät MAL ja kansiosijaintiin)
	- Sarjan perustietojen muokkaaminen pääikkunan kautta (korjaa nimi, aliaksia, jaksomäärä ymv)
	- Hakuikkuna jolla voi etsiä sarjoja tietyillä kriteereillä (nimi, jaksomäärä, tyyppi, tietty tyyppi ei ole vielä nähnyt, ...)


**PITÄISI TOTEUTTAA:**

	- Automaattinen tarkastus, onko tietokannan sarjat vielä siellä missä pitääkin
		TYÖN ALLA
			+ Käy sarjat läpi ja listaa ne, jotka kadonneet
			+ Katso, olisiko saman niminen kansio jossain muualla ja ei tietokannassa
			- Laita käyttäjä päivittämään sarjan sijainti (paluusignaalien tunnistus todo)

	- Uusien sarjojen tunnistus (käytännössä sama kuin poistuneiden tunnistus, ajojärjestyksessä oltava sen jälkeen)

	- Tagien perusteella hakeminen (kolmitilainen checkbox-lista, "on oltava" vs "ei saa olla" vs "ei väliä")

	- Anilist-API (jottei tarvitse aina manuaalisesti kliksutella ketkä on kattonu sarjan sitten viime käynnistyskerran)


**TEHTÄVIÄ PIKKUJUTTUJA:**

	- Vakiojutut `vakiot_piirrettysijainnit.py` -> `vakiot_kansiovakiot.py` ja uudelleennimeäminen funktiokokoelmaksi (yhtenäisyys)

	- Hakukriteerien nollaaminen kun hakuikkuna suljetaan (Ikkunan paluuarvojuttu? Jotenkin muuten?)