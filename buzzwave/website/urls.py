from django.urls.conf import path
from django.contrib.auth.views import LogoutView

from website.views.authentication_views.auth_views import HomeView, LoginView, SignupView, ActivationConfirmView, activate, contact
from website.views.authentication_views.password_reset_views import UserPasswordResetView, UserPasswordResetDoneView, CustomPasswordResetConfirmView, UserPasswordResetCompleteView
from website.views.authentication_views.validate_views import check_username, check_email, check_birth

app_name = 'website'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='website:home'), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('activation-confirm/', ActivationConfirmView.as_view(), name='activation_confirm'),
    path('activate/<str:uidb64>/<str:token>/', activate, name="activate"),

    path('password-reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password-reset-complete/', UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),


    path('contact/', contact),

    path('check-username/', check_username),
    path('check-email/', check_email),
    path('check-birth/', check_birth),
]