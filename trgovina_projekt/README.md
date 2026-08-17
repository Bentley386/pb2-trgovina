# Trgovina (oglasnik)

Django aplikacija za oglasnik (kupim/prodajam), narejena pri predmetu Podatkovne baze 2.

## Struktura

- `trgovina/` – nastavitve projekta (settings, urls)
- `trgovina_app/` – glavna aplikacija
  - `models.py` – `Kategorija`, `Oglas`, `Transakcija`
  - `views.py`, `urls.py` – pogledi in poti
  - `forms.py` – obrazec za dodajanje/urejanje oglasa
  - `templates/` – HTML predloge (Bulma CSS)
  - `admin.py` – registracija modelov v skrbniškem vmesniku

## Podatkovni model

- **Kategorija**: naziv (npr. "Šport", "Elektronika")
- **Oglas**: naslov, opis, cena, tip (Kupim/Prodajam), lastnik, kategorije, ali je še aktiven
- **Transakcija**: zabeleži nakup oglasa (kupec, cena, datum) – en oglas je lahko kupljen samo enkrat

## Zagon projekta

```bash
cd trgovina_projekt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Stran je nato na voljo na `http://127.0.0.1:8000/`, skrbniški vmesnik pa na `http://127.0.0.1:8000/admin/`.

**Pomembno:** preden lahko dodajaš oglase, moraš v adminu ustvariti vsaj eno Kategorijo (oglas mora imeti vsaj eno kategorijo).

## Funkcionalnosti

- pregled najnovejših oglasov
- iskanje oglasov (po naslovu in tipu Kupim/Prodajam)
- dodajanje in urejanje oglasa (samo prijavljeni uporabniki z ustreznimi pravicami)
- nakup oglasa / preklic nakupa
- registracija in prijava uporabnikov
