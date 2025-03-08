from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from fund.models import Fund, Favorite, Review


# Create your views here.
def add_fund(request: HttpRequest):

    new_fund = Fund(
        owner = request.user,
        name = 'NewFund',
        description = f'New fund created by {request.user.username}',
        monthly_stock = 1000,

    )
    new_fund.save()
    return render(request, 'add_fund.html', context={'fund': new_fund})


def complete_fund(request: HttpRequest, fund_id):

    if request.method == "GET" and 'cancel' in request.GET:
        fund = Fund.objects.get(pk=fund_id)
        fund.delete()
        messages.success(request, 'Canceled successfully', 'alert-success')
        return redirect('accounts:profile_view', user_name = request.user.username)

    if request.method == "POST":
        fund = Fund.objects.get(pk=fund_id)

        if 'logo' in request.FILES: fund.logo = request.FILES['logo']
        fund.name = request.POST['name']
        fund.description = request.POST['description']
        fund.monthly_stock = request.POST['monthly_stock']
        fund.start_date = request.POST['start_date']
        fund.status = request.POST['status']

        fund.save()
        messages.success(request, 'Fund was created successfully', 'alert-success')
    return redirect('accounts:profile_view', user_name = request.user.username)


def fund_details(request: HttpRequest, fund_id):
    fund = Fund.objects.get(pk=fund_id)
    reviews = Review.objects.filter(fund=fund)
    favorite = Favorite.objects.filter(fund=fund, user=request.user)
    return render(request, 'fund_details.html', context={'fund': fund, 'reviews': reviews, 'rates': Review.Rates.choices, 'favorite': favorite})


def update_fund(request: HttpRequest, fund_id):

    fund = Fund.objects.get(pk=fund_id)

    if not request.user == fund.owner:
        messages.error(request, 'Only fund Owner can Edit fund data', 'alert-danger')
        return redirect('fund:fund_details', fund_id=fund_id)

    if request.method == "POST":
        if 'logo' in request.FILES: fund.logo = request.FILES['logo']
        fund.name = request.POST['name']
        fund.description = request.POST['description']
        fund.monthly_stock = request.POST['monthly_stock']
        fund.start_date = request.POST['start_date']
        fund.status = request.POST['status']
        fund.save()

        messages.success(request, 'Fund was Updated successfully', 'alert-success')
        return redirect('fund:fund_details', fund_id = fund_id)

    return render(request, 'update_fund.html', context={'fund': fund})


def delete_fund(request: HttpRequest, fund_id):

    fund = Fund.objects.get(pk=fund_id)
    fund.delete()
    messages.success(request, 'Fund Was Deleted Successfully', 'alert-success')
    return redirect('accounts:profile_view', user_name = request.user.username)


def favorite_fund(request: HttpRequest, fund_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Please register to favorite funds', 'alert-danger')
        return redirect('accounts:sign_in')

    try:
        fund = Fund.objects.get(pk=fund_id)

        new_favorite = Favorite(
            user = request.user,
            fund = fund
        )
        favorite = Favorite.objects.filter(fund=fund, user=request.user)

        if not favorite:
            new_favorite.save()
            messages.success(request, 'fund added to favorite', 'alert-success')
        else:
            favorite.delete()
            messages.success(request, 'fund removed from favorite', 'alert-warning')

    except Exception as e:
        print(e)

    return redirect(request.GET.get('next', '/'))


def add_review(request: HttpRequest, fund_id):

    try:
        if not request.user.is_authenticated:
            messages.error(request, "Please Login to add reviews", 'alert-danger')
            return redirect('accounts:sign_in')
        if request.method == 'POST':
            new_comment = Review(
                fund=Fund.objects.get(pk=fund_id),
                user=request.user,
                comment=request.POST['comment'],
                rating=request.POST['rating'])
            new_comment.save()

            # # Send message to user
            # new_user_message = UserMessage(
            #     sender = User.objects.get(pk=1),
            #     user = request.user,
            #     subject = 'Review Fund',
            #     content = 'You Reviewed a Fund',
            # )

            # new_user_message.save()
            messages.success(request, 'Comment was added successfully', 'alert-success')
        return redirect('fund:fund_details', fund_id = fund_id)
    except Exception as e:
        messages.error(request, 'Error in adding your comment', 'alert-danger')
        # return render(request,'page_not_found.html')
        print(e)
        return redirect('fund:fund_details', fund_id = fund_id)


def delete_review(request: HttpRequest, review_id):

    if request.user.is_superuser:
        review = Review.objects.get(pk=review_id)
        review.delete()

        # Send message to user
        # new_user_message = UserMessage(
        #     sender = User.objects.get(pk=1),
        #     user = request.user,
        #     subject = 'Delete Review',
        #     content = 'You Deleted your review',
        # )
        #
        # new_user_message.save()

        messages.success(request, 'Review Deleted Successfully', 'alert-success')
    return redirect('fund:fund_details', fund_id=review.fund.id)


# TODO Add Members to funds using email or phone number
def add_members(request:HttpRequest, fund_id):

    if request.method == "POST":
        user_email = request.POST['member_email']
    fund = Fund.objects.get(pk = fund_id)
    try:
        user = User.objects.get(email=user_email)
    except Exception as e:
        print(e.__cause__, e.__class__, e.__traceback__)
        messages.error(request,'Only Dekher Members can be added to funds, please let them register to be added to your fund', 'alert-warning')
        return redirect('fund:fund_details', fund_id = fund_id)

    if not request.user == fund.owner:
        messages.error(request, "Register to Participate in Funds", 'alert-danger')
        return redirect('accounts:sign_in')
    try:
        fund.members.add(user)
        messages.success(request, 'Member was Added Successfully', 'alert-success')
        return redirect('fund:fund_details', fund_id = fund_id)
    except Exception as e:
        print(e.__cause__, e.__traceback__)
        messages.error(request, 'Error adding member. This member might be already added', 'alert-danger')
        return redirect('fund:fund_details', fund_id = fund_id)


def delete_member(request: HttpRequest, member_username, fund_id):

    try:
        fund = Fund.objects.get(pk = fund_id)
        user = User.objects.get(username = member_username)

        if user in fund.members.all():  # Check if the user is a member
            fund.members.remove(user)

            messages.success(request, 'Member was removed successfully', 'alert-success')
        return redirect('fund:update_fund', fund_id = fund_id)
    except Exception as e:
        print(e.__class__)
        messages.error(request, 'Error Deleting member', 'alert-danger')
        return redirect('fund:update_fund', fund_id = fund_id)