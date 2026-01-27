from django.http import HttpResponse
from django.shortcuts import render

from app_core.models import Category, District, Expensehead, Incomehead,Location
from app_dashboard.models import UserRegistration

# Create your views here.
def dist(request):
    if request.method=='POST':
        name=request.POST.get('name')
        print("success ")
        if District.objects.filter(name = name ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/dist/';</script>")
        dist=District()
        dist.name=name
        dist.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/dist/';</script>")
    else:
        return render(request,"district.html")
    
def location(request):
    if request.method=='POST':
        name=request.POST.get('name')
        dis=request.POST.get('name1')
        print("success ")
        if Location.objects.filter(name = name,dis=dis ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/location/';</script>")
        loc=Location()
        loc.name=name
        loc.dis=District.objects.get(id = dis)
        loc.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/location/';</script>")
    else:
        v=District.objects.all()
        return render(request,"location.html",{"list":v})
    
def viewdis(request):
    v=District.objects.all()
    return render(request,"viewdis.html",{"list":v})

def deletedist(request,id):
    d=District.objects.get(id=id)
    d.delete()
    return HttpResponse("<script>alert('Deleted Successfully');window.location='/core/viewdis/';</script>")

def editdis(request,id):
   s=District.objects.get(id=id)
#    return HttpResponse(s)
   if request.method=='POST' :
        print ("submission successfull")
        name= request.POST.get('name')
        print (name)
        if District.objects.filter(name=name).exists():
            return HttpResponse("<script>alert('Already Exists');window.location='/core/viewdis/';</script>")
        
        s.name=name
        s.save()
        return HttpResponse("<script>alert('Edited Successfully');window.location='/core/viewdis/';</script>" )
   else:
        
#  return HttpResponse("<script>alert('Deleted Successfully');window.location='/home/vcat';</script>" )
    return render(request,'editdis.html',{'editdis':s})
   
def viewloc(request):
    v=Location.objects.all()
    return render(request,"viewloc.html",{"list":v})

def deleteloc(request,id):
    d=Location.objects.get(id=id)
    d.delete()
    return HttpResponse("<script>alert('Deleted Successfully');window.location='/core/viewloc/';</script>")

def locationup(request,id):
    up = Location.objects.get(id=id)
    if request.method=="POST":
        name = request.POST.get('name')
        dis = request.POST.get('dis')
        # return HttpResponse(dis)
        if Location.objects.filter( name=name, dis=dis ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='';</script>")
        up.name = name
        up.dis = District.objects.get(id = dis)
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/core/viewloc/';</script>")
    list=District.objects.all()
    return render(request,"editloc.html",{"locationv":up,"list":list})

def category(request): 
    if request.method=='POST':
        name=request.POST.get('name')
        description=request.POST.get('description')
        print("success ")
        if Category.objects.filter(name = name ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/category/';</script>")
        cat=Category()
        cat.name=name
        cat.description=description
        if len(request.FILES) !=0:
            img = request.FILES['img']
        else:
            img = 'Images/default.jpg'
        cat.img=img
        cat.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/category/';</script>")
    else:
        return render(request,"category.html")

def viewcat(request):
    cv=Category.objects.all()
    return render(request,"viewcat.html",{"list":cv})

def deletecat(request,name):
    d=Category.objects.get(id=name)
    d.delete()
    return HttpResponse("<script>alert('Deleted Successfully');window.location='/core/viewcat/';</script>")

def cateup(request,name):
    up = Category.objects.get(id=name)
    if request.method=="POST":
        cname = request.POST.get('name')
        desc = request.POST.get('description')
        img = request.FILES.get('img')

        if Category.objects.filter(name=cname).exclude(id=name).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/category/';</script>")
        up.name=cname
        up.description=desc
        if img:
            up.img=img
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/core/viewcat/';</script>")
    return render(request,"editcat.html",{"catv":up})


def incomehead(request):
    if request.method=='POST':
        namefield=request.POST.get('namefield')
        print("success ")
        if Incomehead.objects.filter(namefield = namefield ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/incomehead/';</script>")
        inc=Incomehead()
        inc.namefield=namefield
        inc.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/incomehead/';</script>")
    else:
        return render(request,"incomehead.html",{"incomehead":Incomehead.objects.all()})
    

def viewincome(request):
    iv=Incomehead.objects.all()
    return render(request,"viewincome.html",{"list":iv})

def delincome(request,id):
    d=Incomehead.objects.get(id=id)
    d.delete()
    return HttpResponse("<script>alert('Deleted Successfully');window.location='/core/viewincome/';</script>")

def editincome(request,id):
    up = Incomehead.objects.get(id=id)
    if request.method=="POST":
        namefield = request.POST.get('namefield')
        if Incomehead.objects.filter(namefield=namefield).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/incomehead/';</script>")
        up.namefield=namefield
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/core/viewincome/';</script>")
    return render(request,"editincome.html",{"editincome":up})


def viewregistration(request):
    v=UserRegistration.objects.all()
    return render(request,"viewregistration.html",{"list":v})

def expensehead(request):
    if request.method=='POST':
        name=request.POST.get('name')
        description=request.POST.get('description')

        if Expensehead.objects.filter(name = name, description=description).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/expensehead/';</script>")
        exp=Expensehead()
        exp.name=name
        exp.description=description
        exp.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/expensehead/';</script>")
    else:
        return render(request,"expensehead.html",{"expensehead":Expensehead.objects.all()})
    
def viewexpense(request):
    v=Expensehead.objects.all()
    return render(request,"viewexpenseh.html",{"list":v})

def deleteexpense(request,id):
    d=Expensehead.objects.get(id=id)
    d.delete()
    return HttpResponse("<script>alert('Deleted Successfully');window.location='/core/viewexpense/';</script>")

def editexpense(request,id):
    up = Expensehead.objects.get(id=id)
    if request.method=="POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        if Expensehead.objects.filter(name=name, description=description).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/expensehead/';</script>")
        up.name=name
        up.description=description
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/core/viewexpense/';</script>")
    return render(request,"editexpenseh.html",{"editexpense":up})