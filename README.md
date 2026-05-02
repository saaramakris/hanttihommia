# hanttihommia

Käynnistysohje: 
1. lataa repositorio
  - git clone https://github.com/saaramakris/hanttihommia.git
  - cd hanttihommia
3. luo virtuaaliympäristö
  - python3 -m venv venv
  - source venv/bin/activate
4. luo tietokanta 
  - sqlite3 database.db < schema.sql
5. käynnistä sovellus 
  - flask run 

Sovelluksessa on tällä hetkellä seuraavat toiminnot: 
  - Luo uusi käyttäjätunnus
  - Kirjaudu sisään
  - Lisää uusi ilmoitus
  - Tarkista, että ilmoitus näkyy etusivulla
  - Hae ilmoitusta hakusanalla
  - Avaa ilmoitus
  - Muokkaa ilmoitusta
  (- Poista ilmoitus)
  - Avaa oma profiili/käyttäjäsivu
  - valitse kategoria ilmoitukselle
  - avaa ilmoituksen tekijän käyttäjäsivu
  - Lähetä viesti ilmoituksen tekijälle 
  - Vastaa viestin lähettäjälle / lähetä uusi viesti ketjuun 


-
-
-
Sovelluksen kuvaus/työn alla olevat toiminnot:  haussa voi rajata töitä sijainnin / työn tyypin avulla, postilaatikkoon erilliset kansiot saapuneille ja lähetetyille, sivun ulkoasun rakentaminen css avulla,
