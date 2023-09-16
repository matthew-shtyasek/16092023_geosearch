from django import forms


class CoordinatesForm(forms.Form):
    longitude = forms.DecimalField(max_value=180,
                                   min_value=-180,
                                   max_digits=9,
                                   decimal_places=6)
    latitude = forms.DecimalField(max_value=90,
                                  min_value=-90,
                                  max_digits=8,
                                  decimal_places=6)
