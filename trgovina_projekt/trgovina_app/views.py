from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction
from django.http import HttpResponseNotAllowed
from django.db.models import F, Q
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from .models import Oglas, Kategorija, Transakcija
from .forms import OglasForm


def index(request):
    return render(request, 'trgovina_app/index.html', {})


def oglas_podrobnosti(request, oglas_id):
    oglas = get_object_or_404(Oglas, id=oglas_id)
    Oglas.objects.filter(id=oglas_id).update(ogledi=F('ogledi') + 1)
    oglas.refresh_from_db()
    kontekst = {'oglas': oglas}
    return render(request, 'trgovina_app/oglas_podrobnosti.html', kontekst)


def oglas_najnovejsi(request, stevilo):
    najnovejsi = Oglas.objects.filter(aktiven=True).order_by('-datum_cas')[:stevilo]
    kontekst = {'seznam': najnovejsi, 'stevilo': stevilo}
    return render(request, 'trgovina_app/oglas_najnovejsi.html', kontekst)


def oglas_poisci(request):
    poizvedba = request.GET.get('zacetek', '')
    tip = request.GET.get('tip', '')
    rezultat = []
    if poizvedba or tip:
        rezultat = Oglas.objects.filter(aktiven=True)
        if poizvedba:
            rezultat = rezultat.filter(naslov__icontains=poizvedba)
        if tip:
            rezultat = rezultat.filter(tip=tip)
        rezultat = rezultat[:100]
    kontekst = {
        'poizvedba': poizvedba,
        'tip': tip,
        'tipi': Oglas.TIPI_OGLASOV,
        'rezultat': rezultat,
    }
    return render(request, 'trgovina_app/oglas_poisci.html', kontekst)


@login_required
@transaction.atomic
def oglas_kupi(request):
    if request.method == 'POST':
        oglas_id = request.POST.get('oglas_id', -1)
        oglas = get_object_or_404(Oglas, id=oglas_id)
        user = request.user

        if oglas.lastnik == user:
            messages.error(request, "Svojega oglasa ne moreš kupiti.")
            return redirect('trgovina_app:oglas_podrobnosti', oglas_id)

        obstojeca = Transakcija.objects.filter(oglas=oglas).first()
        if obstojeca:
            if obstojeca.kupec == user:
                obstojeca.delete()
                oglas.aktiven = True
                oglas.save()
                messages.success(request, "Nakup je bil preklican.")
            else:
                messages.error(request, "Oglas je žal že prodan.")
        else:
            Transakcija.objects.create(oglas=oglas, kupec=user, cena=oglas.cena)
            oglas.aktiven = False
            oglas.save()
            messages.success(request, "Nakup je bil uspešno zabeležen!")

        return redirect('trgovina_app:oglas_podrobnosti', oglas_id)
    return HttpResponseNotAllowed(['POST'])


@permission_required('trgovina_app.add_oglas')
@transaction.atomic
def oglas_dodaj(request):
    if request.method == "POST":
        form = OglasForm(request.POST)
        if form.is_valid():
            oglas = form.save(commit=False)
            oglas.lastnik = request.user
            oglas.save()
            form.save_m2m()
            messages.success(request, "Oglas je bil uspešno dodan!")
            return redirect('trgovina_app:oglas_podrobnosti', oglas_id=oglas.pk)
    else:
        form = OglasForm()
    kontekst = {'form': form}
    return render(request, 'trgovina_app/oglas_dodaj.html', kontekst)


@permission_required('trgovina_app.change_oglas')
@transaction.atomic
def oglas_uredi(request, oglas_id):
    oglas = get_object_or_404(Oglas, id=oglas_id)
    if request.method == "POST":
        form = OglasForm(request.POST, instance=oglas)
        if form.is_valid():
            form.save()
            messages.success(request, "Oglas je bil uspešno posodobljen!")
            return redirect('trgovina_app:oglas_podrobnosti', oglas_id=form.instance.pk)
    else:
        form = OglasForm(instance=oglas)
    kontekst = {'form': form}
    return render(request, 'trgovina_app/oglas_uredi.html', kontekst)


@transaction.atomic
def registracija(request):
    if request.user.is_authenticated:
        return redirect('trgovina_app:index')
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form.instance)
            messages.success(request, f"Uporabnik {form.instance.username} uspešno registriran!")
            return redirect('trgovina_app:index')
    else:
        form = UserCreationForm()
    kontekst = {'form': form}
    return render(request, 'registration/registration.html', kontekst)
