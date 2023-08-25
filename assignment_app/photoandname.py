from .models import *

def pandn(request):
    lid = request.session.get('lid')
    
    
    if lid is not None:
        try:
            name = Users.objects.get(LOGIN=lid).name
            photo = Users.objects.get(LOGIN=lid).photo
            

        except (Users.DoesNotExist, ValueError):
            pass  
        
    return {'name': name,'photo':photo}

