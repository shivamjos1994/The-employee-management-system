from django.shortcuts import render, HttpResponse
from .models import Department, Role, Employee
from datetime import datetime
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')


def all_emp(request):
    emp = Employee.objects.all()
    context = {
        'emp': emp
    }
    return render(request,'all_emp.html',context)


def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        new_emp = Employee(first_name=first_name, last_name=last_name, dept_id=dept, role_id=role, salary=salary, bonus=bonus, phone=phone, hire_date=datetime.now())
        new_emp.save()
        return HttpResponse("Employee Has Been Added!!")
    else:
        return render(request, 'add_emp.html')



def remove_emp(request, emp_id = 0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Successfully!")
        except:
            return HttpResponse("Please Select a Valid Employee ID")
    emp = Employee.objects.all()
    context = {
        'emp': emp
    }
    return render(request,'remove_emp.html', context)


def filter_emp(request):
    if request.method == "POST":
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emp = Employee.objects.all()
        if name:
            emp = emp.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
 # Q is used to add filter out more than one attribute, icontains means first/last name can be filter out without uppercase/lowercase and we can filter with a single word.
        if dept:
            emp = emp.filter(dept__name__icontains=dept)
        if role:
            emp = emp.filter(role__name__icontains=role)

        context = {
            'emp': emp
        }
        return render(request,'all_emp.html', context)
    elif request.method == "GET":
         return render(request, 'filter_emp.html')
    else:
        return HttpResponse("An Exception Occurred")