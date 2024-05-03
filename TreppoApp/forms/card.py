from django.forms import ModelForm

from ..models import Card


class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = ["title", "description", "category"]
        labels = {"title": "Card title", "description": "Card description", "category": "Card category"}


class CardFormNoCategory(ModelForm):
    class Meta:
        model = Card
        fields = ["title", "description"]
        labels = {"title": "Card title", "description": "Card description"}
