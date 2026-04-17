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
  - Poista ilmoitus
  - Avaa oma profiili/käyttäjäsivu
  - valitse kategoria ilmoitukselle
  - avaa ilmoituksen tekijän käyttäjäsivu 


-
-
-
Sovelluksen kuvaus/työn alla olevat toiminnot:  Käyttäjä voi jättää arvioita toisista käyttäjistä toteutuneen työn jälkeen, haussa voi rajata töitä sijainnin / työn tyypin avulla, sivun ulkoasun rakentaminen css avulla 
