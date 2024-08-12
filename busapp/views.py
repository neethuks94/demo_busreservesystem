from datetime import datetime
from django.contrib import messages
from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import  Bus, Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return render(request, 'signin.html')

        
@login_required(login_url='signin')
def findbus(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        date_r = datetime.strptime(date_r,"%Y-%m-%d").date()
        year = date_r.strftime("%Y")
        month = date_r.strftime("%m")
        day = date_r.strftime("%d")
        bus_list = Bus.objects.filter(source=source_r, dest=dest_r, date__year=year, date__month=month, date__day=day)
        if bus_list:
            return render(request, 'list.html', locals())
        else:
            context['data'] = request.POST
            context["error"] = "No available Bus Schedule for entered Route and Date"
            return render(request, 'findbus.html', context)
    else:
        return render(request, 'findbus.html')


@login_required(login_url='signin')
def bookings(request):
    responseDic = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        seats_r = int(request.POST.get('no_seats'))
        bus = Bus.objects.get(id=id_r)
        if bus:
            if bus.rem > int(seats_r):
                name_r = bus.bus_name
                cost = int(seats_r) * bus.price
                source_r = bus.source
                dest_r = bus.dest
                nos_r = Decimal(bus.nos)
                price_r = bus.price
                date_r = bus.date
                time_r = bus.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                rem_r = bus.rem - seats_r
                Bus.objects.filter(id=id_r).update(rem=rem_r)
                book = Book.objects.create(name=username_r, email=email_r, userid=userid_r, bus_name=name_r,
                                           source=source_r, busid=id_r,
                                           dest=dest_r, price=cost, nos=seats_r, date=date_r, time=time_r,
                                           status='BOOKED')
                
                return render(request, 'bookings.html', locals())
            else:
                responseDic["error"] = "Sorry select fewer number of seats"
                return render(request, 'findbus.html', responseDic)
    else:
        return render(request, 'findbus.html')


@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        try:
            book = Book.objects.get(id=id_r)
            bus = Bus.objects.get(id=book.busid)
            rem_r = bus.rem + book.nos
            Bus.objects.filter(id=book.busid).update(rem=rem_r)
            Book.objects.filter(id=id_r).update(status='CANCELLED')
            Book.objects.filter(id=id_r).update(nos=0)
            messages.success(request, "Booked Bus has been cancelled successfully.")
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that bus"
            return render(request, 'booklist.html', context)
    else:
        return render(request, 'findbus.html')

def resetPassword(request):
    responseDic={}
    try:
        usern=request.POST['uname']
        recepient=request.POST['email']
        pwd=request.POST['password']
        try:
            user=User.objects.get(username=usern)
            if user is not None:
                user.set_password(pwd)
                user.save()
                responseDic['errmsg']="Password Reset Successfully"
                return render(request,"ResetPassword.html",responseDic)
        except Exception as e:
            print(e)
            responseDic["errmsg"]="email doesn't exist"
            return render(request,"ResetPassword.html",responseDic)

    except Exception as e:
        print(e)
        responseDic["errmsg"]="Failed to reset password"
        return render(request,"ResetPassword.html",responseDic)
def Resethome(request):
    return render(request,"Resetpassword.html")       
@login_required(login_url='signin')
def seebookings(request):
    id_r = request.user.id  
    book_list = Book.objects.filter(userid=id_r)   
    if book_list:  
        context = {'book_list': book_list}  
        return render(request, 'booklist.html', context)  
    else:  
        context = {"error": "Sorry no buses booked"} 
        return render(request, 'findbus.html', context)   


def signup(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')

        if User.objects.filter(username=name_r).exists() or User.objects.filter(email=email_r).exists():
            context['error']= "Username or email already exists."
            return render(request, 'signup.html',context)
  
        user = User.objects.create_user(username=name_r, email=email_r, password=password_r)
        if user:
            login(request, user)
            return render(request, 'thank.html')
        else:
            context["error"] = "Unable to create user. Please try again."
            return render(request, 'signup.html')
    else:
        return render(request, 'signup.html', context)



def signin(request):
    context = {}
    if request.method == 'POST':

        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            context["user"] = name_r
            context["id"] = request.user.id
            return render(request, 'success.html', context)
        
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'signin.html', context)
    

        
def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'signin.html', context)



