# forms.py
from django import forms
from .models import State, City

class ServiceForm(forms.Form):
    state = forms.ModelChoiceField(queryset=State.objects.all(), required=True)
    city = forms.ModelChoiceField(queryset=City.objects.none(), required=True)

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('name')
