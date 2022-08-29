from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserCreationForm, VerifyForm, reverifyForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login, logout
from django.template import RequestContext
from django.contrib.auth.hashers import make_password, check_password
from . import verify
from .decorators import verification_required
from . import models
from . import my_auth
# Create your views here.


def index(request):
    print(request.session.keys())
    return render(request, 'index.html')


def signup(request):
    error = None
    phone = request.session.get("phone")
    if phone is None:
        return redirect('pre_signup_phone_verify')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if request.POST['phone'] != request.session.get('phone'):
            return render(request, 'signup.html', {"form":form, "error":"인증 받은 전화번호를 기입하길 바랍니다."})

        print(form.is_valid())
        error = []
        for field in form:
            if field.errors:
                error.append(field.errors)
            # print("Field Error:", field.name, field.errors)
        if form.is_valid():
            # user_phone = models.AuthSmsSignIn.objects.filter(phone_number=form.cleaned_data.get('phone')).latest('phone_number')
            # if user_phone:
            #     if form.phone == user_phone.phone_number:
            del( request.session["phone"])
            form.save()
            return redirect('index')

    form = UserCreationForm()
    return render(request, 'signup.html', {"form":form, "error":error})

def login_core(request):
    # res_data = {}
    logout(request)

    if request.method == "POST":
        auth_input = request.POST['auth_input']
        password = request.POST['password']
        if (auth_input, password):
            auth = my_auth.UserBackend()

            user = auth.authenticate(auth_input, password)
            if user is not None:
                # if user.is_active:
                login(request, user)
                # print(user)
                return redirect('index')
        else:
            res_data['error'] = 'please enter all of input'
            return render(request, 'login.html', res_data)
    return render(request, 'login.html')
    # if request.method == 'GET':
    #     form = LoginForm()
    #     return render(request, 'login.html', {'form':form})
    # elif request.method == 'POST':
    #     auth_input = request.POST.get('auth_input')
    #     password = request.POST.get('password')
    #
    #     if not (auth_input and password):
    #         res_data['error'] = 'please enter all of input'
    #     else:
    #         auth = True
    #         try:
    #             user = models.User.objects.get(username=auth_input)
    #         except Exception as e:
    #             auth = False
    #
    #         if not auth:
    #             auth = True
    #             try:
    #                 user = models.User.objects.get(email=auth_input)
    #             except Exception as e:
    #                 auth = False
    #         if not auth:
    #             auth = True
    #             try:
    #                 user = models.User.objects.get(phone=auth_input)
    #             except Exception as e:
    #                 auth = False
    #         if auth:
    #             if check_password(password, user.password):
    #                 request.session['user'] = user.id
    #                 return redirect('index')
    #             else:
    #                 res_data['error'] = 'Invalid password'
    #         else:
    #             res_data['error'] = 'Invalid Auth input'
    # print(res_data)
    # return render(request,'login.html', res_data)

def signup_phone_verify_page(request):
    if request.method == "POST":
        form = reverifyForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            verify.send(phone)
            form = VerifyForm()
            # request.session["phone"] = phone
            # form.set_phone(phone)
            return render(request, 'phone_verify.html', {"form":form,"phone":phone})
    else:
        form = reverifyForm()
    return render(request, 'signup_phone_verify.html',{'form':form})

def phone_verify(request):
    # print("@")
    if request.method == "POST":
        # form = VerifyForm(request.POST)
        # if form.is_valid():
        #     code = form.cleaned_data.get('code')
        #     phone = request.POST['phone']
        # print(request.POST)
        code = request.POST['code']
        phone = request.POST['phone']
        result, status = verify.check(phone, code)
        if result:
            auth = models.AuthSmsSignIn(phone_number=phone, auth_number=code)
            auth.save()
            request.session['phone'] = phone
            return redirect('signup')
        else:
            message = {"message":"failed verification"}

    return render(request, 'verify_code.html', {'form': VerifyForm(), 'message': message})
@login_required
def detail(request, pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=pk)
    context = {
        'user': user
    }
    return render(request,'detail.html', {"context":context})

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
            request.session['phone'] = phone
            verify.send(phone)
            return redirect('verify')
    return render(request, 'reverify.html')

def verify_code(request):
    message = {}
    result = False
    user = None
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            result, status = verify.check(request.session.get("phone"), code)
            # print(result,status)
            if result and status == 200:
                user = get_user_model().objects.get(phone=request.session.get("phone"))
                if user:
                    del request.session['phone']
                    login(request, user)
            elif status == 404:
                message["message"] = "you need re-verification, code already expired"
        if result and user:
            return redirect('change_password')

    else:
        form = VerifyForm()
    return render(request, 'verify_code.html', {'form': form, 'message': message})

@login_required
def change_password(request):
    if request.method == "POST":
        user = request.user
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password2 == password1:
            user.set_password(password1)
            user.save()
            logout(request)
            return redirect('login')
    # form = CustomUserChangeForm()
    return render(request, 'change_password.html')