from .models import *

from datetime import date



def totalnoticount(request):
    lid = request.session.get('lid')
    tasks_due_soon = 0
    
    if lid is not None:
        try:
            today = date.today()

            robj = ReminderSetting.objects.filter(USER=request.user).first()
            if robj is None:
                tasks_due_soon = Task.objects.filter(duedate__lte=today, status='Pending', USER=request.user).count()
            elif robj.status == 'On':         
                tasks_due_soon = Task.objects.filter(duedate__lte=today, status='Pending', USER=request.user).count()

            robj = ReminderSetting.objects.filter(USER=request.user).first()
            if robj is None:
                tasks_due_soon = Task.objects.filter(duedate__lte=today, status='Pending', USER=request.user).count()
            elif robj.status == 'On':         
                tasks_due_soon = Task.objects.filter(duedate__lte=today, status='Pending', USER=request.user).count()


        except (Users.DoesNotExist, ValueError):
            pass  

    return {'noticount': tasks_due_soon}


