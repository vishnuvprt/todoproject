from django.db import models
from django.core.validators import RegexValidator




# Create your models here.

TYPE_CHOICES = (
    ('Website', 'Website'),
    ('Web Application', 'Web Application'),
    ('Mobile Application', 'Mobile Application'),
    )

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    ('Ongoing', 'Ongoing'),
    ('Cancel', 'Cancel'),
    ('Onhold', 'Onhold'),
)

PRIORITY_CHOICES = (
    ('High', 'High'),
    ('Medium', 'Medium'),
    ('Low', 'Low'),
)



class Login(models.Model):
    email=models.EmailField(max_length=254,unique=True)
    password = models.CharField(max_length=20)
    type = models.CharField(max_length=20,default='user')

class Users(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    phone = models.BigIntegerField(null=False,default=0)
    photo=models.ImageField(upload_to='media/',null=True,default='None')
    email=models.EmailField(max_length=254,unique=True)
    type=models.CharField(max_length=100,null=True,default='None')


class Project(models.Model):
    projectname=models.CharField(max_length=50)
    description=models.TextField()
    startdate=models.DateField()
    enddate=models.DateField()
    duration=models.CharField(max_length=20)
    type=models.CharField(max_length=20,choices=TYPE_CHOICES)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES)


class ProjectTeams(models.Model):
    PROJECT=models.ForeignKey(Project,on_delete=models.CASCADE)
    USER=models.ForeignKey(Users,on_delete=models.CASCADE)


class Task(models.Model):
    title=models.CharField(max_length=20)
    description=models.TextField()
    duedate=models.DateField()
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    priority=models.CharField(max_length=20,choices=PRIORITY_CHOICES,default='Low')
    USER=models.ForeignKey(Users,on_delete=models.CASCADE)
    PROJECT=models.ForeignKey(Project,on_delete=models.CASCADE)

class Subtask(models.Model):
    TASK=models.ForeignKey(Task,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')


class Logs(models.Model):
    USER=models.ForeignKey(Users,on_delete=models.CASCADE)
    logtext=models.CharField(max_length=100)
    timestamp = models.DateTimeField()



class ReminderSetting(models.Model):
    USER=models.OneToOneField(Users,on_delete=models.CASCADE)
    status=models.CharField(max_length=10,default='On')