from .models import *

from datetime import date




def totalnoticount(request):
    lid = request.session.get('lid')
    tasks_due_soon = 0
    
    if lid is not None:
        try:
            today = date.today()
            tasks_due_soon = Task.objects.filter(duedate__lte=today,status='Pending',USER=Users.objects.get(LOGIN=request.session['lid'])).count
        except (Users.DoesNotExist, ValueError):
            pass  
        
    return {'noticount': tasks_due_soon}

