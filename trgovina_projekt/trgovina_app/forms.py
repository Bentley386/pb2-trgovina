from django.forms import ModelForm, TextInput, NumberInput, Select, Textarea
from .models import Oglas


class BulmaFormMixin:
    template_name = "forms/form_snippet.html"

    def __init__(self, /, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (TextInput, NumberInput)):
                field.widget.attrs.update({'class': 'input'})
            elif isinstance(field.widget, Textarea):
                field.widget.attrs.update({'class': 'textarea'})
            elif isinstance(field.widget, Select):
                field.widget.template_name = "forms/select_snippet.html"


class OglasForm(BulmaFormMixin, ModelForm):
    """Obrazec za dodajanje novega oglasa - oglas je ob objavi vedno aktiven."""
    class Meta:
        model = Oglas
        exclude = ['lastnik', 'ogledi', 'aktiven']
        widgets = {
            "opis": Textarea()
        }


class OglasUrediForm(OglasForm):
    """Obrazec za urejanje - lastnik lahko tu oglas tudi ročno označi kot prodan."""
    class Meta(OglasForm.Meta):
        exclude = ['lastnik', 'ogledi']
        labels = {
            "aktiven": "Oglas je še aktiven (odkljukaj, če je bil oglas prodan/kupljen)",
        }
