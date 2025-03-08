from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('signin/', views.sign_in, name="sign_in"),
    path('register/', views.register, name="register"),
    path('logout/', views.log_out, name="log_out"),

    path('profile/<user_name>', views.profile_view, name="profile_view"),
    path('profile/update/<user_name>', views.update_profile, name="update_profile"),
]