from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .models import Profile
from fund.models import Fund, Favorite

# Create your views here.
def register(request: HttpRequest):
    if request.method == "POST":
        try:
            with transaction.atomic():
                new_user = User.objects.create_user(
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    email = request.POST['email'],
                    password = request.POST['password'],
                    username = request.POST['username'],
                )
                new_user.save()

                profile = Profile(
                    user = new_user,
                    about = request.POST['about'],
                    avatar = request.FILES.get("avatar", Profile._meta.get_field("avatar").get_default()),
                )

                profile.save()

            messages.success(request, f'{new_user.username} Account was created Successfully', 'alert-success')
            return redirect('accounts:sign_in')
        except IntegrityError as ie:
            print(ie)
            messages.error(request, 'This username is taken, please try another one', 'alert-danger')
        except Exception as e:
            print(e)
            messages.error(request, 'error in creating your account', 'alert-danger')
    return render(request, 'login_form.html')


def sign_in(request: HttpRequest):

    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            messages.success(request, f'{user.username} Signed in Successfully', 'alert-success')
            return redirect(request.GET.get('next', '/'))
        else:
            messages.error(request, 'Username or password is wrong, please try again', 'alert-danger')
    return render(request, 'login_form.html')


def log_out(request: HttpRequest):

    logout(request)
    messages.success(request, 'logged out successfully, See You later', 'alert-success')
    return redirect('main:home_view')


def profile_view(request: HttpRequest, user_name):

    if not request.user.is_authenticated:
        messages.error(request, 'Please Sign in to View Your Profile', 'alert-danger')
        return redirect('accounts:sign_in')

    user = User.objects.get(username=user_name)
    favorite_funds = Favorite.objects.filter(user = user)

    if not Profile.objects.filter(user = user).first():
        new_profile = Profile(user=user)
        new_profile.save()
    profile: Profile = user.profile
    # profile = Profile.objects.get(user=user)
    user_funds = Fund.objects.filter(owner=user)

    if request.method == "GET" and 'status' in request.GET and request.GET['status'] != 'all':
        user_funds = user_funds.filter(status = request.GET['status'])

        return render(request, 'profile.html', context={'user':user, 'status_choices': Fund.Status.choices, 'funds': user_funds})

    return render(request, 'profile.html', context={'user':user, 'status_choices': Fund.Status.choices, 'funds': user_funds, 'favorite_funds':favorite_funds})


def update_profile(request: HttpRequest, user_name):

    if not request.user.is_authenticated:
        messages.error(request, "Sign in to update your profile","alert-warning")
        return redirect("accounts:sign_in")

    user = User.objects.get(username=user_name)
    user_profile = Profile.objects.get(user=user)

    if request.method == "POST":
        try:
            with transaction.atomic():

                user_profile.about = request.POST['about']
                user_profile.phone_num = request.POST['phone_num']
                if 'avatar' in request.FILES: user_profile.avatar = request.FILES['avatar']

                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.username = request.POST['username']
                user.email = request.POST['email']

                user_profile.save()
                user.save()

                messages.success(request, 'Profile was Updated Successfully', 'alert-success')
                return redirect('accounts:profile_view', user_name=user.username)

        except Exception as e:
            print(e.__class__)
            messages.error(request, 'error in updating your profile ', 'alert-danger')
            return redirect('accounts:profile_view', user_name=user.username)