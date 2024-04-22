from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.
class HomeView(View):
    '''
    사용자 메인 화면
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        return render(request,'authentication/user_main.html', context)
    

class LoginView(View):
    '''
        로그인 기능
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            return redirect('website:home')
        return render(request, 'authentication/user_login.html', context)
    
    def post(self, request: HttpRequest, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            if 'next' in request.GET:
                url = request.GET.get('next')
                url = url.split('?next=')[-1]
            else:
                url = reverse('website:home')
            return JsonResponse({'message':'로그인 되었습니다.', 'url':url}, status = 200)
        
        else:
            return JsonResponse({'message':'일치하는 회원정보가 없습니다'}, status = 400)