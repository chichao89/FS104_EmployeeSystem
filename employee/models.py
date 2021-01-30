from django.db import models 
from django.db.models import CheckConstraint, Q, F
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from datetime import date,datetime
# Create your models here.



class Roles(models.Model):
    role_id = models.IntegerField(primary_key = True)
    role = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100)
    last_update = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Roles"
    
    def __str__(self):
        return f"{self.role +' '+ self.description}"


class Department(models.Model):
    dept_id = models.IntegerField(primary_key=True)
    dept_name = models.CharField('Department',max_length=50, unique=True)
    Is_Active = models.BooleanField(default=True)
    last_update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.dept_name)

    class Meta:
        verbose_name_plural = "Departments"

class Manager(models.Model):
    mgr_id = models.IntegerField(primary_key = True)
    first_name = models.CharField('First_Name',max_length=45)
    last_name = models.CharField('Last_Name',max_length=45)
    emp_id = models.IntegerField()

    def __str__(self):
        return (self.first_name + ' ' + self.last_name)

    class Meta:
        verbose_name_plural = "Managers"


class Employee(models.Model):
    MARRIED ='MR'
    SINGLE = 'SN'
    DIVORCED = 'DI'
    WIDOWED = 'WI'
    MALE = 'M'
    FEMALE = 'F'

    marital_status = (
        (MARRIED, "Married"),
        (SINGLE, "Single"),
        (DIVORCED, "Divorced"),
        (WIDOWED, "Widowed")
    )

    gender = (
        (MALE,"male"),
        (FEMALE,"female")
    )

    EmpId = models.IntegerField(primary_key = True)
    first_name = models.CharField('First_Name',max_length=45)
    last_name = models.CharField('Last_Name',max_length=45)
    marital_status = models.CharField('Marital_Status',max_length=15, choices = marital_status)
    phone_number = PhoneNumberField('Phone_Number',unique = True)
    address = models.CharField('Address',max_length=50)
    gender = models.CharField('Gender',max_length=10,choices = gender)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField()
    date_of_leaving = models.DateField('Date_of_Leaving',help_text='The Leaving Date determines whether it is an Active Employee',blank=True, null=False, default='9999-12-31')
    # manager_id  = models.ForeignKey('self',null=True,blank=True, related_name='employee', on_delete=models.DO_NOTHING)
    manager_id = models.ForeignKey('Manager', on_delete=models.CASCADE, blank=True, null=True)
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(Department,on_delete=models.CASCADE,blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    last_update = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.first_name +' '+ self.last_name}"
    
    def Is_Active_Employee(self):
        return self.date_of_leaving >= date.today()
    Is_Active_Employee.boolean = True
   
    def clean(self):
        try:
            if self.date_of_joining < self.date_of_birth:
                raise ValidationError('Date of Joining must be after Date of Birth')
        except:
            raise ValidationError('Date of Joining must be after date of birth')


class Rating(models.Model):
    Best_Performer ='A+'
    Excellent = 'A'
    Very_Good = 'B+'
    Good = 'B'
    Competent = 'C+'
    Average = 'C'
    Poor = 'D'
    Fail = 'F'

    rating = (
        (Best_Performer, "A+"),
        (Excellent, "A"),
        (Very_Good, "B+"),
        (Good, "B"),
        (Competent, "C+"),
        (Average, "C"),
        (Poor, "D"),
        (Fail, "F"),
    )

    rating_id = models.IntegerField(primary_key=True)
    grade = models.CharField('Grade',max_length=15, choices = rating)
    grade_description = models.CharField("Grade Description", max_length=60)
    last_update = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return (self.grade)
   

class Appraisal(models.Model):
    appraisal_id = models.IntegerField(primary_key=True)
    app_supervisor_comments = models.TextField()
    rating_id = models.ForeignKey(Rating,on_delete=models.CASCADE, blank=True, null=True)
    dept_id = models.ForeignKey(Department,on_delete=models.CASCADE, blank=True, null=True)
    emp_id = models.ForeignKey(Employee,on_delete=models.CASCADE, blank=True, null=True)
    appraisal_date = models.DateField('Appraisal_Year', blank=True, null=True)
    last_update = models.DateField(auto_now_add=True)

    def __str__(self):
        return (str(self.appraisal_id))+" - "+(str(self.appraisal_date))
    
    class Meta:
        verbose_name_plural = 'Appraisals'

