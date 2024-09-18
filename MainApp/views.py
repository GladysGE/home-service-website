from django.shortcuts import render,redirect, get_object_or_404
from MainApp.models import Add_Categorydb,Add_Servicedb,ServiceTypedb,State,City, Service
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from WebApp.models import ContactDb,BookingDb
from django.http import JsonResponse

# Create your views here.
def index_page(req):
    return render(req,"index.html")

def add_category(req):
    return render(req,"Add_Category.html")
def save_category(request):
    if request.method=="POST":
        cn=request.POST.get('cname')
        cd = request.POST.get('cdesc')
        img=request.FILES['image']
    obj=Add_Categorydb(Category_Name=cn,Category_Image=img,Description=cd)
    obj.save()
    messages.success(request, "Category Added successfully")
    return redirect(add_category)
def display_category(req):
    data = Add_Categorydb.objects.all()
    return render(req,"Display_Category.html",{'data':data})
def edit_category(req,c_id):
    data=Add_Categorydb.objects.get(id=c_id)
    return render(req,"Edit_Category.html",{'data':data})
def update_category(req,cid):
    if req.method=="POST":
        name=req.POST.get('cname')
        desc = req.POST.get('cdesc')
    try:
        img=req.FILES['image']
        fs=FileSystemStorage()
        file=fs.save(img.name,img)
    except MultiValueDictKeyError:
        file=Add_Categorydb.objects.get(id=cid).Category_Image
    Add_Categorydb.objects.filter(id=cid).update(Category_Name=name,Category_Image=file,Description=desc)
    return redirect(display_category)
def delete_category(request,c_id):
    data=Add_Categorydb.objects.filter(id=c_id)
    data.delete()
    messages.warning(request, "Deleted")
    return redirect(display_category)

def login_page(request):
    return render(request,"Admin_Login.html")
def admin_login(request):
    if request.method=="POST":
        un=request.POST.get('username')
        pwd=request.POST.get('pass')
        if User.objects.filter(username__contains=un).exists():
            a=authenticate(username=un,password=pwd)
            if a is not None:
                login(request,a)
                request.session['username']=un
                request.session['password']=pwd
                messages.success(request,"Login successfully")
                return redirect(index_page)
            else:
                messages.warning(request,"Invalid username or password")
                return redirect(login_page)

        else:
            messages.warning(request, "User not found")
            return redirect(login_page)
def admin_logout(request):
    del request.session['username']
    del request.session['password']
    messages.success(request,"Thank you..")
    return redirect(login_page)
def add_services(request):
    cat=Add_Categorydb.objects.all()
    return render(request,"Add_Service.html",{'cat':cat})
def save_services(request):
    if request.method=="POST":
        cn=request.POST.get('scate')
        sn=request.POST.get('sname')
        price=request.POST.get('price')
        discount=request.POST.get('sdiscount')
        dtype=request.POST.get('stype')
        desc=request.POST.get('sdesc')
        img=request.FILES['image']
        inc=request.POST.get('included')
        exc=request.POST.get('excluded')
    obj=Add_Servicedb(Category=cn,Service_Name=sn,Price=price,Discount=discount,Discount_Type=dtype,Description=desc,Service_Image=img,Included=inc,Excluded=exc)
    obj.save()
    messages.success(request, "Service Added Successfully")
    return redirect(add_services)
def display_services(request):
    data=Add_Servicedb.objects.all()
    return render(request,"Display_Service.html",{'data':data})
def edit_service(request,sid):
    data=Add_Servicedb.objects.get(id=sid)
    cat=Add_Categorydb.objects.all()
    return render(request,"Edit_Service.html",{'data':data,'cat':cat})
def update_service(request,s_id):
    if request.method=="POST":
        cn = request.POST.get('scate')
        sn = request.POST.get('sname')
        price = request.POST.get('price')
        discount = request.POST.get('sdiscount')
        dtype = request.POST.get('stype')
        desc = request.POST.get('sdesc')
        inc = request.POST.get('included')
        exc = request.POST.get('excluded')
    try:
        img=request.FILES['image']
        fs=FileSystemStorage()
        file=fs.save(img.name,img)
    except MultiValueDictKeyError:
        file=Add_Servicedb.objects.get(id=s_id).Service_Image
    Add_Servicedb.objects.filter(id=s_id).update(Category=cn,Service_Name=sn,Price=price,Discount=discount,Discount_Type=dtype,Description=desc,Included=inc,Excluded=exc,Service_Image=file)
    return redirect(display_services)
def delete_service(request,sid):
    data=Add_Servicedb.objects.filter(id=sid)
    data.delete()
    messages.warning(request, "Deleted")
    return redirect(display_services)
def display_contact(request):
    data=ContactDb.objects.all()
    return render(request,"Display_contacts.html",{'data':data})
def service_type_page(request):
    service=Add_Servicedb.objects.all()
    return render(request,"Add_Service_Type.html",{'service':service})
def save_service_type(request):
    if request.method=="POST":
        sn=request.POST.get('sname')
        st=request.POST.get('stype')
        price=request.POST.get('price')

    obj=ServiceTypedb(Service_Name=sn,Service_Type=st,Price=price)
    obj.save()
    messages.success(request, "Service Added Successfully")
    return redirect(service_type_page)

def display_service_type(request):
    data=ServiceTypedb.objects.all()
    return render(request,"Display_Service_Type.html",{'data':data})
def add_state(request):
    return render(request,"Add_State.html")
def save_state(request):
    if request.method=="POST":
        sn=request.POST.get('sname')
    obj=State(name=sn)
    obj.save()
    messages.success(request, "State Added successfully")
    return redirect(add_state)
def add_city(request):
    state = State.objects.all()
    return render(request, "Add_City.html", {'state': state})
def save_city(request):
    if request.method=="POST":
        sn=request.POST.get('sname')
        cn = request.POST.get('cname')
    obj=City(cname=cn,sname=sn)
    obj.save()
    messages.success(request, "City Added successfully")
    return redirect(add_city)
def service(request):
    city = City.objects.all()
    service=Add_Categorydb.objects.all()
    return render(request, "Service.html", {'city': city,'service':service})
def submit_service(request):
    if request.method == "POST":
        name = request.POST.get('scate')
        city = request.POST.get('city')
    obj = Service(name=name, city=city)
    obj.save()
    return redirect(service)
def display_booking(request):
    data=BookingDb.objects.all()
    return render(request,"Booking_Display.html",{'data':data})