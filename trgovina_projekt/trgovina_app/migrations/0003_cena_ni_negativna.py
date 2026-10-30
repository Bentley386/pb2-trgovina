import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trgovina_app", "0002_oglas_priljubljen_pri"),
    ]

    operations = [
        migrations.AlterField(
            model_name="oglas",
            name="cena",
            field=models.DecimalField(
                decimal_places=2,
                help_text="Cena izdelka v EUR (ne more biti negativna)",
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Cena",
            ),
        ),
        migrations.AlterField(
            model_name="transakcija",
            name="cena",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Dogovorjena cena",
            ),
        ),
        migrations.AddConstraint(
            model_name="oglas",
            constraint=models.CheckConstraint(
                check=models.Q(("cena__gte", 0)),
                name="cena_oglasa_ni_negativna",
            ),
        ),
        migrations.AddConstraint(
            model_name="transakcija",
            constraint=models.CheckConstraint(
                check=models.Q(("cena__gte", 0)),
                name="cena_transakcije_ni_negativna",
            ),
        ),
    ]
