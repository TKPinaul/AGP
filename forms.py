from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from .models import User, Patient, CurrentTreatment

class PatientForm(forms.Form):

    date_consul = forms.DateField(label='Date de consultation', required=True, widget=forms.DateInput(attrs={'type': 'date', 'id':'dateConsul'}))

    plainte = forms.CharField(label='Symptômes actuels', widget=forms.Textarea(attrs={'rows': 10, 'cols': 20, 'placeholder':'Saisissez les motif de consultation ici...'}), required=True)

    analyse = forms.CharField(label='Analyse médicale', widget=forms.Textarea(attrs={'rows': 10, 'cols': 20, 'placeholder':'Saisissez les type d\'analyse à faire...'}), required=True)

    current_treatment = forms.CharField(label='Traitement actuel', widget=forms.Textarea(attrs={'rows': 10, 'cols': 20, 'placeholder':'Présenter un bref résumé du traitement en cour ici...'}), required=False)

    date_appoint = forms.DateField(label='Prendre rendez-vous', required=False, widget=forms.DateInput(attrs={'type': 'date', 'id':'dateAppoint'}))

    # show_diagnostics = forms.BooleanField(label='Faire un diagnostic', widget=forms.CheckboxInput(attrs={'id': 'id_show_diagnostics'}), required=False)
    
    # diagnostics = forms.CharField(label='Diagnostique médicale', widget=forms.Textarea(attrs={'rows': 6, 'cols': 20, 'id': 'id_diagnostics'}), required=False)
    
    doctor_charge = forms.ModelChoiceField(label='Docteur en charge du patient', queryset=User.objects.filter(title="Doctor"), empty_label="Sélectionnez un médecin", required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor_charge'].queryset = User.objects.filter(title="Doctor")
        self.fields['doctor_charge'].empty_label = "Sélectionnez un médecin"

        # self.fields['diagnostics'].widget = forms.HiddenInput()
        # if self.data.get('show_diagnostics', False) == 'on':
        #     self.fields['diagnostics'].widget = forms.Textarea(attrs={'rows': 6, 'cols': 20})
        
        # if not self.initial.get('show_diagnostics', False):
        #     self.fields['diagnostics'].widget = forms.HiddenInput()
        # if self.is_bound:
        #     show_diagnostics = self.cleaned_data.get('show_diagnostics', False)
        #     if not show_diagnostics:
        #         self.fields['diagnostics'].widget = forms.HiddenInput()