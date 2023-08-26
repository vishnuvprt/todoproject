
from functools import wraps
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
# Create your views here.
from django.utils import timezone
from django.views import View
from .forms import *
from .models import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator
from .utils import log_user_action
from django.core.serializers import serialize



def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):

        if request.session['lid'] == 'None' or request.session['lid'] is None:
            return redirect('/myapp/errorpage/') 

        return view_func(request, *args, **kwargs)
    return _wrapped_view




class ErrorClass(View):
    template_name = "PM/pages-error-404.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)





class Login_Class(View):
    template_name = "PM/pages-login.html"

    def get(self, request, *args, **kwargs):
        form = login_form()
        return render(request, self.template_name, {'form': form})

    def post(self,request,*args,**kwargs):
        form=login_form(request.POST)
        if form.is_valid():
            uname=form.cleaned_data['username']
            password=form.cleaned_data['password']
            try:
                lobj=Login.objects.get(email=uname,password=password)
                if lobj.type=='admin':
                    request.session['lid']=lobj.id

                    return HttpResponse("<script>alert('Welcome Admin');window.location='/myapp/admindashboard/'</script>")
                else:
                    request.session['lid'] = lobj.id
                    uid=Users.objects.get(LOGIN=lobj)
                    log_user_action(uid,'Logged In')
                    return HttpResponse("<script>alert('Welcome User');window.location='/myapp/userdashboard/'</script>")
            except Exception as e:
                print(e)
                return render(request, self.template_name, {'form': form,'Error':'No user found'})
        else:

            return render(request, self.template_name, {'form': form})



class SignupClass(View):
    template_name = "PM/pages-register.html"

    def get(self, request, *args, **kwargs):
        form = SignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']

            lobj = Login.objects.create(email=email, password=password, type='user')
            uobj = Users.objects.create(LOGIN=lobj, name=name, email=email, phone=phone)
            log_user_action(uobj,'New user signed up' )
            return HttpResponse("<script>alert('Account Created');window.location='/myapp/first/'</script>")
        else:
            return render(request, self.template_name, {'form': form,'Error':form.errors})
        



class ChangePasswordAdmin(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = changepassword_form()
        return render(request, "PM/change-password.html", {'form': form})
    
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        form=changepassword_form(request.POST)
        if form.is_valid():
            oldp=form.cleaned_data['oldpassword']
            newp=form.cleaned_data['newpassword']
            confp=form.cleaned_data['confirmpassword']
            try:
                lobj=Login.objects.get(password=oldp,pk=request.session['lid'])
                lobj.password=newp
                lobj.save()
                return HttpResponse("<script>alert('Password Changed');window.location='/myapp/first/'</script>")

            except Exception as e:

                return render(request, "PM/change-password.html", {'form': form,'Error':'User not found'})
        else:
            print(form.errors)
            return render(request, "PM/change-password.html", {'form': form,'Error':form.errors})







class AdminDashboardClass(View):
    template_name="PM/dashboard.html"
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        lobj=Logs.objects.all().order_by('-timestamp')

        return render(request, self.template_name,{'data':lobj})


class UserDashboardClass(View):
    template_name = "User/dashboard.html"
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        import datetime
        lobj=Logs.objects.filter(USER=Users.objects.get(LOGIN=request.session['lid'])).order_by('-timestamp')

        return render(request, self.template_name,{'data':lobj})


class Project_Class(View):
    template_name="PM/tables-projects.html"
    form_class=projectFilterClass
    def get_queryset(self):
        queryset=Project.objects.all()
        form=self.form_class(self.request.GET)
        if form.is_valid():
            project_type=form.cleaned_data.get('typeofproject')
            project_status=form.cleaned_data.get('statusofproject')
            if project_type:
                queryset=queryset.filter(type=project_type)
            if project_status:
                queryset=queryset.filter(status=project_status)
        return queryset
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = new_project_form()
        eform = edit_project_form()
        projects=self.get_queryset()
        fform=self.form_class(self.request.GET)

        paginator = Paginator(projects, 5)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        


        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            filtered_projects = [
                {
                    'id': project.id,
                    'projectname': project.projectname,
                    'description': project.description,
                    'startdate': project.startdate,
                    'enddate': project.enddate,
                    'duration': project.duration,
                    'status': project.status
                }
                for project in projects
            ]
            

            return JsonResponse({'project': filtered_projects, 'page_number': page_obj.number, 'num_pages': paginator.num_pages})
        return render(request, self.template_name, {'form': form, 'data': page_obj, 'eform': eform, 'filterform': fform})


    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            form=new_project_form(request.POST)
            if form.is_valid():
                pname=form.cleaned_data['pname']
                description=form.cleaned_data['description']
                startd=form.cleaned_data['startdate']
                endd=form.cleaned_data['enddate']
                duration=form.cleaned_data['duration']
                ptype=form.cleaned_data['project_type']
                pc=Project.objects.all().count() 
                pobj=Project.objects.create(projectname=pname,description=description,startdate=startd,enddate=endd,duration=duration,type=ptype,status='Pending')
                selected_users = form.cleaned_data['user_field']
                for i in selected_users:
                    ProjectTeams.objects.create(PROJECT=pobj,USER=i)
                
                
                pc=pc+1

                return JsonResponse({'message':'ok','projectname': pname,
                    'description': description,
                    'startdate': startd,
                    'enddate': endd,
                    'duration': duration,
                    'project_type': ptype,
                    'status': 'pending',
                    'id': pobj.id,
                    'slno':pc
                    
                    })
            else:
                print(form.errors,"new error")
                errors = form.errors.as_json()
                return JsonResponse({'errors': errors}, status=400)
        else:
          
            return HttpResponse("<script>alert('something went wrong!');history.back();</script>")
        



class UserViewAssignedProjects(View):
    template_name="User/tables-projects.html"
    form_class=projectFilterClass

    form_class=projectFilterClass
    def get_queryset(self):
        queryset = ProjectTeams.objects.filter(USER=Users.objects.get(LOGIN=self.request.session['lid']))
        fform = self.form_class(self.request.GET)
        
        if fform.is_valid():
            project_type = fform.cleaned_data.get('typeofproject')
            project_status = fform.cleaned_data.get('statusofproject')
            pfromdate = fform.cleaned_data.get('pfromdate')
            ptodate = fform.cleaned_data.get('ptodate')
            
            if project_type:                
                queryset = queryset.filter(PROJECT__type=project_type)
            if project_status:
                queryset = queryset.filter(PROJECT__status=project_status)
            if pfromdate:
                queryset = queryset.filter(PROJECT__startdate__gte=pfromdate)
            if ptodate:
                queryset = queryset.filter(PROJECT__enddate__lte=ptodate)

            
        return queryset

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = add_task_form()
        projects=self.get_queryset()
        fform=self.form_class(self.request.GET)

        paginator = Paginator(projects, 5)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)



        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            filtered_projects = [
                {
                    'id': i.PROJECT.id,
                    'projectname': i.PROJECT.projectname,
                    'description': i.PROJECT.description,
                    'startdate': i.PROJECT.startdate,
                    'enddate': i.PROJECT.enddate,
                    'duration': i.PROJECT.duration,
                    'status': i.PROJECT.status
                }
                for i in projects
            ]
            

            return JsonResponse({'project': filtered_projects, 'page_number': page_obj.number, 'num_pages': paginator.num_pages})
        return render(request, self.template_name, {'form': form, 'data': page_obj, 'filterform': fform})


        
    
    


class EditProject_Class(View):
    template_name = "PM/tables-projects.html"
    @method_decorator(login_required)
    def get(self, request, project_id,*args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                project = Project.objects.get(pk=project_id)
                team=ProjectTeams.objects.filter(PROJECT=project_id)
                userlist = []
                for i in team:
                    userlist.append({
                        'user': i.USER.id
                    })
                project_data = {
                    'project_id' : project.id,
                    'projectname': project.projectname,
                    'description': project.description,
                    'startdate': project.startdate,
                    'enddate': project.enddate,
                    'duration': project.duration,
                    'project_type': project.type,
                    'status': project.status,
                    'userlist': userlist
                }
            
                return JsonResponse(project_data)
            except Project.DoesNotExist:
                return JsonResponse({'error': 'Project not found'}, status=404)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
    
    @method_decorator(login_required)
    def post(self, request, project_id, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            form = edit_project_form(request.POST)
            if form.is_valid():
                try:
                    project = Project.objects.get(pk=project_id)
                    project.projectname = form.cleaned_data['pname']
                    project.description = form.cleaned_data['description']
                    project.startdate = form.cleaned_data['startdate']
                    project.enddate = form.cleaned_data['enddate']
                    project.duration = form.cleaned_data['duration']
                    project.type = form.cleaned_data['project_type']
                    project.status = form.cleaned_data['status']
                    project.save()
                    
                    selected_users = form.cleaned_data['user_field']
                    ProjectTeams.objects.filter(PROJECT=project).delete()  
                    for i in selected_users:
                        ProjectTeams.objects.create(PROJECT=project, USER=i)


                    updated_project_data = {
                    'project_id': str(project),
                    'projectname': project.projectname,
                    'description': project.description,
                    'startdate': project.startdate,
                    'enddate': project.enddate,
                    'duration': project.duration,
                    'project_type': project.type,
                    'status': project.status,
                    }
                    
                    return JsonResponse(updated_project_data)
                except Project.DoesNotExist:
                    errors = {'error': 'Project not found'}
                    return JsonResponse(errors, status=404)
            else:
                errors = form.errors.as_json()
                print(errors,"errrrrrrrr")
                print(form.errors,"new error")
                return JsonResponse({'errors': errors}, status=400)
        else:
            return HttpResponse("<script>alert('something went wrong!');history.back();</script>")







class ProjectTeamClass(View):
    template_name="PM/tables-team.html"
    
    @method_decorator(login_required)
    def get(self,request,pid,*args,**kwargs):
        request.session['pid']=pid
        tobj=ProjectTeams.objects.filter(PROJECT=pid)
        return render(request,self.template_name,{'team':tobj})





class DeleteProject(View):
    @method_decorator(login_required)
    def get(self, request, pid, *args, **kwargs):

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                project = Project.objects.get(pk=pid)
                project.delete()
                return JsonResponse({'success': True})
            except Project.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)




class StaffsClass(View):
    template_name = "PM/tables-data.html"
    form_class = StaffFilterForm

    def get_queryset(self, name):
        return Users.objects.filter(name__icontains=name)
    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        persons = []

        if form.is_valid():
            name = form.cleaned_data.get('name')
            persons = self.get_queryset(name)
            
            paginator = Paginator(persons, 5)  
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            data = [{
                'id': person.id,
                'name': person.name,
                'email': person.email,
                'phone': person.phone,
                'photo': person.photo.url if person.photo else None,
            } for person in persons]
            
            return JsonResponse({'persons': data,'page_number': page_obj.number, 'num_pages': paginator.num_pages})
        
        return render(request, self.template_name, {'form': form, 'persons': page_obj})















class AdminViewTaskClass(View):
    template_name="PM/users-task.html"
    @method_decorator(login_required)
    def get(self,request,uid,*args,**kwargs):
        pid=request.session['pid']
        tobj=Task.objects.filter(USER=uid,PROJECT=pid)
        return render(request,self.template_name,{'data':tobj})
        







class ChangePasswordUser(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = changepassword_form()
        return render(request, "User/change-password.html", {'form': form})
    
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        form=changepassword_form(request.POST)
        if form.is_valid():
            oldp=form.cleaned_data['oldpassword']
            newp=form.cleaned_data['newpassword']
            confp=form.cleaned_data['confirmpassword']
            try:
                lobj=Login.objects.get(password=oldp,pk=request.session['lid'])
                lobj.password=newp
                lobj.save()
                uid=Users.objects.get(LOGIN=request.session['lid'])
                log_user_action(uid,'Password Changed')
                log_user_action(uid,'Logged Out')
                return HttpResponse("<script>alert('Password Changed');window.location='/myapp/first/'</script>")

            except Exception as e:
                print(e)
                return render(request, "User/change-password.html", {'form': form,'Error':'User not found'})
        else:
            return render(request, "User/change-password.html", {'form': form})





    
    
    
class AddnewTaskClass(View):
    @method_decorator([login_required])
    def post(self, request,projectid,*args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            form = add_task_form(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                description=form.cleaned_data['description']
                duedate=form.cleaned_data['duedate']
                priority=form.cleaned_data['priority']
                uid=Users.objects.get(LOGIN=request.session['lid'])
                print(projectid,"ooooooo")
                pobj=Project.objects.get(pk=projectid)
                if pobj.status not in ['Completed','Onhold','Cancel']:
                    tobj=Task.objects.create(title=title,description=description,duedate=duedate,priority=priority,USER=uid,PROJECT_id=projectid)
                    log_user_action(uid,"New Task added")
                    return JsonResponse({'message': 'Task added successfully'})
                else:
                    status='Project '+pobj.status
                    return JsonResponse({'message':status+',Contact Project cordinator for further details'})


            else:
                print(form.errors)
                return JsonResponse({'error': 'Form is not valid'})
        else:
            return HttpResponse("<script>alert('something went wrong!');history.back();</script>")








class UserViewTasksClass(View):
    template_name="User/tables-data.html"
    form_class=FilterTaskForm
    def get_queryset(self):
        queryset= Task.objects.filter(PROJECT=self.request.session['projectid'], USER=Users.objects.get(LOGIN=self.request.session['lid']))
        form=self.form_class(self.request.GET)
        if form.is_valid():
            priority=form.cleaned_data.get('priority')
            status=form.cleaned_data.get('status')
            fdate=form.cleaned_data.get('fromdate')
            tdate=form.cleaned_data.get('todate')
            if priority:
                queryset=queryset.filter(priority=priority)
            if status:
                queryset=queryset.filter(status=status)
            if fdate:
                queryset=queryset.filter(duedate__gte=fdate)

            if tdate:
                queryset=queryset.filter(duedate__lte=tdate)

        
        return queryset
    


    @method_decorator([login_required])
    def get(self, request, projectid, *args, **kwargs):
        request.session['projectid']=projectid
        form = edit_task_form()
        tasks=self.get_queryset()
        fform=self.form_class(self.request.GET)

       


        paginator = Paginator(tasks, 5)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            filtered_tasks = [
                {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'duedate': task.duedate,
                    'status': task.status,
                    'priority': task.priority,
                 
                }
                for task in tasks
            ]
        
            

            return JsonResponse({'tasks': filtered_tasks, 'page_number': page_obj.number, 'num_pages': paginator.num_pages})
        return render(request, self.template_name, {'form': form, 'data': page_obj, 'fform': fform,'pid':request.session['projectid']})

  
class SortTasksView(View):
    def get_queryset(self):
        queryset = Task.objects.filter(PROJECT=self.request.session['projectid'], USER=Users.objects.get(LOGIN=self.request.session['lid']))
        sort_by = self.request.GET.get('sort_by')
        print(sort_by)
        if sort_by == 'title_asc':
            queryset = queryset.order_by('title')
        elif sort_by == 'title_desc':
            queryset = queryset.order_by('-title')

        elif sort_by == 'priority_asc':
            queryset = queryset.order_by('priority')

        elif sort_by == 'priority_desc':
            queryset = queryset.order_by('-priority')

        return queryset

    @method_decorator([login_required])
    def get(self, request, *args, **kwargs):
        tasks = self.get_queryset()
        sorted_tasks = [
            {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'duedate': task.duedate,
                'status': task.status,
                'priority': task.priority,
            }
            for task in tasks
        ]
        return JsonResponse({'tasks': sorted_tasks})




class SortTasksViewWP(View):
    def get_queryset(self):
        queryset = Task.objects.filter(USER=Users.objects.get(LOGIN=self.request.session['lid']))
        sort_by = self.request.GET.get('sort_by')
        print(sort_by)
        if sort_by == 'title_asc':
            queryset = queryset.order_by('title')
        elif sort_by == 'title_desc':
            queryset = queryset.order_by('-title')

        elif sort_by == 'priority_asc':
            queryset = queryset.order_by('priority')

        elif sort_by == 'priority_desc':
            queryset = queryset.order_by('-priority')
            
        return queryset

    @method_decorator([login_required])
    def get(self, request, *args, **kwargs):
        tasks = self.get_queryset()
        sorted_tasks = [
            {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'duedate': task.duedate,
                'status': task.status,
                'priority': task.priority,
            }
            for task in tasks
        ]
        return JsonResponse({'tasks': sorted_tasks})













class ViewTasksClass(View):
    template_name="User/tables-task.html"
    form_class=FilterTaskForm
    def get_queryset(self):
        queryset= Task.objects.filter(USER=Users.objects.get(LOGIN=self.request.session['lid']))
        print(queryset,"dataaaaaaaa")
        form=self.form_class(self.request.GET)
        if form.is_valid():
            priority=form.cleaned_data.get('priority')
            status=form.cleaned_data.get('status')
            fdate=form.cleaned_data.get('fromdate')
            tdate=form.cleaned_data.get('todate')
            if priority:
                queryset=queryset.filter(priority=priority)
            if status:
                queryset=queryset.filter(status=status)

            if fdate:
                queryset=queryset.filter(duedate__gte=fdate)

            if tdate:
                queryset=queryset.filter(duedate__lte=tdate)
            sort_by = self.request.GET.get('sort_by')
        if sort_by:
            if sort_by == 'title_asc':
                queryset = queryset.order_by('title')
            elif sort_by == 'title_desc':
                queryset = queryset.order_by('-title')
            elif sort_by == 'priority_asc':
                queryset = queryset.order_by('priority')
            elif sort_by == 'priority_desc':
                queryset = queryset.order_by('-priority')



        return queryset
    


    @method_decorator([login_required])
    def get(self, request, *args, **kwargs):
        form = edit_task_form()
        user = Users.objects.get(LOGIN=request.session['lid'])
        addtaskform = add_task_form_2(user)
        tasks=self.get_queryset()
        fform=self.form_class(self.request.GET)

       


        paginator = Paginator(tasks, 5)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        
        
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            filtered_tasks = [
                {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'duedate': task.duedate,
                    'status': task.status,
                    'priority': task.priority,
                 
                }
                for task in tasks
            ]
        
            

            return JsonResponse({'tasks': filtered_tasks, 'page_number': page_obj.number, 'num_pages': paginator.num_pages})
        return render(request, self.template_name, {'form': form,'addtaskform':addtaskform, 'data': page_obj, 'fform': fform})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        uid = Users.objects.get(LOGIN=request.session['lid'])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            form = add_task_form_2(uid, request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                duedate = form.cleaned_data['duedate']
                priority = form.cleaned_data['priority']

                project_value = form.cleaned_data['project']
                try:
                    projectid = int(project_value)
                except ValueError:
                    print("Error: Unable to convert project value to int")
                    return JsonResponse({'error': 'Invalid project value'})
                pobj=Project.objects.get(pk=projectid)
                if pobj.status not in ['Completed','Onhold','Cancel']:

                    tobj = Task.objects.create(
                        title=title, description=description, duedate=duedate,
                        priority=priority, USER=uid, PROJECT_id=projectid
                    )
                # Assuming log_user_action is defined elsewhere
                    log_user_action(uid, "New Task added")
                    return JsonResponse({'message': 'Task added successfully', 'id': tobj.id,
                    'title': title,
                    'description': description,
                    'duedate': duedate,
                    'priority': priority,
                    })
                else:
                    status='Project '+pobj.status
                    return JsonResponse({'message':status})


            else:
                errors = form.errors.as_json()
                return JsonResponse({'error': errors})
        else:
            return JsonResponse({'error': 'Invalid request'})
        









class EditTaskClass(View):
    template_name = "User/tables-data.html"
    @method_decorator(login_required)
    def get(self, request, taskid,*args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            
            try:
                task = Task.objects.get(pk=taskid)

                task_data = {
                    'taskid' : task.id,
                    'title': task.title,
                    'description': task.description,
                    'duedate': task.duedate,
                    'priority': task.priority,
                    'status': task.status,
                }
            
                return JsonResponse(task_data)
            except Task.DoesNotExist:
                return JsonResponse({'error': 'Task not found'}, status=404)
        else:
            
            return JsonResponse({'error': 'Invalid request'}, status=400)
    
    @method_decorator(login_required)
    def post(self, request, taskid, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            form = edit_task_form(request.POST)
            if form.is_valid():
                try:
                    tobj = Task.objects.get(pk=taskid)
                    tobj.title = form.cleaned_data['title']
                    tobj.description = form.cleaned_data['description']
                    tobj.duedate = form.cleaned_data['duedate']
                    tobj.priority = form.cleaned_data['priority']
                    tobj.status = form.cleaned_data['status']
                    tobj.save()
                    uptaskdata = {
                    'taskid': tobj.id,
                    'title': tobj.title,
                    'description': tobj.description,
                    'duedate': tobj.duedate,
                    'priority': tobj.priority,
                    'status': tobj.status,
                    }
                    uid=Users.objects.get(LOGIN=request.session['lid'])
                    log_user_action(uid,"Task Updated")
                    return JsonResponse(uptaskdata)
                except Project.DoesNotExist:
                    errors = {'error': 'Task not found'}
                    return JsonResponse(errors, status=404)
            else:
                errors = form.errors.as_json()
                print(errors,"errrrrrrrr")
                return JsonResponse({'errors': errors}, status=400)
        else:
            return HttpResponse("<script>alert('something went wrong!');history.back();</script>")





class SubTaskClass(View):
    template_name="User/tables-subtask.html"
    def get(self,request,taskid,*args,**kwargs):
        request.session['taskid']=taskid
        stobj=Subtask.objects.filter(TASK=taskid)
        form=add_subtask_form()
        eform=edit_subtask_form()
        return render(request,self.template_name,{'data':stobj,'form':form,'eform':eform})
    







class SubTaskEditClass(View):    
    template_name="User/tables-subtask.html"
    def get(self,request,subtaskid,*args,**kwargs):
        stobj=Subtask.objects.get(pk=subtaskid)
        task_data = {
                    'taskid' : stobj.id,
                    'title': stobj.title,
                    'status': stobj.status,
                }
            
        return JsonResponse(task_data)

    @method_decorator(login_required)
    def post(self, request, subtaskid, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            form = edit_subtask_form(request.POST)
            if form.is_valid():
                try:
                    tobj = Subtask.objects.get(pk=subtaskid)
                    tobj.title = form.cleaned_data['title']
                    tobj.status = form.cleaned_data['status']
                    tobj.save()
                    uptaskdata = {
                    'taskid': tobj.id,
                    'status': tobj.status,
                    }
                    uid=Users.objects.get(LOGIN=request.session['lid'])
                    log_user_action(uid,"Subtask Updated")
                    return JsonResponse(uptaskdata)
                except Project.DoesNotExist:
                    errors = {'error': 'Task not found'}
                    return JsonResponse(errors, status=404)
            else:
                errors = form.errors.as_json()
                print(errors,"errrrrrrrr")
                return JsonResponse({'errors': errors}, status=400)
        else:
            return HttpResponse("<script>alert('something went wrong!');history.back();</script>")





class AddSubTask(View):
    @method_decorator([login_required])
    def post(self, request,*args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            form = add_subtask_form(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                uid=Users.objects.get(LOGIN=request.session['lid'])
                sobj=Subtask.objects.filter(TASK_id=request.session['taskid']).count()
                tobj=Subtask.objects.create(title=title,TASK_id=request.session['taskid'])
                log_user_action(uid,"New Sub Task added")
                sobj +=1
                return JsonResponse({'message':'ok','title': title,
                    'status': 'pending',
                    'id': tobj.id,
                    'slno':sobj
                    })

                
            else:
                return JsonResponse({'error': 'Form is not valid'})
        else:
            return HttpResponse("<script>alert('something went wrong!');history.back();</script>")




class DeleteSubtask(View):
    @method_decorator([login_required])
    def get(self,request,subtaskid,*args,**kwargs ):
        sobj=Subtask.objects.get(pk=subtaskid)
        sobj.delete()
        uid=Users.objects.get(LOGIN=request.session['lid'])
        log_user_action(uid,"Subtask deleted")
        return JsonResponse({'message':'deleted'})

class Deletetask(View):
    @method_decorator([login_required])
    def get(self,request,taskid,*args,**kwargs ):
        sobj=Task.objects.get(pk=taskid)
        sobj.delete()
        uid=Users.objects.get(LOGIN=request.session['lid'])
        log_user_action(uid,"Task deleted")
        return JsonResponse({'message':'deleted'})











class UserProfileClass(View):
    template_name='User/users-profile.html'
    @method_decorator([login_required])
    def get(self,request,*args,**kwargs):
        
        uobj=Users.objects.get(LOGIN=request.session['lid'])
        eform=editprofileform()
        rform=SettingsForm()
        return render(request,self.template_name,{'data':uobj,'eform':eform,'rform':rform})





class EditProfileClass(View):
    template_name='User/users-profile.html'
    @method_decorator([login_required])
    def post(self, request,*args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            form = editprofileform(request.POST)
            if form.is_valid():
                name=form.cleaned_data['name']
                job=form.cleaned_data['job']
                phone=form.cleaned_data['phone']
                
                uid=Users.objects.get(LOGIN=request.session['lid'])
                uid.name=name
                uid.type=job
                uid.phone=phone
                uid.save()


                log_user_action(uid,"Profile Updated")

                return JsonResponse({'message':'ok','name': name,
                    'job': job,
                    'phone':phone 
                    })

                
            else:
                print(form.errors)
                return render(request,self.template_name,{'Error':form.errors,'eform':form})

                
        else:
            return HttpResponse("<script>alert('something went wrong!');history.back();</script>")





class ProfileDataClass(View):
    @method_decorator([login_required])
    def get(self, request, *args, **kwargs):

        try:

            uobj = Users.objects.get(LOGIN=request.session['lid'])

            if uobj.photo:  # Check if the photo field is not None
                photo = uobj.photo.url
            else:
                photo = '/static/assets/img/20230814095643.jpg'

            data = {
                'name': uobj.name,
                'email': uobj.email,
                'job': uobj.type,
                'photo': photo,
                'phone': uobj.phone
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'data':'No data'})









class UserProfileView(View):

    template_name = 'User/users-profile.html'
    @method_decorator([login_required])
    def get(self, request, *args, **kwargs):
        user = request.session['lid']
        try:
            user_profile = Users.objects.get(LOGIN=user)
        except Users.DoesNotExist:
            user_profile = None

        form = ProfilePhotoUploadForm()
        context = {
            'data': user_profile,
            'eform': form,
        }
        return render(request, self.template_name, context)

class UploadProfilePhotoView(View):
    @method_decorator([login_required])
    def post(self, request, *args, **kwargs):
        form = ProfilePhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            profile_image = form.cleaned_data['profile_image']
            user =  request.session['lid']
            try:
                user_profile = Users.objects.get(LOGIN=user)
                user_profile.photo = profile_image
                user_profile.save()
                log_user_action(user_profile,'Profile photo updated')

                return JsonResponse({'success': True})
            except Users.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'User not found'})
        else:
            print(form.errors)
            return JsonResponse({'success': False})
        


class GetProfilePhotoView(View):
    @method_decorator([login_required])
    def get(self, request, *args, **kwargs):
        user = request.session['lid']
        try:
            user_profile = Users.objects.get(LOGIN=user)
            photo_url = user_profile.photo.url if user_profile.photo  else '/static/assets/img/20230814095643.jpg'
            print(photo_url)
            return JsonResponse({'photo': photo_url})
        except Users.DoesNotExist:
            return JsonResponse({'photo': '/static/assets/img/20230814095643.jpg'})



class GetReminderStatus(View):
    @method_decorator([login_required])
    def get(self, request, *args, **kwargs):
        user_login = request.session['lid']
        try:
            user = Users.objects.get(LOGIN=user_login)
            try:
                reminder_setting = ReminderSetting.objects.get(USER=user)
                reminder_status = reminder_setting.status
            except ReminderSetting.DoesNotExist:
                reminder_status = 'Off' 
        except Users.DoesNotExist:
            reminder_status = 'Off'  
        
        return JsonResponse({'rs': reminder_status})

class UpdateReminderStatus(View):
    @method_decorator([login_required])
    def post(self, request, *args, **kwargs):
        user = request.session['lid']
        status = request.POST.get('status')  # Assuming you send the status from AJAX
        
        try:
            rs = ReminderSetting.objects.get(USER=Users.objects.get(LOGIN=user))
            rs.status = status
            rs.save()
        except ReminderSetting.DoesNotExist:
            ReminderSetting.objects.create(USER=Users.objects.get(LOGIN=user), status=status)
        
        return JsonResponse({'status': 'updated'})







class RemoveProfilePhotoView(View):
    @method_decorator([login_required])
    def post(self, request, *args, **kwargs):
        try:
            user = Users.objects.get(LOGIN=request.session['lid'])
            if user.photo:
                user.photo.delete()  # Remove the photo file from storage
                user.photo = None    # Set the photo field to None
                user.save()
                log_user_action(user,'Profile photo deleted')
            return JsonResponse({'message': 'Profile photo removed successfully'})
        except Users.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)




class NotificationClass(View):
    template_name="User/notifications.html"
    @method_decorator([login_required])
    def get(self, request, *args, **kwargs):
        from datetime import date
        today = date.today()
        tasks_due_soon = Task.objects.filter(duedate__lte=today,status='Pending',USER=Users.objects.get(LOGIN=request.session['lid']))
        
        paginator = Paginator(tasks_due_soon, 5)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {'data': page_obj})



















#====================================Ajax==================================


class CheckEmailUniqueness(View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email', '')
        is_unique = not Users.objects.filter(email=email).exists()
        return JsonResponse({'is_unique': is_unique})




#=============================================================================


#==============================Util Functions=================================


class LogoutClass(View):
    def get(self,request,*args,**kwargs):
        request.session['lid']='None'
        return redirect('/myapp/first/')
       

class UserLogoutClass(View):
    def get(self,request,*args,**kwargs):
        uid=Users.objects.get(LOGIN=request.session['lid'])
        log_user_action(uid,'Logged Out')
        request.session['lid']='None'
        return redirect('/myapp/first/')
    



            

#==============================================================================
