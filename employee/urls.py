from django.contrib import admin  
from django.urls import path,include
from . import views  
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'EmployeeViewSet', views.EmployeeViewSet,'Employee')
router.register(r'AppraisalViewSet',views.AppraisalViewSet,'Appraisal')
router.register(r'DepartmentViewSet',views.DepartmentViewSet)
router.register(r'ManagerViewSet',views.ManagerViewSet,'Manager')
# router.register(r'toDoLists', views.ToDoListViewSet)


urlpatterns = [
    path('register/', views.registerPage , name="register"),
    path('login/', views.loginPage , name="login"),
    path('logout/', views.logoutPage, name="logout"),  
    path('', views.emp, name="home"),  
    path('edit/<int:emp_id>/', views.edit, name='edit'),  
    path('update/<int:emp_id>', views.update, name='update'), 
    path('employee/', include(router.urls)), 
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]  