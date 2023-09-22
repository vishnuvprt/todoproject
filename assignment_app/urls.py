
from django.urls import path

from assignment_app import views
from .views import *


urlpatterns = [


    path('first/', views.Login_Class.as_view(),name="first"),
    path('signup/', views.SignupClass.as_view(),name="signup"),
    path('admindashboard/', views.AdminDashboardClass.as_view(),name="admindashboard"),
    path('userdashboard/', views.UserDashboardClass.as_view(),name="userdashboard"),
    path('check_email_uniqueness/', CheckEmailUniqueness.as_view(), name='check_email_uniqueness'),
    path('projects/', Project_Class.as_view(), name='projects'),

    path('projects/<int:project_id>/edit/', EditProject_Class.as_view(), name='edit-project'),
    path('projectteam/<int:pid>/', ProjectTeamClass.as_view(), name='projectteam'),
    path('adminviewtasks/<int:uid>/', AdminViewTaskClass.as_view(), name='adminviewtasks'),
    path('deleteitem/<int:pid>/delete/', DeleteProject.as_view(), name='delete_item'),




    path('users/', StaffsClass.as_view(), name='users'),
    path('adminchangepassword/', ChangePasswordAdmin.as_view(), name='adminchangepassword'),
    path('userchangepassword/', ChangePasswordUser.as_view(), name='userchangepassword'),
    path('userassignedprojects/', UserViewAssignedProjects.as_view(), name='userassignedprojects'),
    path('usertasks/', ViewTasksClass.as_view(), name='usertasks'),
    path('usertasks/sort/', SortTasksViewWP.as_view(), name='usertaskssort'),
    path('userassignedprojects/<int:projectid>/add/', AddnewTaskClass.as_view(), name='addnewtask'),
    path('userviewtasks/<int:projectid>/', UserViewTasksClass.as_view(), name='userviewtasks'),
    path('userviewtasks/<int:projectid>/sort/', SortTasksView.as_view(), name='sort_tasks'),
    path('userviewtasks/<int:taskid>/edit/', EditTaskClass.as_view(), name='edittask'),
    path('userviewtasks/<int:taskid>/delete/', Deletetask.as_view(), name='deletetask'),
    path('subtask/<int:taskid>/', SubTaskClass.as_view(), name='subtask'),
    path('subtask/<int:subtaskid>/edit/', SubTaskEditClass.as_view(), name='editsubtask'),
    path('subtask/<int:subtaskid>/delete/', DeleteSubtask.as_view(), name='deletesubtask'),
    path('addsubtask/', AddSubTask.as_view(), name='addsubtask'),
    path('userprofile/', UserProfileClass.as_view(), name='userprofile'),
    path('userprofiledata/', ProfileDataClass.as_view(), name='userprofiledata'),

    path('profile/', UserProfileView.as_view(), name='profile'),
    path('upload-profile-photo/', UploadProfilePhotoView.as_view(), name='upload_profile_photo'),
    path('get-profile-photo/', GetProfilePhotoView.as_view(), name='get_profile_photo'),
    path('remove-profile-photo/', RemoveProfilePhotoView.as_view(), name='remove_profile_photo'),
    path('edit-profile/', EditProfileClass.as_view(), name='edit_profile'),
    path('notifications/', NotificationClass.as_view(), name='notifications'),
    path('reminders/', GetReminderStatus.as_view(), name='reminders'),
    path('updatereminders/', UpdateReminderStatus.as_view(), name='updatereminders'),




    path('logout/', LogoutClass.as_view(), name='logout'),
    path('ulogout/', UserLogoutClass.as_view(), name='ulogout'),
    path('errorpage/', ErrorClass.as_view(), name='errorpage'),




]
