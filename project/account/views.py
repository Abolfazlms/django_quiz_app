# account/views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import CustomUser
import sweetify

@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/1')

    if request.method == 'POST':
        username_or_phone = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(phone_number=username_or_phone)
            username = user.username
        except CustomUser.DoesNotExist:
            username = username_or_phone

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            sweetify.success(request, 'با موفقیت وارد شدید!', text='شما می‌توانید تست را انجام بدهید', type='success', timer=2000)
            return redirect('/1')
        else:
            sweetify.error(request, 'Oops...', text='نام کاربری یا گذرواژه اشتباه است.', persistent='close', type='error')

    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

@csrf_exempt
def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                sweetify.success(request, 'ثبت‌نام با موفقیت انجام شد', text='شما می‌توانید وارد حساب کاربری خود شوید.', type='success', timer=2000)
                return redirect('account:login')
        else:
            sweetify.toast(request, type='success', title='راهنما', text='رمز عبور انتخابی باید حداقل دارای 8 کاراکتر باشد.', timer=4000)
            form = CustomUserCreationForm()

        return render(request, 'accounts/signup.html', {'form': form})
    else:
        return redirect('/')
