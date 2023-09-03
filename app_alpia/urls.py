"""
URL configuration for app_alpia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gestionPatient import views
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', lambda request: redirect('login'), name='root'),
    # path('acceuil/', views.acceuil_list, name='acceuil-list'),
    # path('acceuil/<int:id>', views.acceuil_detail, name='acceuil-detail'),
    
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    path('acceuil/', views.home, name='acceuil_init'),
    path('acceuil/<str:name>', views.acceuil, name='acceuil'),
    
    path('patient/', views.patient, name='patient'),
    path('patient/add', views.add_patient, name='patient-add'),
    path('patient/<int:id>/update', views.update_patient, name='patient-update'),
    path('patient/<int:id>/delate', views.delate_patient, name='patient-delate'),
    
    path('patient/liste', views.list_patient, name='patient-liste'),
    path('patient/<int:id>/read', views.read_patient, name='read-patient'),
    path('patient/<int:id>/folder', views.patient_folder, name='patient-folder'),
    path('patient/<int:id>/fiche_medicale', views.fiche_medical, name='fiche-medical'),
    path('patient/<int:id_p>/<int:id_tr>/fiche_consultation', views.fiche_consultation, name='fiche-consultation'),
    path('patient/<int:id_p>/<int:id_hm>/fiche_antecedent', views.fiche_antecedent, name='fiche-antecedent'),
    
    path('administrate/', views.administrate, name='administrate'),
    path('administrate/add', views.add_administration, name='administrate-add'),
    path('administrate/<int:id>/update', views.update_administration, name='administrate-update'),
    path('administrate/<int:id>/delate', views.delate_administration, name='administrate-delate')
]
