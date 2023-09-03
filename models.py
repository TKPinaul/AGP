from django.db import models
from django.utils import timezone
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=50, default="root123")
    title = models.CharField(max_length=100, default="Administrateur")
    tel_number = PhoneNumberField(default="00000000")
    email = models.EmailField(max_length=100, default="compte@gmail.com")
    connection_count = models.IntegerField(default=0)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.surname
    
    
class Patient(models.Model):
    
    class Sex(models.TextChoices):
        Masculine = 'M'
        Feminine = 'F'
        
    class Marital_status(models.TextChoices):
        Celibate = 'Celibat'
        Marry = 'Couple'
        Widow = 'Veuve/Veuf'
        
    id_patient = models.AutoField(primary_key=True)
    surname_p = models.CharField(max_length=100)
    first_name_p = models.CharField(max_length=200)
    age_p = models.IntegerField()
    sex_p = models.fields.CharField(choices=Sex.choices, max_length=9)
    marital_status = models.fields.CharField(choices=Marital_status.choices, max_length=10)
    profession = models.CharField(max_length=200)
    numero_p = models.IntegerField(default="00000000")
    email_p = models.CharField(max_length=150, default="compte@gmail.com")
    residence =  models.CharField(max_length=200)
    ethnic = models.CharField(max_length=150)
    religion = models.CharField(max_length=100)
    
    
class MedicalHistory(models.Model):
    id_MH = models.AutoField(primary_key=True)
    medical = models.TextField()
    surgical = models.TextField()
    obstetrical = models.TextField()
    eating_habits = models.TextField(null=True)
    allergies = models.TextField(blank=True, null=True)
    id_patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_history')


class FamilyHistory(models.Model):
    id_FH = models.AutoField(primary_key=True)
    family_history = models.TextField()
    id_patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='family_history')


class CurrentTreatment(models.Model):
    id_traitement = models.AutoField(primary_key=True)
    date_consultation = models.DateField(default=date.today)
    actu_complaints = models.TextField(null=True)
    analyse_medical = models.TextField(null=True)
    current_treatment = models.TextField()
    date_appointment = models.DateField(default=date.today, null=True)
    diagnostics = models.TextField(null=True)
    id_patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='current_treatment', db_column='id_patient')
    id_user_id = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
