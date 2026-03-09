import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Sum
from datetime import datetime
from datetime import date
from django.core.mail import send_mail
import os 
import joblib
import numpy as np
import pickle



from app_core.models import Expensehead, Incomehead
from app_user.models import BudgetDetails, ExpenseDetails, IncomeDetails
from financetracker.users.models import User
from django.db.models.functions import ExtractMonth



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

    month = request.GET.get("month")

    if not month:
        month = datetime.now().month

    data = IncomeDetails.objects.filter(
        user=request.user,
        date__month=month
    )

    total_income = sum(i.amount for i in data)

    return render(request,"viewdetails.html",{
        "list":data,
        "selected_month":int(month),
        "total_income":total_income
    })



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

    if request.method == "POST":

        expensehead_id = request.POST.get("expensehead")
        description = request.POST.get("description")
        date_str = request.POST.get("date")
        amount = float(request.POST.get("amount") or 0)

        expense_date = datetime.strptime(date_str, "%Y-%m-%d")

        # CHECK IF INCOME EXISTS FOR THAT MONTH
        income_exists = IncomeDetails.objects.filter(
            user=request.user,
            date__year=expense_date.year,
            date__month=expense_date.month
        ).exists()

        if not income_exists:
            messages.error(
                request,
                "⚠ Please add income first before adding expenses."
            )
            return redirect("user:expensedetails")


        expensehead = Expensehead.objects.get(id=expensehead_id)

        # SAVE EXPENSE
        ExpenseDetails.objects.create(
            user=request.user,
            expensehead=expensehead,
            description=description,
            date=date_str,
            amount=amount
        )

        expense_month = expense_date.strftime("%B")
        expense_year = expense_date.year

        # CHECK BUDGET
        budget = BudgetDetails.objects.filter(
            user=request.user,
            expensehead=expensehead,
            month=expense_month
        ).first()

        total_expense = ExpenseDetails.objects.filter(
            user=request.user,
            expensehead=expensehead,
            date__year=expense_year,
            date__month=expense_date.month
        ).aggregate(total=Sum("amount"))["total"] or 0

        if budget:

            budget_amount = float(budget.amount)
            remaining_budget = budget_amount - float(total_expense)

            if remaining_budget < 0:

                send_mail(
                    subject="⚠️ Budget Alert - Expense Exceeded",
                    message=f"""
Hi {request.user.first_name},

Your expenses for the category '{expensehead.name}' have exceeded your monthly budget.

Budget Amount : ₹{budget_amount}
Total Expense : ₹{total_expense}
Exceeded By : ₹{abs(remaining_budget)}

Please review your expenses in Finance Tracker.

Best Regards,
Finance Tracker Team
""",
                    from_email=None,
                    recipient_list=[request.user.email],
                    fail_silently=True
                )

                messages.warning(
                    request,
                    f"{expensehead.name} budget exceeded by ₹{abs(remaining_budget)}"
                )

            else:
                messages.success(
                    request,
                    f"₹{amount} added to {expensehead.name}. Remaining budget: ₹{remaining_budget}"
                )

        else:
            messages.info(
                request,
                f"₹{amount} expense added to {expensehead.name}. No budget set for {expense_month}."
            )

        return redirect("user:expensedetails")

    expenseheads = Expensehead.objects.all()

    return render(
        request,
        "Expensedetails.html",
        {
            "expensehead": expenseheads
        }
    )




def viewexpense(request):

    month = request.GET.get('month')

    # ✅ If month not selected, use current month
    if not month:
        month = datetime.now().month

    # Expense list filter
    expenses = ExpenseDetails.objects.filter(
        user=request.user,
        date__month=int(month)
    )

    # Pie Chart Data
    expense_data = expenses.values('expensehead__name').annotate(
        total_amount=Sum('amount')
    ).order_by('-total_amount')

    labels = [item['expensehead__name'] for item in expense_data]
    data = [float(item['total_amount']) for item in expense_data]

    # ✅ Total Expense
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # ✅ Total Categories
    category_count = expenses.values('expensehead').distinct().count()

    context = {
        "list": expenses,
        "selected_month": int(month),   # send month to html
        "labels": labels,
        "data": data,
        "total_expense": total_expense,
        "category_count": category_count
    }

    return render(request, "viewexpense.html", context)


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

    month_dict = {
        "1": "January",
        "2": "February",
        "3": "March",
        "4": "April",
        "5": "May",
        "6": "June",
        "7": "July",
        "8": "August",
        "9": "September",
        "10": "October",
        "11": "November",
        "12": "December"
    }

    month_number = request.GET.get('month')

    if not month_number:
        month_number = str(datetime.now().month)

    month_name = month_dict.get(month_number)

    # TOTAL INCOME
    total_income = IncomeDetails.objects.filter(
        user=request.user,
        date__month=int(month_number)
    ).aggregate(total=Sum('amount'))['total'] or 0


    total_income = IncomeDetails.objects.filter(
        user=request.user,
        date__month=int(month_number)
    ).aggregate(total=Sum('amount'))['total'] or 0


   # TOTAL INCOME
    total_income = IncomeDetails.objects.filter(
        user=request.user,
        date__month=int(month_number)
    ).aggregate(total=Sum("amount"))["total"] or 0


    # BUDGETS
    budgets = BudgetDetails.objects.filter(
        user=request.user,
        month=month_name
    )

    total_budget = budgets.aggregate(total=Sum("amount"))["total"] or 0


    # REMAINING AFTER BUDGET
    remaining_after_budget = total_income - total_budget


    total_exceeded = 0

    # CHECK BUDGET EXCEEDED
    for b in budgets:

        total_expense = ExpenseDetails.objects.filter(
            user=request.user,
            expensehead=b.expensehead,
            date__month=int(month_number)
        ).aggregate(total=Sum("amount"))["total"] or 0

        if total_expense > b.amount:
            total_exceeded += (total_expense - b.amount)


    # EXPENSE WITHOUT BUDGET
    budget_heads = budgets.values_list("expensehead_id", flat=True)

    non_budget_expense = ExpenseDetails.objects.filter(
        user=request.user,
        date__month=int(month_number)
    ).exclude(
        expensehead_id__in=budget_heads
    ).aggregate(total=Sum("amount"))["total"] or 0


    # FINAL REMAINING BALANCE
    final_remaining = remaining_after_budget - (total_exceeded + non_budget_expense)


    context = {
        "expensehead": Expensehead.objects.all(),
        "total_income": total_income,
        "total_budget": total_budget,
        "remaining_income": final_remaining,
        "selected_month": month_number
    }

    return render(request, "budgetdetails.html", context)





def viewbudget(request):

    # get month from dropdown
    month = request.GET.get('month')

    # if no month selected -> current month
    if not month:
        month = datetime.now().strftime("%B")   # January, February etc.

    # filter data
    v = BudgetDetails.objects.filter(
        user=request.user,
        month=month
    )

    # pie chart data
    labels = []
    amounts = []

    for i in v:
        labels.append(i.expensehead.name)
        amounts.append(float(i.amount))

    return render(
        request,
        "viewbudget.html",
        {
            "list": v,
            "selected_month": month,
            "labels": labels,
            "amounts": amounts
        }
    )


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







def overbudget(request, month):

    current_year = date.today().year

    # Convert month name to month number
    month_number = datetime.strptime(month, "%B").month


    # Group expenses by expense head
    grouped_expenses = ExpenseDetails.objects.filter(
        user=request.user,
        date__month=month_number,
        date__year=current_year
    ).values(
        'expensehead'
    ).annotate(
        total_amount=Sum('amount')
    )


    budget_data = BudgetDetails.objects.filter(
        user=request.user,
        month=month
    )


    overbudget_expenses = []


    for item in grouped_expenses:

        expensehead_id = item['expensehead']
        total_amount = float(item['total_amount'])

        expensehead_obj = Expensehead.objects.get(id=expensehead_id)

        budget = budget_data.filter(
            expensehead=expensehead_obj
        ).first()


        # 🔴 CASE 1 : No budget set
        if not budget:

            overbudget_expenses.append({
                "expensehead": expensehead_obj.name,
                "amount": total_amount,
                "budget": "Not Set",
                "over_by": total_amount
            })


        # 🔴 CASE 2 : Expense greater than budget
        elif total_amount > float(budget.amount):

            overbudget_expenses.append({
                "expensehead": expensehead_obj.name,
                "amount": total_amount,
                "budget": budget.amount,
                "over_by": total_amount - float(budget.amount)
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















