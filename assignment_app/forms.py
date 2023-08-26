import re
from django import forms
from .models import *
from django.core.validators import MinLengthValidator



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




class login_form(forms.Form):
    username = forms.EmailField(
        label="Username",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'yourUsername',
            'required': True,
        }),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'yourPassword',
            'required': True,
        }),
    )




class SignupForm(forms.Form):
    name = forms.CharField(

        label="Your Name",
        max_length=20,
        validators=[MinLengthValidator(limit_value=3, message="Field must have at least 3 characters.")],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'yourName',
            'required': True,
        }),
    )

    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'yourEmail',
            'required': True,
        }),
    )

    phone = forms.CharField(
        label="Your Phone",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'yourPhone',
            'required': True,
           
        }),
    )

    password = forms.CharField(
        label="Your Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'yourPassword',
            'required': True,
        }),
    )

    cpassword = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'yourcPassword',
            'required': True,
        }),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check if the email is unique
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken. Please choose another.")

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not password:
            raise forms.ValidationError("Password is required.")

        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$'
        if not re.match(password_regex, password):
            raise forms.ValidationError(
                "Password must be 8-20 characters long and contain at least one lowercase letter, one uppercase letter, one digit, and one special character (@$!%*?&)."
            )

        return password







class new_project_form(forms.Form):
    pname = forms.CharField(
        label="Project Name",
        max_length=50,
        validators=[MinLengthValidator(limit_value=3, message="Field must have at least 3 characters.")],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingName',
            'required': True,
            'placeholder':'Project Name'
        }),
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'floatingTextarea',
            'required': True,
            'placeholder': 'Description'
        }),
    )
    startdate = forms.DateField(
        label="Start Date",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'floatingSdate',
            'required': True,
            'type':'date'
        }),
    )
    enddate = forms.DateField(
        label="End Date",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'floatingEdate',
            'required': True,
            'type': 'date',
        }),
    )
    duration = forms.CharField(
        label="Duration",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingDuration',
            'required': True,
            'readonly':True,
            'placeholder': 'Project Name',

        }),
    )
    project_type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-select','id':"floatingSelect"}))
    user_field = forms.ModelMultipleChoiceField(queryset=Users.objects.all(), label="Select User",widget=forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'userField'}),required=True)





class edit_project_form(forms.Form):
    pname = forms.CharField(
        label="Project Name",
        max_length=50,
        validators=[MinLengthValidator(limit_value=3, message="Field must have at least 3 characters.")],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingName',
            'required': True,
            'placeholder':'Project Name'
        }),
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'floatingTextarea',
            'required': True,
            'placeholder': 'Description'
        }),
    )
    startdate = forms.DateField(
        label="Start Date",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'floatingSdate',
            'required': True,
            'type':'date'
        }),
    )
    enddate = forms.DateField(
        label="End Date",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'floatingEdate',
            'required': True,
            'type': 'date',
        }),
    )
    duration = forms.CharField(
        label="Description",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingDuration',
            'required': True,
            'readonly':True,
            'placeholder': 'Project Duration',

        }),
    )
    project_type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-select','id':"floatingSelect"}))
    user_field = forms.ModelMultipleChoiceField(queryset=Users.objects.all(), label="Select User",widget=forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'userField'}),required=True)
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-select','id':"floatingSelect2"}))








class add_task_form(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=20,
        validators=[MinLengthValidator(limit_value=3, message="Field must have at least 3 characters.")],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingTitle',
            'required': True,
            'placeholder':'Title'
        }),
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'floatingDescription',
            'required': True,
            'placeholder': 'Description'
        }),
    )
    duedate = forms.DateField(
        label="Due Date",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'floatingDdate',
            'required': True,
            'type':'date'
        }),
    )

    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, widget=forms.Select(attrs={'class': 'form-select','id':"floatingPriority"}))




class edit_task_form(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=20,
        validators=[MinLengthValidator(limit_value=3, message="Field must have at least 3 characters.")],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingName',
            'required': True,
            'placeholder':'Title'
        }),
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'floatingTextarea',
            'required': True,
            'placeholder': 'Description'
        }),
    )
    duedate = forms.DateField(
        label="Due Date",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'floatingSdate',
            'required': True,
            'type':'date'
        }),
    )

    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, widget=forms.Select(attrs={'class': 'form-select','id':"floatingSelect"}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-select','id':"floatingSelect2"}))






class add_subtask_form(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=50,
        validators=[MinLengthValidator(limit_value=3, message="Field must have at least 3 characters.")],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingName',
            'required': True,
            'placeholder':'Title'
        }),
    )




class edit_subtask_form(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=50,
        validators=[MinLengthValidator(limit_value=3, message="Field must have at least 3 characters.")],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingName',
            'required': True,
            'placeholder': 'Title'
        }),
    )

    status = forms.ChoiceField(choices=STATUS_CHOICES,widget=forms.Select(attrs={'class': 'form-select', 'id': "floatingSelect2"}))





class changepassword_form(forms.Form):
    oldpassword = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'op',
            'required': True,
            'placeholder':'Old Password'
        }),
    )
    newpassword = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'yourPassword',
            'required': True,
            'placeholder': 'New Password',
            
        }),
    )
    confirmpassword = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'yourCPassword',
            'required': True,
            'placeholder': 'Confirm Password'
        }),
    )
    def clean_password(self):
        password = self.cleaned_data.get('newpassword')

        if not password:
            raise forms.ValidationError("Password is required.")

        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$'
        if not re.match(password_regex, password):
            raise forms.ValidationError(
                "Password must be 8-20 characters long and contain at least one lowercase letter, one uppercase letter, one digit, and one special character (@$!%*?&)."
            )

        return password

    



class projectFilterClass(forms.Form):
    typeofproject=forms.ChoiceField(choices=TYPE_CHOICES,required=False,widget=forms.Select(attrs={'class': 'form-select-sm', 'id': "typeselect"}))
    statusofproject=forms.ChoiceField(choices=STATUS_CHOICES,required=False,widget=forms.Select(attrs={'class': 'form-select-sm ', 'id': "stsselect"})) 
    pfromdate=forms.DateField(
        label="From",
        widget=forms.DateInput(attrs={
            'class': 'form-control-sm',
            'id': 'floatingFdate',
            'type':'date'
        }),
        required=False  

    )
    ptodate=forms.DateField(
        label="To",
        widget=forms.DateInput(attrs={
            'class': 'form-control-sm',
            'id': 'floatingTdate',
            'required': False,
            'type':'date'
        }),
        required=False  

    )






class editprofileform(forms.Form):
    name = forms.CharField(
        label="Full Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'fullName',
            'required': True,
        }),
        
    )

    job = forms.CharField(
        label="Job",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'Job',
            'required': True,
        }),
        
    )

    phone = forms.CharField(
        label="Phone",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'Phone',
            'required': True,
            'number': True,
            
        }),
        
    )

    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'Email',
            'required': True,
            'readonly':True,
        }),
    )



class ProfilePhotoUploadForm(forms.Form):
    profile_image = forms.ImageField()


class FilterTaskForm(forms.Form):
    priority=forms.ChoiceField(choices=PRIORITY_CHOICES,required=False,widget=forms.Select(attrs={'class': 'form-select-sm', 'id': "prioritychoice"})) 
    status=forms.ChoiceField(choices=STATUS_CHOICES,required=False,widget=forms.Select(attrs={'class': 'form-select-sm', 'id': "statuschoice"})) 
    fromdate=forms.DateField(
        label="From",
        widget=forms.DateInput(attrs={
            'class': 'form-control-sm',
            'id': 'fromdate',
            'type':'date'
        }),
        required=False  

    )

    todate=forms.DateField(
        label="TO",
        widget=forms.DateInput(attrs={
            'class': 'form-control-sm',
            'id': 'todate',
            'type':'date'
        }),
        required=False  

    )






class StaffFilterForm(forms.Form):
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'searchname',
            'placeholder': 'Search name here....',
        }),
        required=False
    )




class add_task_form_2(forms.Form):



    title = forms.CharField(
        label="Title",
        max_length=20,
        validators=[MinLengthValidator(limit_value=3, message="Field must have at least 3 characters.")],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingTitle',
            'required': True,
            'placeholder':'Title'
        }),
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'floatingDescription',
            'required': True,
            'placeholder': 'Description'
        }),
    )
    duedate = forms.DateField(
        label="Due Date",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'floatingDdate',
            'required': True,
            'type':'date'
        }),
    )

    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, widget=forms.Select(attrs={'class': 'form-select','id':"floatingPriority"}))
    def __init__(self, user, *args, **kwargs):
        super(add_task_form_2, self).__init__(*args, **kwargs)
        
        projects = ProjectTeams.objects.filter(USER=user)
        project_choices = [(project.PROJECT.id, project.PROJECT.projectname) for project in projects]

        self.fields['project'] = forms.ChoiceField(
            choices=project_choices,
            label="Select Project",
            widget=forms.Select(attrs={'class': 'form-select', 'id': 'projectField'}),
            required=True
        )



class SettingsForm(forms.Form):
      reminder_enabled = forms.BooleanField(
        label="Enable Reminder",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input','id':'flexSwitch'}),
    )







