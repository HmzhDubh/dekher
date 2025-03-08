from . import views
from django.urls import path

app_name = 'fund'

urlpatterns = [
    path('add/', views.add_fund, name='add_fund'),
    path('complete/<fund_id>', views.complete_fund, name='complete_fund'),
    path('<fund_id>/details/', views.fund_details, name='fund_details'),

    path('update/<fund_id>', views.update_fund, name='update_fund'),
    path('delete/<fund_id>', views.delete_fund, name='delete_fund'),

    path('favorite/<fund_id>', views.favorite_fund, name='favorite_fund'),

    path('review/<fund_id>', views.add_review, name='add_review'),
    path('review/delete/<review_id>', views.delete_review, name='delete_review'),

    path('add/member/<fund_id>', views.add_members, name='add_members'),
    path('delete/member/<member_username>/<fund_id>', views.delete_member, name='delete_member'),
]