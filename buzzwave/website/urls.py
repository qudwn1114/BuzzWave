from django.urls.conf import path
from django.contrib.auth.views import LogoutView

from website.views.authentication_views.auth_views import HomeView, LoginView, SignupView, FindUsernameView, ActivationConfirmView, activate, contact, subscribe
from website.views.authentication_views.password_reset_views import UserPasswordResetView, UserPasswordResetDoneView, CustomPasswordResetConfirmView, UserPasswordResetCompleteView
from website.views.authentication_views.validate_views import check_username, check_email, check_birth
from website.views.blog_views.blog_views import BlogView, BlogCreateView, BlogDetailView, BlogEditView
from website.views.blog_views.summernote_views import summernote_image_upload_view

app_name = 'website'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='website:home'), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('activation-confirm/', ActivationConfirmView.as_view(), name='activation_confirm'),
    path('activate/<str:uidb64>/<str:token>/', activate, name="activate"),

    path('find/username/', FindUsernameView.as_view(), name='find_username'),
    path('password-reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password-reset-complete/', UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),


    path('contact/', contact),
    path('subscribe/', subscribe),

    path('check-username/', check_username),
    path('check-email/', check_email),
    path('check-birth/', check_birth),

    path('blog/', BlogView.as_view(), name='blog'),
    path('blog-create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog-edit/<int:pk>/', BlogEditView.as_view(), name='blog_edit'),
    path('summernote/upload-image/', summernote_image_upload_view),
]
