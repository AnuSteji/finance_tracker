from django.http import HttpResponse
from django.shortcuts import render

from app_core.models import Expensehead, Incomehead
from app_user.models import BudgetDetails, ExpenseDetails, IncomeDetails
from financetracker.users.models import User

# Create your views here.
def incomedetails(request):
    if request.method=='POST':
        
        incomehead=request.POST.get('incomehead')
        date=request.POST.get('date')
        amount=request.POST.get('amount')

        # u=User()
        # u.username=username
        # u.role='User'
        # u.save()

        ind=IncomeDetails() 
        ind.user=request.user
        ind.incomehead=Incomehead.objects.get(id=incomehead)
        ind.date=date
        ind.amount=amount
        ind.save()
        return HttpResponse("<script>alert('Income Details Added Successfully');window.location='/user/incomedetails/';</script>")
    else:
        return render(request, "Incomedetails.html",{"incomehead":Incomehead.objects.all()})
    
def viewdetails(request):
    v=IncomeDetails.objects.filter(user=request.user)
    return render(request,"viewdetails.html",{"list":v})

def deletedetails(request,id):
    d=IncomeDetails.objects.get(id=id)
    d.delete()
    return HttpResponse("<script>alert('Deleted Successfully');window.location='/user/viewdetails/';</script>")

def editdetails(request,id):
   ed=IncomeDetails.objects.get(id=id)
   if request.method=='POST' :
        incomehead= request.POST.get('incomehead')
        date= request.POST.get('date')
        amount= request.POST.get('amount')
        
        ed.incomehead=Incomehead.objects.get(namefield=incomehead)
        ed.date=date
        ed.amount=amount
        ed.save()
        return HttpResponse("<script>alert('Edited Successfully');window.location='/user/viewdetails/';</script>" )
   else:
       return render(request,"editdetails.html",{"det":ed})
   
def expensedetails(request):
    if request.method=='POST':
        
        expensehead=request.POST.get('expensehead')
        description=request.POST.get('description')
        date=request.POST.get('date')
        amount=request.POST.get('amount')
        

        exd=ExpenseDetails() 
        exd.user=request.user
        exd.expensehead=Expensehead.objects.get(id=expensehead)
        exd.description=description
        exd.date=date
        exd.amount=amount
        exd.save()
        return HttpResponse("<script>alert('Expense Details Added Successfully');window.location='/user/expensedetails/';</script>")
    else:
        
        return render(request, "Expensedetails.html",{"expensehead":Expensehead.objects.all()})   
    
def viewexpense(request):
    v=ExpenseDetails.objects.filter(user=request.user)
    return render(request,"viewexpense.html",{"list":v})
def deleteexpense(request,id):
    d=ExpenseDetails.objects.get(id=id)
    d.delete()
    return HttpResponse("<script>alert('Deleted Successfully');window.location='/user/viewexpense/';</script>")

def editexpense(request,id):
    ed=ExpenseDetails.objects.get(id=id)
    if request.method=='POST' :
          expensehead= request.POST.get('expensehead')
          description= request.POST.get('description')
          date= request.POST.get('date')
          amount= request.POST.get('amount')
          
          ed.expensehead=Expensehead.objects.get(name=expensehead)
          ed.description=description
          ed.date=date
          ed.amount=amount
          ed.save()
          return HttpResponse("<script>alert('Edited Successfully');window.location='/user/viewexpense/';</script>" )
    else:
         return render(request,"editexpense.html",{"det":ed})
    
def budgetdetails(request):
    if request.method=='POST':
        
        expensehead=request.POST.get('expensehead')
        month=request.POST.get('month')
        amount=request.POST.get('amount')
        

        bd=BudgetDetails() 
        bd.user=request.user
        bd.expensehead=Expensehead.objects.get(id=expensehead)
        bd.month=month
        bd.amount=amount
        bd.save()
        return HttpResponse("<script>alert('Budget Details Added Successfully');window.location='/user/budgetdetails/';</script>")
    else:
        
        return render(request, "budgetdetails.html",{"expensehead":Expensehead.objects.all()})
    
def viewbudget(request):
    v=BudgetDetails.objects.filter(user=request.user)
    return render(request,"viewbudget.html",{"list":v})

def deletebudget(request,id):
    d=BudgetDetails.objects.get(id=id)
    d.delete()
    return HttpResponse("<script>alert('Deleted Successfully');window.location='/user/viewbudget/';</script>")

def editbudget(request,id):
    ed=BudgetDetails.objects.get(id=id)
    if request.method=='POST' :
          expensehead= request.POST.get('expensehead')
          month= request.POST.get('month')
          amount= request.POST.get('amount')
          
          ed.expensehead=Expensehead.objects.get(name=expensehead)
          ed.month=month
          ed.amount=amount
          ed.save()
          return HttpResponse("<script>alert('Edited Successfully');window.location='/user/viewbudget/';</script>" )
    else:
         return render(request,"editbudget.html",{"ebu":ed})

    

    