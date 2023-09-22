from .models import *


def pandn(request):
    lid = request.session.get('lid')
    name = ""  
    photo = ""  
    if lid is not None:
        try:
            
<<<<<<< HEAD
            name = Users.objects.get(pk=lid).name
            photo = Users.objects.get(pk=lid).photo
=======
            name = Users.objects.get(LOGIN=lid).name
            photo = Users.objects.get(LOGIN=lid).photo
>>>>>>> 695c1564f21dc5bb418c10a064dd0137c00b2de9

        except (Users.DoesNotExist, ValueError):
            pass
        
    return {'name': name, 'photo': photo}




def sonoff(request):
    lid = request.session.get('lid')
    sts = ""

    if lid is not None:
        try:
<<<<<<< HEAD
            user = Users.objects.get(pk=lid)
=======
            user = Users.objects.get(LOGIN=lid)
>>>>>>> 695c1564f21dc5bb418c10a064dd0137c00b2de9
            rem=ReminderSetting.objects.filter(USER=user)
            if rem is not None:
                reminder_setting = ReminderSetting.objects.get(USER=user)
            else:
                sts = reminder_setting.status
        except (Users.DoesNotExist, ReminderSetting.DoesNotExist, ValueError):
            pass

    return {'sts': sts}