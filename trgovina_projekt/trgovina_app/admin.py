from django.contrib import admin
from .models import Oglas, Kategorija, Transakcija


@admin.register(Transakcija)
class TransakcijaAdmin(admin.ModelAdmin):
    # Transakcije nastanejo samodejno preko gumba "Kupi" na strani,
    # zato jih v adminu samo pregledujemo, ne dodajamo ročno.
    def has_add_permission(self, request):
        return False


admin.site.register(Oglas)
admin.site.register(Kategorija)
