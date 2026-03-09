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