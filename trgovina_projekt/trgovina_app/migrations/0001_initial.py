from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kategorija',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv', models.CharField(max_length=50, unique=True, verbose_name='Naziv kategorije')),
            ],
            options={
                'verbose_name_plural': 'Kategorije',
                'ordering': ['naziv'],
            },
        ),
        migrations.CreateModel(
            name='Oglas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naslov', models.CharField(help_text='Do 200 znakov', max_length=200, verbose_name='Naslov oglasa')),
                ('opis', models.CharField(blank=True, default='', help_text='Do 5000 znakov', max_length=5000, verbose_name='Opis oglasa')),
                ('datum_cas', models.DateTimeField(auto_now_add=True, verbose_name='Datum in čas objave oglasa')),
                ('cena', models.DecimalField(decimal_places=2, help_text='Cena izdelka (v EUR)', max_digits=10, verbose_name='Cena')),
                ('ogledi', models.IntegerField(default=0, verbose_name='Število ogledov oglasa')),
                ('tip', models.CharField(choices=[('K', 'Kupim'), ('P', 'Prodajam')], max_length=20, verbose_name='Tip oglasa')),
                ('aktiven', models.BooleanField(default=True, verbose_name='Ali je oglas še aktiven (ni prodan/kupljen)')),
                ('kategorije', models.ManyToManyField(to='trgovina_app.kategorija', verbose_name='Kategorije, v katere spada oglas')),
                ('lastnik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oglasi', to=settings.AUTH_USER_MODEL, verbose_name='Lastnik oglasa')),
            ],
            options={
                'verbose_name_plural': 'Oglasi',
                'ordering': ['-datum_cas'],
            },
        ),
        migrations.CreateModel(
            name='Transakcija',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cena', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Dogovorjena cena')),
                ('datum_cas', models.DateTimeField(auto_now_add=True, verbose_name='Datum in čas transakcije')),
                ('kupec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nakupi', to=settings.AUTH_USER_MODEL, verbose_name='Kupec')),
                ('oglas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transakcije', to='trgovina_app.oglas', verbose_name='Oglas')),
            ],
            options={
                'verbose_name_plural': 'Transakcije',
                'ordering': ['-datum_cas'],
            },
        ),
        migrations.AddConstraint(
            model_name='transakcija',
            constraint=models.UniqueConstraint(fields=('oglas',), name='enolicnost_transakcije_oglasa'),
        ),
    ]
