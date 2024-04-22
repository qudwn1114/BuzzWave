from django.urls.conf import path
from django.contrib.auth.views import LogoutView

from website.views.authentication_views.auth_views import HomeView, LoginView

app_name = 'website'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='website:home'), name='logout'),
]