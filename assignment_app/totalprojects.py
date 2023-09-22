from .models import *

def total_projects(request):
    totalp = Project.objects.count()
    return {'totalp': totalp}



def finished_projects(request):
    finishedp=Project.objects.filter(status='Completed').count()
    return {'finishedp':finishedp}



def ongoing_projects(request):
    ongoingp=Project.objects.filter(status='Ongoing').count()
    return {'ongoingp':ongoingp}





def total_projects_user(request):
    lid = request.session.get('lid')
    totalp = 0
    
    if lid is not None:
        try:
<<<<<<< HEAD
            uid = Users.objects.get(pk=lid)
=======
            uid = Users.objects.get(LOGIN_id=lid)
>>>>>>> 695c1564f21dc5bb418c10a064dd0137c00b2de9
            totalp = ProjectTeams.objects.filter(USER=uid).count()
        except (Users.DoesNotExist, ValueError):
            pass  
        
    return {'totalpu': totalp}


def finished_tasks(request):
    lid = request.session.get('lid')  
    totalp = 0  
    
    if lid is not None:
        try:
<<<<<<< HEAD
            uid = Users.objects.get(pk=lid)
=======
            uid = Users.objects.get(LOGIN_id=lid)
>>>>>>> 695c1564f21dc5bb418c10a064dd0137c00b2de9
            totalp = Task.objects.filter(USER=uid, status='Completed').count()
        except (Users.DoesNotExist, ValueError):
            pass  
        
    return {'totalfp': totalp}


def Ongoing_tasks(request):
    lid = request.session.get('lid')  
    totalp = 0  
    
    if lid is not None:
        try:
<<<<<<< HEAD
            uid = Users.objects.get(pk=lid)
=======
            uid = Users.objects.get(LOGIN_id=lid)
>>>>>>> 695c1564f21dc5bb418c10a064dd0137c00b2de9
            totalp = Task.objects.filter(USER=uid, status='Ongoing').count()
        except (Users.DoesNotExist, ValueError):
            pass  
        
    return {'totalop': totalp}
