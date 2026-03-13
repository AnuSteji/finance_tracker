from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout


from app_core.models import Location
from app_dashboard.models import UserRegistration
from financetracker.users.models import User
from django.core.mail import send_mail
from django.db.models import Sum
from app_user.models import IncomeDetails, ExpenseDetails
import xlwt


# Create your views here.

@never_cache
@login_required(login_url='/loginf/')
def admindashboard(request):
    return render(request, "Admintemplate.html")


def guestdashboard(request):
    return render(request, "Guesttemplate.html")


def loginf (request):
    if request.method=='POST':
        Username= request.POST.get('username')
        Password= request.POST.get('password') 

        user=authenticate(request, username=Username, password=Password)
        if user is not None:
            if user.role=='Admin':
                login(request, user)
                return HttpResponse("<script>alert('Login Successful');window.location='/admindashboard/';</script>")
            elif user.role=='User':
                login(request, user)
                return HttpResponse("<script>alert('Login Successful');window.location='/userdashboard/';</script>")
            else:
                return HttpResponse("<script>alert('Login Failed');window.location='/loginf/';</script>")
        else:
            return HttpResponse("<script>alert('Login Failed');window.location='/loginf/';</script>")        

    else:
        return render(request,"login.html")
    

def userregistration(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        contact=request.POST.get('contact')
        img=request.FILES.get('img')
        username=request.POST.get('username')
        password=request.POST.get('password')
        address=request.POST.get('address')
        location=request.POST.get('location')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return redirect('dashboard:userregistration')

        if User.objects.filter(username=username,email=email).exists():
            return HttpResponse("<script>alert('User already exists');window.location='/userregistration/';</script>")
        
        u=User()
        u.name=name
        u.email=email
        u.username=username
        u.set_password(password)
        u.role="User"
        u.save()

        ur=UserRegistration()
        ur.contact=contact
        if len(request.FILES) !=0:
            img = request.FILES['img']
        else:
            img = 'Images/default.jpg'
        ur.img=img
        ur.address=address
        ur.user=User.objects.get(username=username)
        ur.location=Location.objects.get(id=location)
        ur.save()
        send_mail(subject='🎉 Welcome to Finance Tracker!',message=f'Hi {name},Your registration was successful!Welcome to Finance Tracker. We’re excited to help you manage your expenses and budgets efficiently.You can now log in and start tracking your finances.Thank you for joining us!Best Regards,Finance Tracker Team',from_email=None,recipient_list=[email])
        return HttpResponse("<script>alert('User Registered Successfully');window.location='/loginf/';</script>")
    else:
        v=Location.objects.all()
        return render(request,"userregistration.html",{"list":v})
    
@never_cache
@login_required(login_url='/loginf/')    
def userdashboard(request):
    return render(request, "Usertemplate.html")

def logout_view(request):
    logout(request)
    return HttpResponse(
        "<script>alert('Logged out successfully');window.location='/loginf/';</script>"
    )

def about(request):
    return render(request, "about.html")

def services(request):
    return render(request, "services.html")

@login_required(login_url='/loginf/')
def admin_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    income_list = IncomeDetails.objects.all()
    expense_list = ExpenseDetails.objects.all()

    if start_date and end_date:
        income_list = income_list.filter(date__range=[start_date, end_date])
        expense_list = expense_list.filter(date__range=[start_date, end_date])

    total_income = income_list.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expense_list.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'income_list': income_list,
        'expense_list': expense_list,
        'total_income': float(total_income),
        'total_expense': float(total_expense),
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, "admin_report.html", context)

@login_required(login_url='/loginf/')
def export_report_excel(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    income_list = IncomeDetails.objects.all()
    expense_list = ExpenseDetails.objects.all()

    if start_date and end_date:
        income_list = income_list.filter(date__range=[start_date, end_date])
        expense_list = expense_list.filter(date__range=[start_date, end_date])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Finance_Report.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Income and Expenses')

    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Type', 'Category/Head', 'Date', 'Amount']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    for row in income_list:
        row_num += 1
        ws.write(row_num, 0, 'Income', font_style)
        ws.write(row_num, 1, row.incomehead.namefield, font_style)
        ws.write(row_num, 2, str(row.date), font_style)
        ws.write(row_num, 3, float(row.amount), font_style)

    for row in expense_list:
        row_num += 1
        ws.write(row_num, 0, 'Expense', font_style)
        ws.write(row_num, 1, row.expensehead.name, font_style)
        ws.write(row_num, 2, str(row.date), font_style)
        ws.write(row_num, 3, float(row.amount), font_style)

    wb.save(response)
    return response