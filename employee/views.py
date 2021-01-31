from django.shortcuts import render,redirect
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework import permissions
from .permissions import IsAdminOrReadOnly,IsManager
# from rest_framework.authentication import TokenAuthentication
from .forms import EmployeeForm, AppraisalForm
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
 

# Create your views here. 
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:    
        form = UserCreationForm()
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + user)
                return redirect('login')

    context = {'form':form}
    return render(request, 'register.html',context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')    
    else:  
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # current_user_id = request.user.id
                # manager = Manager.objects.get(user_id = current_user_id)
                # employee_id = manager_id
                login(request,user)
                return redirect('home')
            else:
                messages.info(request, 'username or password is incorrect')           
        context = {}
        return render(request, 'login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url = 'login')
def emp(request):
     if request.method == 'GET':
        current_user_id = request.user.id
        if request.user.is_superuser:
            #return redirect('http://127.0.0.1:8000/admin')
            return redirect('http://127.0.0.1:8000/employee')
        else:
            
            employee = Employee.objects.get(user_id = current_user_id)
            employee_id = employee.EmpId       
            if Manager.objects.filter(emp_id = employee_id):
                manager_id = Manager.objects.filter(emp_id = employee_id).values('mgr_id')[0]['mgr_id']
                selected_employees = Employee.objects.filter(manager_id = manager_id)
                context = {'employees':selected_employees}
                return render(request,'show.html',context) 
            else:    
                appraisal = Appraisal.objects.get(emp_id = employee_id)
                context = {'form':employee, 'appraisal':appraisal}
                return render(request,'index.html',context) 
    
@login_required(login_url = 'login')
def edit(request, emp_id): 
        emp_id = int(emp_id)
        employee = Employee.objects.get(EmpId=emp_id)
        appraisal = Appraisal.objects.get(emp_id = emp_id)
        ratings = Rating.objects.all()
        context = {'form':employee, 'appraisal':appraisal,'ratings':ratings}
        return render(request,'edit.html', context)  


@login_required(login_url = 'login')
def update(request, emp_id):
    if request.method == 'POST':
        emp_id = int(emp_id)  
        # employee = Employee.objects.get(EmpId=emp_id)
        appraisal = Appraisal.objects.get(emp_id = emp_id)  
        form = AppraisalForm(request.POST, instance = appraisal)  
        if form.is_valid():  
            form.save() 
        return redirect('http://127.0.0.1:8000/')

# def destroy(request, emp_id):  
#     emp_id = int(emp_id)  
#     employee = Employee.objects.get(EmpId=emp_id)  
#     employee.delete()  
#     return redirect("/show")  

    
class EmployeeViewSet(viewsets.ModelViewSet):
    #queryset = Employee.objects.filter(date_of_leaving__gte=date.today())
    # queryset = Employee.objects.all()
    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            return Employee.objects.all()
        else:
            return Employee.objects.filter(user_id=user_id)
    serializer_class = EmployeeSerializer
    permission_classes = (IsAdminOrReadOnly,)
    # permission_classes = (permissions.IsAdminUser,)
    


class AppraisalViewSet(viewsets.ModelViewSet):
    # queryset = Appraisal.objects.all()
    queryset = User.objects.none()
    serializer_class = AppraisalSerializer
    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            return Appraisal.objects.all()
        else:  
            emp_id = Employee.objects.filter(user_id=user_id).values('EmpId')[0]['EmpId']
            if Manager.objects.filter(emp_id = emp_id):
                manager_id = Manager.objects.filter(emp_id = emp_id).values('mgr_id')[0]['mgr_id']
                employee = Employee.objects.filter(manager_id = manager_id)         
                return Appraisal.objects.filter(emp_id__in = employee)             
            else:
                return Appraisal.objects.filter(emp_id = emp_id)
    permission_classes = (permissions.DjangoModelPermissions|IsManager,)
 

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (permissions.IsAdminUser,)

class ManagerViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
             return ManagerSerializer
        else:
            return EmployeeSerializer
    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            return Manager.objects.all()
        else:
            employee = Employee.objects.get(user_id = user_id)
            employee_id = employee.EmpId       
            if Manager.objects.filter(emp_id = employee_id):
                manager_id = Manager.objects.filter(emp_id = employee_id).values('mgr_id')[0]['mgr_id']
                return Employee.objects.filter(manager_id = manager_id)           
    permission_classes = (IsAdminOrReadOnly,)

