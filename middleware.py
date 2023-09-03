from django.shortcuts import redirect
from django.urls import reverse

class LoginAndAdminRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        user = request.session.get('utilisateur')
        role = request.session.get('fonction')
        
        if not user and request.path != reverse('login'):
            return redirect('login')
        
        if role != 'Administrator' and request.path == reverse('administrate'):
            return redirect('login')
        
        response = self.get_response(request)
        return response
