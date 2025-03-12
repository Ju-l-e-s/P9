# reviews/forms.py

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Ticket, Review

class TicketForm(forms.ModelForm):
    """
    A form for creating and updating Ticket instances.

    :param model: The model associated with this form.
    :type model: Ticket
    :param fields: The fields to be included in the form.
    :type fields: list of str
    """
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        # We don't include 'user' or 'time_created' because they will be managed automatically


class ReviewForm(forms.ModelForm):
    """
    A form for creating and updating Review instances.

    :param RATING_CHOICES: A list of tuples representing rating choices.
    :type RATING_CHOICES: list of tuple
    :param rating: A choice field for selecting a rating, displayed as radio buttons.
    :type rating: forms.ChoiceField

    :param Meta.model: The model associated with this form.
    :type Meta.model: Review
    :param Meta.fields: The fields to include in the form.
    :type Meta.fields: list of str
    """
    RATING_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']