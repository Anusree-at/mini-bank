from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Userregister, History
from django.contrib.auth.models import User, auth
# Create your views here.

def userregistration(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        account_number = request.POST['account_number']
        adhar_number = request.POST['adhar_number']
        pan_card = request.POST['pan_card']
        pin = request.POST['pin']
        username = request.POST['username']
        password = request.POST['password']
        minimum_balance = int(request.POST['minimum_balance'])
        image = request.FILES['image']

        if minimum_balance < 1000:
            return render(request, 'userregister.html',{'minimum': "Amount is less than 1000"})

        if Userregister.objects.filter(account_number=account_number).exists():
            return render(request, 'userregister.html', {'message': "Account already exists"})
        else:
            data = Userregister.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, account_number=account_number, adhar_number=adhar_number, pan_card=pan_card, pin=pin, username=username, password=password, minimum_balance=minimum_balance, image=image, user_type="user")
            data.save()
            return redirect(Login)
    else:
        return render(request, 'userregister.html')

def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        admin_user = auth.authenticate(request, username=username, password=password)
        print(admin_user)
        if admin_user is not None and admin_user.is_staff:
            auth.login(request, admin_user)
            return redirect(bankprofile)
        data = auth.authenticate(username=username, password=password)
        if data is not None:
            auth.login(request, data)
            if data.user_type == "user":
                return redirect(userhome)
            elif data.user_type == "bank":
                return redirect(usercount)

        else:
            return HttpResponse("invalid credentials")
    else:
        return render(request, 'adminlogin.html')


def withdraw(request):
    if request.method == "POST":
        account_number = request.POST['accountnumber']
        amount = int(request.POST['amount'])
        data = Userregister.objects.get(account_number=account_number)
        if data is not None:
            if data.minimum_balance < 1000:
                return render(request, 'withdraw.html', {'with': "Can't withdraw money"})

            else:
                data.minimum_balance = data.minimum_balance - amount
                data.save()
                transaction = History.objects.create(user_id=data.id, details="debit", history_amount=amount)
                transaction.save()
                return render(request, 'withdraw.html', {'withdrew': "money has withdrawn"})
        else:
            return HttpResponse("Invalid Account Number")
    else:
        return render(request, 'withdraw.html')
def deposit(request):
    if request.method == "POST":
        account_number = request.POST['accountnumber']
        amount = int(request.POST['depositamount'])
        data = Userregister.objects.get(account_number=account_number)
        if data is not None:
            if amount < 200:
                return render(request, 'deposit.html', {'condition': "can't deposit amount under 200"})
            else:
                data.minimum_balance = data.minimum_balance + amount
                data.save()
                transaction = History.objects.create(user_id=data.id, details="credit", history_amount=amount)
                transaction.save()
                return render(request, 'deposit.html', {'deposit': "money has deposited"})
        else:
            return HttpResponse("Invalid Account Number")
    else:
        return render(request, 'deposit.html')

def balance(request):
    if request.method == "POST":
        account_number = request.POST['accountnumber']
        data = Userregister.objects.get(account_number=account_number)
        if data is not None:
            return render(request, 'useroptions.html', {'balance': data})
        else:
            return HttpResponse("Invalid Account number")
    else:
        return render(request, ' useroptions.html')


def adminoptions(request):
    if request.method == "POST":
        bankname = request.POST['bankname']
        IFSC = request.POST['IFSC']
        branch = request.POST['branch']
        username = request.POST['username']
        password = request.POST['password']
        data = Userregister.objects.create_user(bankname=bankname, IFSC=IFSC, branch=branch, username=username, password=password, user_type="bank")
        data.save()
        return redirect(bankprofile)
    else:
        return render(request, 'bankregister.html')

def bankprofile(request):
    data = Userregister.objects.filter(user_type="bank")
    return render(request, 'bankprofile.html', {'data': data})

def userhome(request):
    data = Userregister.objects.get(id=request.user.id)
    return render(request, 'userhome.html', {'id': data})
def usermore(request):
    data = Userregister.objects.get(id=request.user.id)
    return render(request, 'usermore.html', {'id': data})
def back(request):
    return redirect(userhome)
def usercount(request):
    count = Userregister.objects.filter(user_type="user").count()
    return render(request, 'bankhome.html', {'count': count})
def all_users(request):
    all = Userregister.objects.filter(user_type="user")
    return render(request, 'allusers.html', {'all': all})
def user_view(request, id):
    view = Userregister.objects.get(id=id)
    return render(request, 'user_view.html', {'view': view})
def history(request):
    data = History.objects.filter(user_id=request.user.id)
    return render(request, 'history.html', {'data': data})
def bankhistory(request,id):
    data = History.objects.filter(user_id=id)
    return render(request, 'bankhistory.html', {'data': data})
def edit(request):
    data=Userregister.objects.get(id=request.user.id)
    if request.method == "POST":
        data.first_name = request.POST['first_name']
        data.last_name = request.POST['last_name']
        data.email = request.POST['email']
        data.phone_number = request.POST['phone_number']
        data.account_number = request.POST['account_number']
        data.adhar_number = request.POST['adhar_number']
        data.pan_card = request.POST['pan_card']
        data.pin = request.POST['pin']
        data.username = request.POST['username']
        if 'image' in request.FILES:
            data.image = request.FILES['image']
        data.save()
        return redirect(userhome)
    else:
        return render(request, 'edit.html', {'data': data})

def log_out(request):
    auth.logout(request)
    return redirect(Login)
def search(request):

    if request.method == "POST":
        search_ = request.POST["search"]
        data = Userregister.objects.filter(first_name__icontains=search_)
        return render(request, 'allusers.html', {'data': data})
    else:
        return render(request, 'allusers.html')
