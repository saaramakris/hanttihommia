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



- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään sovellukseen ilmoituksia. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään ilmoituksia.
- Käyttäjä näkee sovellukseen lisätyt ilmoitukset. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät ilmoitukset.
- Käyttäjä pystyy etsimään tietokohteita hakusanalla tai muulla perusteella (esim. sijainti, maksettava palkkio). Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä ilmoituksia.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja (esim. käyttäjän saamat arvostelut, ilmoitusten määrä, tehtyjen töiden määrä) ja käyttäjän lisäämät ilmoitukset.
- Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokittelun. Mahdolliset luokat ovat tietokannassa (esim. työn tyyppi, kesto, maksettu palkkio)
- Käyttäjä voi jättää arvioita toisista käyttäjistä toteutuneen työn jälkeen 
