import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Sum
from datetime import datetime
from datetime import date
import os 
import joblib
import numpy as np
import pickle

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
    if request.method == 'POST':

        expensehead_id = request.POST.get('expensehead')
        description = request.POST.get('description')
        date_str = request.POST.get('date')
        amount = float(request.POST.get('amount') or 0)

        expensehead = Expensehead.objects.get(id=expensehead_id)

        # ---------- SAVE EXPENSE ----------
        exd = ExpenseDetails(
            user=request.user,
            expensehead=expensehead,
            description=description,
            date=date_str,
            amount=amount
        )
        exd.save()

        # ---------- MONTH CALCULATIONS ----------
        expense_date = datetime.strptime(date_str, "%Y-%m-%d")
        expense_month = expense_date.month
        expense_year = expense_date.year

        # Get the budget for this month & head
        budget = BudgetDetails.objects.filter(
            user=request.user,
            expensehead=expensehead,
            month=expense_month
        ).first()

        if budget and budget.amount > 0:
            # Total expense for this month
            total_expense = ExpenseDetails.objects.filter(
                user=request.user,
                expensehead=expensehead,
                date__year=expense_year,
                date__month=expense_month
            ).aggregate(total=Sum('amount'))['total'] or 0

            # How much the budget can still increase
            remaining_budget = budget.amount - total_expense
            if remaining_budget < 0:
                remaining_budget = 0  # Do not show negative numbers

            msg = f"{remaining_budget}"  # Only the increase value

        else:
            msg = "0"  # If no budget is set, show 0

        return HttpResponse(
            f"<script>alert('{msg}');window.location='/user/expensedetails/';</script>"
        )

    return render(
        request,
        "Expensedetails.html",
        {"expensehead": Expensehead.objects.all()}
    )



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
    




def viewtotal(request):
    expense_data = ExpenseDetails.objects.filter(user=request.user)
    budget_data = BudgetDetails.objects.filter(user=request.user)

    months = [
        ("January", "January"), ("February", "February"), ("March", "March"),
        ("April", "April"), ("May", "May"), ("June", "June"),
        ("July", "July"), ("August", "August"), ("September", "September"),
        ("October", "October"), ("November", "November"), ("December", "December"),
    ]

    # Initialize totals
    total = {m: {"expense": 0.0, "budget": 0.0} for m, _ in months}

    # ---------- EXPENSE ----------
    for e in expense_data:
        if e.date:
            month_key = e.date.strftime("%B")  # January, February...
            total[month_key]["expense"] += float(e.amount)

    # ---------- BUDGET ----------
    for b in budget_data:
        # Convert month number -> month name
        if isinstance(b.month, int):
            month_name = datetime(1900, b.month, 1).strftime("%B")
        else:
            month_name = b.month  # if already stored as name

        if month_name in total:
            total[month_name]["budget"] += float(b.amount)

    totaldata = []

    # ---------- ALERT + DATA ----------
    for m, name in months:
        expense = total[m]["expense"]
        budget = total[m]["budget"]

        if budget > 0:
            if expense <= budget:
                remaining_budget = budget - expense
                messages.info(
                    request,
                    f"✅ {name}: Budget can still increase by {remaining_budget}"
                )
            else:
                increase_needed = expense - budget
                messages.warning(
                    request,
                    f"⚠️ {name}: Expense exceeds budget! Increase budget by {increase_needed}"
                )

        totaldata.append({
            "month": name,
            "total_expense": expense,
            "total_budget": budget,
        })

    return render(request, "viewtotal.html", {"totaldata": totaldata})



from django.db.models import Sum
from datetime import datetime, date
from decimal import Decimal


def overbudget(request, month):
    current_year = date.today().year

    # Convert month name to month number
    month_number = datetime.strptime(month, "%B").month

    # Get all expenses for selected month
    expense_data = ExpenseDetails.objects.filter(
        user=request.user,
        date__month=month_number,
        date__year=current_year
    )

    # Group by expensehead and SUM
    grouped_expenses = expense_data.values(
        'expensehead__id',
        'expensehead__name'
    ).annotate(
        total_amount=Sum('amount')
    )

    budget_data = BudgetDetails.objects.filter(
        user=request.user,
        month=month
    )

    overbudget_expenses = []

    for expense in grouped_expenses:
        budget_for_head = budget_data.filter(
            expensehead_id=expense['expensehead__id']
        ).first()

        if budget_for_head and expense['total_amount'] > budget_for_head.amount:
            overbudget_expenses.append({
                "expensehead": expense['expensehead__name'],
                "total_expense": expense['total_amount'],
                "budget": budget_for_head.amount,
                "over_by": expense['total_amount'] - budget_for_head.amount
            })

    return render(request, "overbudget.html", {
        "overbudget_expenses": overbudget_expenses,
        "month": month,
        "year": current_year
    })



# Load model once (IMPORTANT)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'loan_rf_optimized.pkl')
print(f"Loading model from: {model_path}")
model = joblib.load(model_path)

def prediction(request):
     if request.method == "POST":

        features = [
            int(request.POST.get('no_of_dependents')),
            int(request.POST.get('education')),
            int(request.POST.get('self_employed')),
            float(request.POST.get('income_annum')),
            float(request.POST.get('loan_amount')),
            float(request.POST.get('loan_term')),
            int(request.POST.get('cibil_score')),
            float(request.POST.get('residential_assets_value')),
            float(request.POST.get('commercial_assets_value')),
            float(request.POST.get('luxury_assets_value')),
            float(request.POST.get('bank_asset_value')),
            ]


        features = np.array(features).reshape(1, -1)

        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

        if prediction == 1:
            result = "Eligible for Loan Approval"
        else:
            result = "Not Eligible for Loan Approval"

        return render(
            request,
            'result.html',
            {
                'result': result,
                'probability': round(probability * 100, 2)
            }
        )

     return render(request, 'loan.html')








