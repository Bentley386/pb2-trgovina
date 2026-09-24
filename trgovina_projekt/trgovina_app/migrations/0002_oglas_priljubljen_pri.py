from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trgovina_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='oglas',
            name='priljubljen_pri',
            field=models.ManyToManyField(blank=True, related_name='priljubljeni_oglasi', to=settings.AUTH_USER_MODEL, verbose_name='Uporabniki, ki jim je oglas všeč'),
        ),
    ]
