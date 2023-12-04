from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.conf import settings

# Create your views here.
def is_customer(user):
    
    return user.groups.filter(name='CUSTOMER').exists()
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')
   
def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('home')
    else:
        return redirect('admin-dashboard')
@login_required(login_url='adminlogin')    
def add(request):
    return render(request,'voyage/admin_add_hotels.html')
@login_required(login_url='adminlogin')
def admin_hotels_view(request):
    hotels=models.Hotel.objects.all()
    return render(request,'voyage/admin_hotels.html',{'hotels':hotels})
@login_required(login_url='adminlogin')
def admin_voitures_view(request):
    voitures=models.Voiture.objects.all()
    return render(request,'voyage/admin_voiture.html',{'voitures':voitures})
@login_required(login_url='adminlogin')
def view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'voyage/view_customer.html',{'customers':customers})    
@login_required(login_url='adminlogin')
def admin_add_hotel_view(request):
    hotelForm=forms.HotelForm()
    if request.method=='POST':
        hotelForm=forms.HotelForm(request.POST, request.FILES)
        if hotelForm.is_valid():
            hotelForm.save()
        return HttpResponseRedirect('hotels')
    return render(request,'voyage/admin_add_hotels.html',{'hotelForm':hotelForm})
def delete_hotel_view(request,pk):
    hotel=models.Hotel.objects.get(id=pk)
    hotel.delete()
    return redirect('hotels')
def update_hotel_view(request,pk):
    hotel=models.Hotel.objects.get(id=pk)
    hotelForm=forms.HotelForm(instance=hotel)
    if request.method=='POST':
        hotelForm=forms.HotelForm(request.POST,request.FILES,instance=hotel)
        if hotelForm.is_valid():
            hotelForm.save()
            return redirect('hotels')
    return render(request,'voyage/admin_update_hotel.html',{'hotelForm':hotelForm})
@login_required(login_url='adminlogin')
def admin_add_voiture_view(request):
    voitureForm=forms.VoitureForm()
    if request.method=='POST':
        voitureForm=forms.VoitureForm(request.POST, request.FILES)
        if voitureForm.is_valid():
            voitureForm.save()
        return HttpResponseRedirect('voitures')
    return render(request,'voyage/admin_add_voiture.html',{'voitureForm':voitureForm})
@login_required(login_url='adminlogin')
def update_voiture_view(request,pk):
    voiture=models.Voiture.objects.get(id=pk)
    voitureForm=forms.VoitureForm(instance=voiture)
    if request.method=='POST':
        voitureForm=forms.VoitureForm(request.POST,request.FILES,instance=voiture)
        if voitureForm.is_valid():
            voitureForm.save()
            return redirect('voitures')
    return render(request,'voyage/admin_update_voiture.html',{'voitureForm':voitureForm})
def delete_voiture_view(request,pk):
    voiture=models.Voiture.objects.get(id=pk)
    voiture.delete()
    return redirect('voitures')
def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('login')
    return render(request,'voyage/signup.html',context=mydict)

def customer_home_view(request):
    hotels=models.Hotel.objects.all()
    voitures=models.Voiture.objects.all()
    if 'hotel_ids' in request.COOKIES:
        hotel_ids = request.COOKIES['hotel_ids']
        counter=hotel_ids.split('|')
        hotel_count_in_cart=len(set(counter))
    else:
        hotel_count_in_cart=0
    if 'voiture_ids' in request.COOKIES:
        voiture_ids = request.COOKIES['voiture_ids']
        counter=voiture_ids.split('|')
        voiture_count_in_cart=len(set(counter))
    else:
        voiture_count_in_cart=0    
    return render(request,'voyage/customer_home.html',{'hotels':hotels,'voitures':voitures,' voiture_count_in_cart': voiture_count_in_cart,'hotel_count_in_cart':hotel_count_in_cart})


  

def delete_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('view-customer')



def update_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('view-customer')
    return render(request,'voyage/admin_update_customer.html',context=mydict)

@login_required(login_url='login')
@user_passes_test(is_customer)
def my_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'voyage/my_profile.html',{'customer':customer})
@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    # for cards on dashboard
    customercount=models.Customer.objects.all().count()
    hotelscount=models.Hotel.objects.all().count()
    

   

    mydict={
    'customercount':customercount,
    ' hotelscount': hotelscount,
  
    }
    return render(request,'voyage/admin_dashboard.html',context=mydict)

def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    hotels=models.Hotel.objects.all().filter(name__icontains=query)
    if 'hotel_ids' in request.COOKIES:
        hotel_ids = request.COOKIES['hotel_ids']
        counter=hotel_ids.split('|')
        hotel_count_in_cart=len(set(counter))
    else:
        hotel_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'voyage/customer_home.html',{'hotels':hotels,'word':word,'hotel_count_in_cart':hotel_count_in_cart})
    return render(request,'voyage/customer_home.html',{'hotels':hotels,'word':word,'hotel_count_in_cart':hotel_count_in_cart})



def delete_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    order.delete()
    return redirect('admin-view-booking')

# for changing status of order (pending,delivered...)

def update_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    orderForm=forms.OrderForm(instance=order)
    if request.method=='POST':
        orderForm=forms.OrderForm(request.POST,instance=order)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('admin-view-booking')
    return render(request,'voyage/update_order.html',{'orderForm':orderForm})

def add_to_cart_view(request,pk):
    hotels=models.Hotel.objects.all()

    #for cart counter, fetching products ids added by customer from cookies
    if 'hotel_ids' in request.COOKIES:
        hotel_ids = request.COOKIES['hotel_ids']
        counter=hotel_ids.split('|')
        hotel_count_in_cart=len(set(counter))
    else:
        hotel_count_in_cart=1

    response = render(request, 'voyage/customer_home.html',{'hotels':hotels,'hotel_count_in_cart':hotel_count_in_cart})

    #adding product id to cookies
    if 'hotel_ids' in request.COOKIES:
        hotel_ids = request.COOKIES['hotel_ids']
        if hotel_ids=="":
            hotel_ids=str(pk)
        else:
            hotel_ids=hotel_ids+"|"+str(pk)
        response.set_cookie('hotel_ids', hotel_ids)
    else:
        response.set_cookie('hotel_ids', pk)

    hotel=models.Hotel.objects.get(id=pk)
    messages.info(request, hotel.name + ' added to cart successfully!')

    return response

def admin_view_order_view(request):
    orders=models.Orders.objects.all()
    ordered_hotels=[]
    ordered_bys=[]
    for order in orders:
        ordered_hotel=models.Hotel.objects.all().filter(id=order.hotel.id)
        ordered_by=models.Customer.objects.all().filter(id = order.customer.id)
        ordered_hotels.append(ordered_hotel)
        ordered_bys.append(ordered_by)
    return render(request,'voyage/admin_view_order.html',{'data':zip(ordered_hotels,ordered_bys,orders)})
# for checkout of cart
def cart_view(request):
    #for cart counter
    if 'hotel_ids' in request.COOKIES:
        hotel_ids = request.COOKIES['hotel_ids']
        counter=hotel_ids.split('|')
        hotel_count_in_cart=len(set(counter))
    else:
        hotel_count_in_cart=0

    # fetching product details from db whose id is present in cookie
    hotels=None
    total=0
    if 'hotel_ids' in request.COOKIES:
        hotel_ids = request.COOKIES['hotel_ids']
        if hotel_ids != "":
            hotel_id_in_cart=hotel_ids.split('|')
            hotels=models.Hotel.objects.all().filter(id__in = hotel_id_in_cart)

            #for total price shown in cart
            for p in hotels:
                total=total+p.prix
    return render(request,'voyage/cart.html',{'hotels':hotels,'hotel_count_in_cart':hotel_count_in_cart})


def remove_from_cart_view(request,pk):
    #for counter in cart
    if 'hotel_ids' in request.COOKIES:
        hotel_ids = request.COOKIES['hotel_ids']
        counter=hotel_ids.split('|')
        hotel_count_in_cart=len(set(counter))
    else:
        hotel_count_in_cart=0

    # removing product id from cookie
    total=0
    if 'hotel_ids' in request.COOKIES:
        hotel_ids = request.COOKIES['hotel_ids']
        hotel_id_in_cart=hotel_ids.split('|')
        hotel_id_in_cart=list(set(hotel_id_in_cart))
        hotel_id_in_cart.remove(str(pk))
        hotels=models.Hotel.objects.all().filter(id__in = hotel_id_in_cart)
        #for total price shown in cart after removing product
        for p in hotels:
            total=total+p.prix

        #  for update coookie value after removing product id in cart
        value=""
        for i in range(len(hotel_id_in_cart)):
            if i==0:
                value=value+hotel_id_in_cart[0]
            else:
                value=value+"|"+hotel_id_in_cart[i]
        response = render(request, 'voyage/cart.html',{'hotels':hotels,'hotel_count_in_cart':hotel_count_in_cart})
        if value=="":
            response.delete_cookie('hotel_ids')
        response.set_cookie('hotel_ids',value)
        return response
def my_order_view(request):
    
    customer=models.Customer.objects.get(user_id=request.user.id)
    orders=models.Orders.objects.all().filter(customer_id = customer)
    ordered_hotels=[]
    for order in orders:
        ordered_hotels=models.Hotel.objects.all().filter(id=order.hotel.id)
        ordered_hotels.append(ordered_hotels)

    return render(request,'voyage/my_order.html',{'data':zip(ordered_hotels,orders)})
def edit_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('my-profile')
    return render(request,'voyage/edit_profile.html',context=mydict)


