from django.db import models
from django.contrib.auth.models import User


class Kategorija(models.Model):
    naziv = models.CharField(max_length=50, unique=True, verbose_name="Naziv kategorije")

    def __str__(self):
        return self.naziv

    class Meta:
        ordering = ["naziv"]
        verbose_name_plural = "Kategorije"


class Oglas(models.Model):

    TIPI_OGLASOV = {
        "K" : "Kupim",
        "P" : "Prodajam"
    }

    naslov = models.CharField(max_length=200, verbose_name="Naslov oglasa", help_text="Do 200 znakov")
    opis = models.CharField(max_length=5000, blank=True, default="", verbose_name="Opis oglasa", help_text="Do 5000 znakov")
    lastnik = models.ForeignKey(User, on_delete=models.CASCADE, related_name="oglasi", verbose_name="Lastnik oglasa")
    datum_cas = models.DateTimeField(auto_now_add=True, verbose_name="Datum in čas objave oglasa")
    cena = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena", help_text="Cena izdelka (v EUR)")
    ogledi = models.IntegerField(default=0, verbose_name="Število ogledov oglasa")
    tip = models.CharField(max_length=20, choices=TIPI_OGLASOV.items(), verbose_name="Tip oglasa")
    aktiven = models.BooleanField(default=True, verbose_name="Ali je oglas še aktiven (ni prodan/kupljen)")
    kategorije = models.ManyToManyField(Kategorija, verbose_name="Kategorije, v katere spada oglas")

    def __str__(self):
        return f"{self.get_tip_display()}: {self.naslov}"

    class Meta:
        ordering = ["-datum_cas"]
        verbose_name_plural = "Oglasi"


class Transakcija(models.Model):
    oglas = models.ForeignKey(Oglas, on_delete=models.CASCADE, related_name="transakcije", verbose_name="Oglas")
    kupec = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nakupi", verbose_name="Kupec")
    cena = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Dogovorjena cena")
    datum_cas = models.DateTimeField(auto_now_add=True, verbose_name="Datum in čas transakcije")

    def __str__(self):
        return f"Transakcija: {self.oglas.naslov} ({self.kupec})"

    class Meta:
        ordering = ["-datum_cas"]
        constraints = [
            models.UniqueConstraint(
                fields=["oglas"],
                name="enolicnost_transakcije_oglasa"
            )
        ]
        verbose_name_plural = "Transakcije"

