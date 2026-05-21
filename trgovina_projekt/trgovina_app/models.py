from django.db import models
from django.contrib.auth.models import User

class Oglas(models.Model):

    TIPI_OGLASOV = {
        "K" : "Kupim",
        "P" : "Prodajam"
    }

    naslov = models.CharField(max_length=200, verbose_name="Naslov oglasa", help_text="Do 200 znakov")
    opis = models.CharField(max_length=5000, blank=True, default="", verbose_name="Naslov oglasa", help_text="Do 5000 znakov")
    lastnik = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Lastnik oglasa")
    datum_cas = models.DateTimeField(auto_now_add=True, verbose_name="Datum in čas objave oglasa")
    cena = models.DecimalField(decimal_places=2, verbose_name="Cena", help_text="Cena izdelka (v EUR)")
    ogledi = models.IntegerField(default=0, verbose_name="Število ogledov oglasa")
    Tip = models.CharField(max_length=20, choices=TIPI_OGLASOV.items())
    kategorije = models.ManyToManyField("Kategorija", verbose_name="Kategorije, v katere spada oglas")
    
    class Meta:
        verbose_name_plural = "Oglasi"

class Kategorija(models.Model):

    class Meta:
        verbose_name_plural = "Kategorije"

class Transakcija(models.Model):

    class Meta:
        verbose_name_plural = "Transakcije"
        
