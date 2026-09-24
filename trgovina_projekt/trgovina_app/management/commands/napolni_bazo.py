import random
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from trgovina_app.models import Kategorija, Oglas, Transakcija

KATEGORIJE = [
    "Oblačila", "Obutev", "Elektronika", "Šport in rekreacija",
    "Pohištvo", "Knjige", "Igrače", "Glasbeni inštrumenti",
    "Vrt in orodje", "Avtomobilski deli", "Lepota in nega", "Otroška oprema",
]

ARTIKLI = [
    "Gorsko kolo", "Cestno kolo", "Zimska jakna", "Poletni sandali",
    "Prenosnik", "Pametni telefon", "Slušalke brezžične", "Tablica",
    "Trosed", "Jedilna miza", "Pisarniški stol", "Omara",
    "Roman - Zgodovinski", "Strokovna knjiga", "Otroška slikanica",
    "Lego kocke", "Namizna igra", "Plišasta igrača",
    "Kitara akustična", "Klaviatura", "Boben",
    "Kosilnica", "Vrtne škarje", "Lestev",
    "Avtomobilske gume", "Strešni nosilec", "Avtosedež za otroka",
    "Fen za lase", "Parfum", "Kozmetični set",
    "Voziček za dojenčka", "Otroška posteljica", "Otroška oblačila set",
]

PRIDEVNIKI = ["skoraj nov", "rabljen", "kot nov", "malo rabljen", "top stanje", "za rezervne dele"]


class Command(BaseCommand):
    help = "Napolni bazo z demo kategorijami, uporabniki in oglasi za testiranje."

    def add_arguments(self, parser):
        parser.add_argument(
            "--stevilo", type=int, default=40,
            help="Koliko oglasov naj se ustvari (privzeto 40)."
        )

    @transaction.atomic
    def handle(self, *args, **options):
        stevilo = options["stevilo"]

        self.stdout.write("Brisanje obstoječih oglasov in kategorij...")
        Oglas.objects.all().delete()
        Kategorija.objects.all().delete()

        self.stdout.write("Ustvarjanje kategorij...")
        kategorije = [Kategorija.objects.create(naziv=naziv) for naziv in KATEGORIJE]

        self.stdout.write("Ustvarjanje demo uporabnikov (geslo: geslo1234)...")
        uporabniki = []
        for ime in ["ana", "bor", "cene", "dora"]:
            uporabnik, ustvarjen = User.objects.get_or_create(username=ime)
            if ustvarjen:
                uporabnik.set_password("geslo1234")
                uporabnik.save()
            uporabniki.append(uporabnik)

        self.stdout.write(f"Ustvarjanje {stevilo} oglasov...")
        oglasi = []
        for _ in range(stevilo):
            artikel = random.choice(ARTIKLI)
            pridevnik = random.choice(PRIDEVNIKI)
            tip = random.choice(["K", "P"])
            oglas = Oglas.objects.create(
                naslov=f"{artikel} ({pridevnik})",
                opis=f"Prodajam/kupujem: {artikel}, stanje: {pridevnik}. Možen dogovor za ceno.",
                lastnik=random.choice(uporabniki),
                cena=Decimal(random.randrange(500, 50000)) / 100,
                tip=tip,
            )
            oglas.kategorije.set(random.sample(kategorije, k=random.randint(1, 2)))
            oglasi.append(oglas)

        # Nekaj oglasov označimo kot že prodane, da lahko preizkusiš tudi to stanje.
        prodani = random.sample(oglasi, k=max(1, stevilo // 8))
        for oglas in prodani:
            kupci = [u for u in uporabniki if u != oglas.lastnik]
            Transakcija.objects.create(oglas=oglas, kupec=random.choice(kupci), cena=oglas.cena)
            oglas.aktiven = False
            oglas.save()

        self.stdout.write(self.style.SUCCESS(
            f"Gotovo: {len(kategorije)} kategorij, {len(uporabniki)} demo uporabnikov, {stevilo} oglasov "
            f"({len(prodani)} označenih kot prodanih)."
        ))
