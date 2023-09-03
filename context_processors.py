from gestionPatient.models import User


def user_context(request):
    v_user = None
    role = None
    
    # recuperate le nom utilisateur
    if 'utilisateur' in request.session:
        v_user = request.session['utilisateur'] 
    
    # recuperate le titre de l'utilisateur 
    if 'fonction' in request.session:
        role = request.session['fonction']
    
    # recuperate l'id utilisateur
    user_id = request.session.get('user_id')
    user = None
    if user_id:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass
    
    return {
        'v_user': v_user, 
        'role': role, 
        'user': user,
        }