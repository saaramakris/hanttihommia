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
6. Siirry selaimessa päätteen kertomaan osoitteeseen 

Sovellusta voi testata esimerkiksi näin: 
1. Luo käyttäjä A.
2. Kirjaudu sisään käyttäjänä A ja lisää ilmoitus.
3. Kirjaudu ulos.
4. Luo käyttäjä B.
5. Hae käyttäjän A ilmoitus.
6. Lähetä ilmoitukseen viesti.
7. Kirjaudu ulos
8. Kirjaudu käyttäjänä A ja vastaa viestiin.
9. Muokkaa ja poista omaa ilmoitusta.

Sovellukseen voi lisätä ilmoituksia erilaisista töistä, ilmoitukselle voi valita luokan ja siihen on täytettävä kuvaus ja maksettava palkkio. Kirjautunut käyttäjä voi tarkastella ilmoitusten lähettäjien profiileja ja nähdä sieltä esim. Kuinka kauan käyttäjä on ollut jäsenenä ja kuinka monta ilmoitusta hänellä on sillä hetkellä aktiivisena. Ilmoituksen jättäneelle käyttäjälle voi lähettää viestin ja hän voi vastata siihen. Postilaatikossa uusin viestiketju nousee ylimmäiseksi ja esikatselussa näkyy viestiketjun viimeisin viesti. Sovelluksen uk´lkoasu on tehty HTML:llä. 
