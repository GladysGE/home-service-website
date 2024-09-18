from django.shortcuts import render,redirect,get_object_or_404
from MainApp.models import Add_Categorydb,Add_Servicedb,ServiceTypedb,State,City,Service
from WebApp.models import ContactDb,RegisterDb,CartDb,BookingDb
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import razorpay
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
def home_page(request):
    cat=Add_Categorydb.objects.all()
    return render(request,"Home.html",{'cat':cat})
def about_page(request):
    return render(request,"About_Us.html")
def contact_page(request):
    return render(request,"Contact.html")
def contact_save(request):
    if request.method=="POST":
        fullname = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
    obj=ContactDb(FullName=fullname,Email=email,Subject=subject,Message=message)
    obj.save()
    messages.success(request, "Data Submitted Contact You Soon")
    return redirect(contact_page)
def portfolio_page(request):
    return render(request,"Portfolio.html")
def blog_page(request):
    return render(request,"Blog.html")
def filtered_service(request,cat_name):
    data=Add_Servicedb.objects.filter(Category=cat_name)
    return render(request,"Filtered_Service.html",{'data':data})

def single_service(request,sid):
    data=Add_Servicedb.objects.get(id=sid)
    stype=ServiceTypedb.objects.filter()
    inclusions = data.Included.split(',') if data.Included else []
    exclusions = data.Excluded.split(',') if data.Excluded else []
    return render(request,"Single_Service.html",{'data':data,'stype':stype,'inclusions':inclusions,'exclusions':exclusions})
def registration_page(request):
    return render(request,"Register.html")
def registration_save(request):
    if request.method=="POST":
        un=request.POST.get('uname')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
    obj=RegisterDb(Username=un,Email=email,Password=pass1,Confirm_Password=pass2)
    subject = 'Welcome to Our HomeCarePros world'
    message = f'Hi {obj.Username} Thank You for registering with us! Your Account has been successfully created.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [obj.Email, ]
    send_mail(subject, message, email_from, recipient_list)
    if RegisterDb.objects.filter(Username=un).exists():
      messages.warning(request, "User already exists...!")
    elif RegisterDb.objects.filter(Email=email).exists():
        messages.warning(request, "Email already exists...!")
    obj.save()
    messages.success(request, "Registered Successfully")
    return redirect(registration_page)
def user_login(request):
    if request.method=="POST":
        un=request.POST.get('uname')
        pwd=request.POST.get('password')
        if RegisterDb.objects.filter(Username=un,Password=pwd).exists():
            request.session['Username'] = un
            request.session['Password'] = pwd
            messages.success(request, "WELCOME")
            return redirect(home_page)
        else:
            messages.warning(request,"INVALID USERNAME OR PASSWORD")
            return redirect(registration_page)
    else:
        messages.warning(request, "INVALID USERNAME OR PASSWORD")
        return redirect(registration_page)

def user_logout(request):
    del request.session['Username']
    del request.session['Password']
    messages.success(request,"Thank you..")
    return redirect(registration_page)
def cart_page(request):
    data=CartDb.objects.filter(Username=request.session['Username'])
    total_price=0
    for i in data:
        total_price=total_price+i.Total_Price

    return render(request,"Cart_Page.html",{'data':data,'total_price':total_price})
def save_cart(request):
    if request.method=="POST":
        discount = request.POST.get('discount')
        dtype=request.POST.get('stype')
        tprice = request.POST.get('totalprice')
        uname= request.POST.get('uname')
        sname = request.POST.get('sname')
        if CartDb.objects.filter(Username=uname).exists():
            messages.error(request, "You can only add one service to the cart.")
            return redirect('cart_page')

        obj = CartDb(Discount=discount,Discount_Type=dtype, Total_Price=tprice, Username=uname, Service_Name=sname)
        obj.save()
        return redirect('home_page')
def delete_item(request,item_id):
    data=CartDb.objects.filter(id=item_id)
    data.delete()
    return redirect(cart_page)
def our_services(request):
    cat = Add_Categorydb.objects.all()
    states = State.objects.all()
    data = {}

    # Create a dictionary structure to hold the state and city data
    for state in states:
        cities = City.objects.filter(sname=state.name)
        city_data = {}
        for city in cities:
            services = Service.objects.filter(city=city.cname)
            service_names = [service.name for service in services]
            city_data[city.cname] = service_names
        data[state.name] = city_data

    services = []
    if request.method == 'POST':
        selected_state = request.POST.get('state')
        selected_city = request.POST.get('city')

        if selected_state and selected_city:
            services = Service.objects.filter(city=selected_city)

    context = {
        'data': data,
        'states': states,
        'services': services,
        'cat': cat,
    }
    return render(request, 'Our_Services.html', context)
def search_service(request):
    return render(request,"search_service.html")
def booking_page(request):
    data=CartDb.objects.filter(Username=request.session['Username'])
    total_price = 0
    for i in data:
        total_price = total_price + i.Total_Price
    return render(request,"Booking.html",{'data':data,'total_price':total_price})
def booking_save(request):
    if request.method == 'POST':
        uname=request.POST.get('uname')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        date = request.POST.get('date')
        hours = request.POST.get('hours')
        minutes = request.POST.get('minutes')
        ampm = request.POST.get('ampm')
        address=request.POST.get('address')
        complaint_image = request.FILES['complaint-image']
        description = request.POST.get('description')
        tprice = request.POST.get('total_price')
        # Process time into 24-hour format
        hours = int(hours)
        minutes = int(minutes)
        if ampm == 'PM' and hours != 12:
            hours += 12
        elif ampm == 'AM' and hours == 12:
            hours = 0

        time = datetime.strptime(f"{hours}:{minutes}", "%H:%M").time()

        # Save the complaint image if provided
        if complaint_image:
            fs = FileSystemStorage()
            filename = fs.save(complaint_image.name, complaint_image)
            complaint_image_url = fs.url(filename)
        else:
            complaint_image_url = None

        # Here you would save the data to your database or process it as needed
        # For example:
        obj=BookingDb(Name=uname,Phone=phone,Email=email,Date=date, Time=time,Address=address, Complaint_image=complaint_image_url, Description=description,Total_Price=tprice)
        obj.save()
        subject = 'Welcome to Our HomeCarePros world'
        message = f'Dear {obj.Name} Your Appointment Has Been Scheduled. Please find the booking details below\nDate of Appointment:{obj.Date}\n...\n...\n...\nSlot: {obj.Time}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [obj.Email, ]
        send_mail(subject, message, email_from, recipient_list)
        return redirect(payment_page)

        # Redirect to a success page or
def payment_page(request):
    customer=BookingDb.objects.order_by('-id').first()
    payy=customer.Total_Price
    amount=int(payy*100)
    payy_str=str(amount)
    for i in payy_str:
        print(i)
    if request.method=="POST":
        order_currency="INR"
        client=razorpay.Client(auth=('rzp_test_Vp4OL3XiUZPcuu','Nuhcu0efjBTOjYEMfQWNP0Ii'))
        payment=client.order.create({'amount':amount,'currency':order_currency,'payment_capture':'1'})
    return render(request,"Payment_Page.html",{'customer':customer,'payy_str':payy_str})
def demo(request):
    return render(request,"demo.html")