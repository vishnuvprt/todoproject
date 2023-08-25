from .models import *


def pandn(request):
    lid = request.session.get('lid')
    name = ""  
    photo = ""  
    if lid is not None:
        try:
            
            name = Users.objects.get(LOGIN=lid).name
            photo = Users.objects.get(LOGIN=lid).photo

        except (Users.DoesNotExist, ValueError):
            pass
        
    return {'name': name, 'photo': photo}




def sonoff(request):
    lid = request.session.get('lid')
    sts = ""

    if lid is not None:
        try:
            user = Users.objects.get(LOGIN=lid)
            rem=ReminderSetting.objects.filter(USER=user)
            if rem is not None:
                reminder_setting = ReminderSetting.objects.get(USER=user)
            else:
                sts = reminder_setting.status
        except (Users.DoesNotExist, ReminderSetting.DoesNotExist, ValueError):
            pass

    return {'sts': sts}