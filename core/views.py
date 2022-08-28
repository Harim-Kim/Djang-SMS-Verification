from django.shortcuts import render, redirect
from .forms import UserCreationForm, VerifyForm, reverifyForm
from django.contrib.auth.decorators import login_required
from . import verify
from .decorators import verification_required
from . import models
# Create your views here.


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # user_phone = models.AuthSmsSignIn.objects.filter(phone_number=form.cleaned_data.get('phone'))
            # if user_phone:
            form.save()
            # verify.send(form.cleaned_data.get('phone'))
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def signup_phone_verify_page(request):
    if request.method == "POST":
        form = reverifyForm(request.POST)
        print("1")
        print(form.is_valid())
        if form.is_valid():

            phone = form.cleaned_data.get('phone')
            verify.send(phone)
            form = VerifyForm()
            form.set_phone(phone)
            return render(request, 'phone_verify.html', {"form":form,"phone":phone})
    else:
        form = reverifyForm()
    return render(request, 'signup_phone_verify.html',{'form':form})

def phone_verify(request):
    message = {}
    print("@")
    if request.method == "POST":
        # form = VerifyForm(request.POST)
        # if form.is_valid():
        #     code = form.cleaned_data.get('code')
        #     phone = request.POST['phone']
        print(request.POST)
        code = request.POST['code']
        phone = request.POST['phone']
        result, status = verify.check(phone, code)
        if result:
            # auth = models.AuthSmsSignIn(phone_number=phone, auth_number=code)
            # auth.save()
            return redirect('signup')
        else:
            message = {"message":"failed verification"}

    # form =
    return render(request, 'verify.html', {'form': VerifyForm(), 'message': message})

@login_required
def verify_code(request):
    message = {}
    result = False
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            result, status = verify.check(request.user.phone, code)
            # print(result,status)
            if result and status == 200:
                request.user.is_verified = True
                request.user.save()
            elif status == 404:
                message["message"] = "you need re-verification, code already expired"
        if result:
            return redirect('index')

    else:
        form = VerifyForm()
    return render(request, 'verify.html', {'form': form, 'message': message} )

@login_required
def reverify(request):
    if request.method == "GET":
        form = reverifyForm()
        return render(request, 'reverify.html', {'form':form})
    elif request.method == "POST":
        form = reverifyForm(request.POST)
        # print(form)
        print(form.is_valid())
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            verify.send(phone)
            return redirect('/verify.html')
    return render(request, 'reverify.html')