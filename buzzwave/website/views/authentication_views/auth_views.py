from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
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

@require_http_methods(["POST"])
def contact(request: HttpRequest):
    '''
        메일 전송
    '''
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    message = request.POST['message']
    to_email = 'yttrendreport@gmail.com'

    try:
        message = render_to_string('authentication/contact_email.html', {
            'name' : name,
            'email' : email,
            'phone' : phone,
            'message' : message
        })

        mail_title = f"[Buzz Wave] Contact email ({name})"
        sendEmail = EmailMessage(mail_title, message, settings.EMAIL_HOST_USER, to=[to_email])
        sendEmail.send()
    except Exception as e:
        return JsonResponse({
            'message' : 'Send Error'
        }, status = 400)

    return JsonResponse({
        'message' : 'Your email has been sent. We will contact you as soon as possible using the contact information you provided.'
    }, status = 200)