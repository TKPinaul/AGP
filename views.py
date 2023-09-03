
import json
from django.shortcuts import get_object_or_404

from datetime import datetime
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse, JsonResponse

from gestionPatient.models import User, Patient, MedicalHistory, FamilyHistory, CurrentTreatment
from .forms import PatientForm
# from .decorators import admin_required


def login(request):
    if 'show_password' in request.POST:
        request.session['show_password'] = True
    else:
        request.session['show_password'] = False
    
    if request.method == 'POST':
        v_user = request.POST.get('utilisateur')
        v_password = request.POST.get('mot_pass')
        
        users = User.objects.filter(surname=v_user, password=v_password)
        if users.exists():
            user = users.first()
            role = user.title
            request.session['user_id'] = user.pk
            request.session['fonction'] = role
            request.session['utilisateur'] = v_user
            
            today = timezone.now().date()
            if user.last_login_time != today:
                user.last_login_time = today
                user.last_login_time = timezone.now()
                user.connection_count = 1
            else:
                user.connection_count += 1
            user.save()
                
            request.session['premiere_connexion'] = True
            
            return redirect(reverse('acceuil', kwargs={'name': v_user}))
        else:
            error_message = "user name or password is not valid"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')


def user_logout(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        print(user_id)
        if user_id:
            user = User.objects.get(pk=user_id)
            user.last_logout_time = timezone.now()
            user.save()
        logout(request)
        return redirect('login')
    return redirect('acceuil')


def home(request):
    users = User.objects.all()
    return render(request, 'acceuil.html')


def acceuil(request, name):
    users=User.objects.all()
    premiere_connexion = request.session.pop('premiere_connexion', False)
    return render(request, 'acceuil.html', {"name":name, "users":users, "premiere_connexion": premiere_connexion})


# -----------------------Patient-----------------------

# Création de dossier medical et ajout d'un nouveau patient
def add_patient(request):
    users = User.objects.filter(title="Doctor")

    if request.method == 'POST':
        nom_p = request.POST['nom_p']
        prenom_p = request.POST['prenom_p']
        age_p = int(request.POST['age'])
        
        if prenom_p:
            existing_patients = Patient.objects.filter(surname_p=nom_p, first_name_p=prenom_p)
        else:
            existing_patients = Patient.objects.filter(surname_p=nom_p)
        
        if existing_patients.exists():
            messages.error(request, "Une personne est déjà enregistrer en ce nom.")
            return render(request, 'fonction_crud/add_dossierMedical.html', {"existing_patients":existing_patients, "users":users})
        else:
            if age_p <= 0:
                messages.error(request, "L'âge doit être supérieur à zéro.")
                return render(request, 'fonction_crud/add_dossierMedical.html', {"users":users})
            user_instance = User.objects.get(pk=request.POST['doctor_charge'])
            
            with transaction.atomic():
                patients = Patient.objects.create(
                    surname_p = request.POST['nom_p'],
                    first_name_p = request.POST['prenom_p'],
                    age_p = request.POST['age'],
                    sex_p = request.POST['sex_p'],
                    marital_status = request.POST['marital_status'],
                    profession = request.POST['profession'],
                    numero_p = request.POST['num_tel'],
                    email_p = request.POST['mail'],
                    residence =  request.POST['residence'],
                    ethnic = request.POST['ethnie'],
                    religion = request.POST['religion']
                )
                
                medicalhistorys = MedicalHistory.objects.create(
                    medical = request.POST['medical_history'],
                    surgical = request.POST['surgical_history'],
                    obstetrical = request.POST['obstetrical_history'],
                    eating_habits = request.POST['hab_aliment'],
                    allergies = request.POST['allergie'],
                    id_patient =patients
                )
                
                familyhistorys = FamilyHistory.objects.create(
                    family_history = request.POST['family_history'],
                    id_patient=patients
                )
                
                currentTreatments = CurrentTreatment.objects.create(
                    date_consultation = request.POST['date_consul'],
                    actu_complaints = request.POST['plainte'],
                    analyse_medical = request.POST['analyse'],
                    current_treatment = request.POST['current_treatment'],
                    date_appointment = request.POST['date_appoint'],
                    id_patient = patients,
                    id_user_id = user_instance
                )
            patients.save()
            medicalhistorys.save()
            familyhistorys.save()
            currentTreatments.save()
            
            return redirect('patient-liste')
    return render(request, 'fonction_crud/add_dossierMedical.html', {"users":users})

# Modifier les donées personnel du patient
def update_patient(request, id):
    patients = Patient.objects.get(id_patient=id)
    
    if request.method == 'POST':
        patients.surname_p = request.POST['nom_p']
        patients.first_name_p = request.POST['prenom_p']
        patients.age_p = request.POST['age']
        patients.sex_p = request.POST['sex_p']
        patients.marital_status = request.POST['marital_status']
        patients.profession = request.POST['profession']
        patients.numero_p = request.POST['num_tel']
        patients.email_p = request.POST['mail']
        patients.residence =  request.POST['residence']
        patients.ethnic = request.POST['ethnie']
        patients.religion = request.POST['religion']
        patients.save()
        return redirect('patient-liste')
    
    return render(request, 'fonction_crud/update_patient.html', {"patients":patients})


def delate_patient(request):
    patients = Patient.objects.all()
    return render(request, 'fonction_crud/delate_patient.html')

# Afficher fiche d'un patient
def read_patient(request, id):
    patients = Patient.objects.get(id_patient=id)
    return render(request, 'fonction_crud/read_patient.html', {"patient":patients})

# Gestion des dossiers médical (liste des dossiers)
def patient(request):
    patients_list = Patient.objects.all()
    paginator = Paginator(patients_list, 8)
    page_number = request.GET.get('page')
    patients = paginator.get_page(page_number)
    return render(request, 'patientManagement.html', {"patients":patients})

# Gestion des patients
def list_patient(request):
    patients_list = Patient.objects.order_by('surname_p')
    paginator = Paginator(patients_list, 8)
    page_number = request.GET.get('page')
    patients = paginator.get_page(page_number)
    return render(request, 'listePatient.html', {"patients":patients})

# dossierMedicale
def patient_folder(request, id):
    users = User.objects.filter(title="Doctor")
    patients = Patient.objects.get(id_patient=id)
    
    medical_history = None
    family_history = None
    current_treatment = None
    
    try:
        medical_history = MedicalHistory.objects.get(id_patient=id)
        family_history = FamilyHistory.objects.get(id_patient=id)
        current_treatment = CurrentTreatment.objects.get(id_patient=id)
    except (MedicalHistory.DoesNotExist,
            FamilyHistory.DoesNotExist,
            CurrentTreatment.DoesNotExist):
        pass
    
    fiche_medical_list = CurrentTreatment.objects.filter(id_patient=patients).order_by('date_consultation')
    paginator = Paginator(fiche_medical_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'pat': patients,
        'med_story': medical_history,
        'fam_story': family_history,
        'cur_treatment': current_treatment,
        'page_obj': page_obj,
        'users': users
    }
    return render(request, 'dossierMedicale.html', context)

def fiche_medical(request, id): 
    users = User.objects.filter(title="Doctor")
    patients = Patient.objects.get(id_patient=id)
    form = PatientForm(initial={'show_diagnostics': False})
    
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            date_c = form.cleaned_data['date_consul']
            actu_c = form.cleaned_data['plainte']
            analyse_m = form.cleaned_data['analyse']
            current_t = form.cleaned_data['current_treatment']
            date_ap = form.cleaned_data['date_appoint']
            user_instance = User.objects.get(pk=request.POST['doctor_charge'])
            
            CurrentT = CurrentTreatment.objects.create(
                date_consultation=date_c,
                actu_complaints=actu_c,
                analyse_medical=analyse_m,
                current_treatment=current_t,
                date_appointment=date_ap,
                id_patient = patients,
                id_user_id = user_instance
            )
            CurrentT.save()
            return redirect('patient-folder', id=id)
        else:
            return redirect('fiche-medical', id=id)
    else:
        form = PatientForm()
        
    return render(request, 'ficheMedicale.html', {'form': form, "users":users, 'id': id })
    # print("Debug - Users:", users)
    # print("Debug - Form:", form)


def fiche_consultation(request, id_p, id_tr):
    users = User.objects.all()
    patients = Patient.objects.get(id_patient=id_p)
    currentTreatments = CurrentTreatment.objects.get(id_patient=id_p, id_traitement=id_tr)
    
    context = {
        'users': users,
        'patients': patients,
        'currentTreatments': currentTreatments,
    }
    return render(request, 'fonction_crud/ficheConsultation.html', context)


def fiche_antecedent(request, id_p, id_hm):
    patients = get_object_or_404(Patient, id_patient=id_p)
    medicalHistorys = get_object_or_404(MedicalHistory, id_patient=id_p, id_MH=id_hm)
    
    context = {
        'patients': patients,
        'medicalHistorys': medicalHistorys,
    }
    return render(request, 'fonction_crud/ficheAntecedent.html', context)

# -----------------------Administrateur-----------------------

# administration
# @admin_required
def administrate(request):
    users = User.objects.all()
    
    for user in users:
        last_login = user.last_login_time
        last_logout = user.last_logout_time
        
        if last_login and last_logout:
            time_spent = abs(last_logout - last_login)
            total_seconds = time_spent.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)
            user.time_spent = f"{hours:02}:{minutes:02}:{seconds:02}"
            
    return render(request, 'administration.html', {"users":users})

def add_administration(request):
    users = User.objects.all()
    if request.method == 'POST':
        users = User.objects.create(
            surname = request.POST['nom'],
            first_name = request.POST['prenom'],
            title = request.POST['titre'],
            tel_number = request.POST['numero'],
            email = request.POST['mail'],
            password = request.POST['mot_passe']
            )        
        users.save()
        return redirect('administrate')
    return render(request, 'fonction_crud/add_administration.html', {"users":users})

def update_administration(request, id):
    users = User.objects.get(id_user=id)    
    if request.method == 'POST':
        users.surname = request.POST['nom']
        users.first_name = request.POST['prenom']
        users.title = request.POST['titre']
        users.tel_number = request.POST['numero']
        users.email = request.POST['mail']
        users.password = request.POST['mot_passe']
        users.save()
        return redirect('administrate')
    return render(request, 'fonction_crud/update_administration.html', {"users":users})

def delate_administration(request, id):
    users = User.objects.get(id_user=id)
    if request.method == 'POST':
        users.delete()
        return redirect('administrate')
    return render(request, 'fonction_crud/delate_administration.html', {"users":users})






