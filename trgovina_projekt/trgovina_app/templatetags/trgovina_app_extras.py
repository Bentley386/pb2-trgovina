from django import template

register = template.Library()

@register.filter
def je_kupil(uporabnik, oglas):
    if not uporabnik.is_authenticated:
        return False
    return oglas.transakcije.filter(kupec=uporabnik).exists()
