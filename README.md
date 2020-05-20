# Piirrettyselain
Graafinen ohjelma piirrettykansioiden selaamiseen, Qt5-pohjainen ja pyörii python3.8+:lla (kunhan on requests-moduuli).
Aina välillä ollut ongelmana se, että piirrossarjoja on niin monta ja niin monelle kovalevylle hajautettuna, että yksittäisen sarjan sijainnin etsiminen on ollut työn ja tuskan takana. Moni näistä kovalevyistä vieläpä sijaitsee kotiverkon toisella puolella, eli hakeminen on hidasta ja tiedostoselain hyytyy pystyyn kesken homman.

Varsinainen "ajettava" pääikkuna on `main_piirrettyselain.py`, joka kutsuu tarvittaessa esiin muita ikkunoita (`ikkuna_*.py` Tietokannat muodostetaan ja tarkistetaan `funktiot_piirrettyfunktiot.py` kutsuttaessa, ja loput tiedostot on aika itseselittäviä kokoelmia luokkia, funktioita, vakioita ja ui-materiaaleja.


**TEHDYT ASIAT:**

	+ Tietokantojen kasaus
	+ Pääikkuna (lista sarjoista, sarjojen perustiedot ja napit jotka vievät MAL ja kansiosijaintiin)
	+ Sarjan perustietojen muokkaaminen pääikkunan kautta (korjaa nimi, aliaksia, jaksomäärä ymv)
	+ Hakuikkuna jolla voi etsiä sarjoja tietyillä kriteereillä (nimi, jaksomäärä, tyyppi, tietty tyyppi ei ole vielä nähnyt, ...)
	+ Anilist-API (jottei tarvitse aina manuaalisesti kliksutella ketkä on kattonu sarjan sitten viime käynnistyskerran)
	+ Automaattinen tarkastus, onko tietokannan sarjat vielä siellä missä pitääkin
	+ Uusien sarjojen tunnistus (käytännössä sama kuin poistuneiden tunnistus, ajojärjestyksessä oltava sen jälkeen)

**PITÄISI TOTEUTTAA:**

	- Tagien perusteella hakeminen (kolmitilainen checkbox-lista, "on oltava" vs "ei saa olla" vs "ei väliä")

	- Sarjan kansiosijainnin muokkausmahdollisuus

	- Mahdollisuus poistaa sarja tietokannasta

	- Tietokanta tunnetuille hämäyskansioille (ne mille käyttäjä painaa "tämä ei ole sarja" kun ne löydetään)


**TEHTÄVIÄ PIKKUJUTTUJA:**

	+ Vakiojutut `vakiot_piirrettysijainnit.py` -> `vakiot_kansiovakiot.py` ja uudelleennimeäminen funktiokokoelmaksi (yhtenäisyys)

	+ Hakukriteerien nollaaminen kun hakuikkuna suljetaan

	- Satunnaissarjanappi hakuikkunaan

	- Puuttuvien sarjojen käsittelyssä: tarkasta onko asetettava kansio jo jonkun tunnetun sarjan kohdekansio (entä jos on..?)

	+ Puuttuvien sarjojen nappiasettelu kuntoon: meinaan koko ajan painaa "OK"-nappia (joka sulkee ikkunan) kun pitäisi painaa "Aseta"

	- Puuttuvien sarjojen ikkunassa: "Luotan sinuun"-nappi, joka käyttää kaikki ehdotukset

	- Puuttuvien sarjojen ikkunassa: korvaa dialoginapit norminapeilla, jottei Enter sulje ikkunaa

	- Uusien sarjojen tunnistukseen se ettei laske kansiota jollei siellä ole yhtään videota

	- Uusien sarjojen lisäyksessä: lisää nuppi josta saa säädettyä hakutulosten määrää (hidas)

	- Uusien sarjojen lisäyksessä: "Hae toiset N"-nappi, jolla toiset hakutulokset

	- Uusien sarjojen lisäyksessä: kaikki MAL-sarjat näköjään ei olekaan AL:ssä -> nimi erikseen

	- Tietokannan korjausfunktio: tunnista sarjat joille on löydetty MAL-linkki mutta kuvakkeena on edelleen "oletus"

	- Implementoi automaaginen kuvienlataus osaksi tarkistusrumbaa (paremmin)

	- Tagien lisääminen ja poistaminen, automaaginen tunnistus kansiosta

	- bakaBT-sarjojen fiksu tunnistaminen (lista bakaBT-sarjoista, saiskohan qbitista jonkun fiksun listan ulos..?)
