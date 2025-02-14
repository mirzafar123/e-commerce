from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth import logout ,update_session_auth_hash
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user_company = "No Company"  # Agar formadan kelmasa, default qiymat beramiz

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                user_company=user_company,  # Qo‘shimcha maydon
            )
            user.phone_number = phone_number
            user.is_active = True  
            user.save()

            messages.success(request, "Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz!")
            return redirect('signup')

    else:
        form = UserRegistrationForm()
    
    return render(request, 'signup.html', {'form': form})
def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Kiritilgan email: {email}")  # Debug
        print(f"Kiritilgan parol: {password}")  # Debug
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Email yoki parol noto‘g‘ri!")

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, "Tizimdan chiqdingiz!")
    return redirect('login')
User = get_user_model()  # Custom User model (`Account`)

def check_user_exists(request):
    email = request.GET.get('email', None)  # URL orqali email olamiz
    username = request.GET.get('username', None)  # URL orqali username olamiz

    if email and User.objects.filter(email=email).exists():
        return JsonResponse({'exists': True, 'message': "Bu email bilan foydalanuvchi mavjud!"})
    elif username and User.objects.filter(username=username).exists():
        return JsonResponse({'exists': True, 'message': "Bu username bilan foydalanuvchi mavjud!"})
    
    return JsonResponse({'exists': False, 'message': "Foydalanuvchi topilmadi!"})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import UserUpdateForm, CustomPasswordChangeForm
from django.contrib.auth import get_user_model
@login_required
def user_profile(request):
    user = request.user  # Hozirgi foydalanuvchi

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        password_form = CustomPasswordChangeForm(user, request.POST)

        if "update_profile" in request.POST:  # 🟢 Profilni yangilash
            if user_form.is_valid():
                user_instance = user_form.instance  # Avvalgi user obyekti
                for field in user_form.cleaned_data:
                    new_value = user_form.cleaned_data[field]
                    if new_value:  # ✅ Faqat **to‘ldirilgan** maydonlar o‘zgaradi!
                        setattr(user_instance, field, new_value)

                user_instance.save()  # **🟢 Endi faqat o‘zgargan maydonlar saqlanadi!**
                messages.success(request, "Profil muvaffaqiyatli yangilandi! ✅")

            else:
                messages.error(request, "Profilni yangilashda xatolik bor! ❌")

            return redirect('user_profile')

        elif "change_password" in request.POST:  # 🔴 Parolni o‘zgartirish
            if password_form.is_valid():
                new_password = password_form.cleaned_data.get("new_password1")
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Foydalanuvchini sessiyadan chiqarmaslik uchun
                messages.success(request, "Parol muvaffaqiyatli yangilandi! 🔐")
            else:
                messages.error(request, "Parolni yangilashda xatolik bor! ❌")

            return redirect('user_profile')

    else:
        user_form = UserUpdateForm(instance=user)
        password_form = CustomPasswordChangeForm(user)

    return render(request, "user.html", {"user_form": user_form, "password_form": password_form})
