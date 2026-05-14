from django.db import models

class Izdelek(models.Model):
    
    class Meta:
        verbose_name_plural = 'Izdelki'

class Kategorija(models.Model):

    class Meta:
        verbose_name_plural = 'Kategorije'

class Transakcija(models.Model):

    class Meta:
        verbose_name_plural = 'Transakcije'
        
