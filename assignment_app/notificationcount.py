from .models import *

from datetime import date



def totalnoticount(request):
    lid = request.session.get('lid')
    tasks_due_soon = 0
    
    if lid is not None:
        try:
            today = date.today()
<<<<<<< HEAD
            robj = ReminderSetting.objects.filter(USER=request.user).first()
            if robj is None:
                tasks_due_soon = Task.objects.filter(duedate__lte=today, status='Pending', USER=request.user).count()
            elif robj.status == 'On':         
                tasks_due_soon = Task.objects.filter(duedate__lte=today, status='Pending', USER=request.user).count()
=======
            robj = ReminderSetting.objects.filter(USER=Users.objects.get(LOGIN=lid)).first()
            if robj is None:
                tasks_due_soon = Task.objects.filter(duedate__lte=today, status='Pending', USER=Users.objects.get(LOGIN=request.session['lid'])).count()
            elif robj.status == 'On':         
                tasks_due_soon = Task.objects.filter(duedate__lte=today, status='Pending', USER=Users.objects.get(LOGIN=request.session['lid'])).count()
>>>>>>> 695c1564f21dc5bb418c10a064dd0137c00b2de9

        except (Users.DoesNotExist, ValueError):
            pass  

    return {'noticount': tasks_due_soon}


