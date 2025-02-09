from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.views.decorators.http import require_http_methods
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.validators import validate_email
from django.core.exceptions  import ValidationError
from django.db import transaction
from django.conf import settings
from django.contrib.auth.models import User

from website.models import Subscriber
from website.views.authentication_views.validate_views import validate_username, validate_password, validate_birth
from website.tokens import account_activation_token

import datetime

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
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({'message':'아이디 또는 비밀번호가 일치하지 않습니다.'}, status = 400)
        if not user.check_password(raw_password=password):
            return JsonResponse({'message':'아이디 또는 비밀번호가 일치하지 않습니다.'}, status = 400)
        if user.profile.withdrawal_at:
            return JsonResponse({'message':'탈퇴한 회원입니다.'}, status = 400)
        if not user.profile.email_verified:
            return JsonResponse({'message':'이메일을 확인하여 계정을 활성화 해주세요.', 'url':reverse('website:activation_confirm') + f'?username={username}'}, status = 403)
        if not user.is_active:
            return JsonResponse({'message':'비활성화 된 회원입니다.'}, status = 400)
        login(request, user)
        if 'next' in request.GET:
            url = request.GET.get('next')
            url = url.split('?next=')[-1]
        else:
            url = reverse('website:home')
        return JsonResponse({'message':'Hi.', 'url':url}, status = 200)
    

class SignupView(View):
    '''
        회원가입
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            return redirect('website:home')
        return render(request, 'authentication/user_signup.html', context)
    
    def post(self, request: HttpRequest, *args, **kwargs):
        membername = request.POST['membername']
        email = request.POST['email'].strip()
        username = request.POST['username'].strip()
        password = request.POST['password']
        phone = request.POST['phone']
        birth = request.POST['birth']
        company = request.POST['company']

        if not validate_username(username):
            return JsonResponse({"message": "유효하지 않은 아이디 입니다."}, status=400)
        if not validate_password(password):
            return JsonResponse({"message": "비밀번호는 숫자와 영문자 조합으로 8~16자리를 사용해야 합니다."}, status=400)
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"message": "잘못된 이메일 형식입니다."},
                status=400)
        if not validate_birth(birth):
            return JsonResponse({
                "message": "잘못된 날짜 형식 입니다. ex) 19900101"},
                status=400)
        try:
            User.objects.get(username=username)
            return JsonResponse({
                "message": "이미 가입된 아이디 입니다."},
                status=400)
        except:
            pass
        try:
            User.objects.get(email=email)
            return JsonResponse({
                "message": "이미 가입된 이메일 입니다."},
                status=400)
        except:
            pass

        try:
            with transaction.atomic(): 
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user.is_active = False
                user.profile.membername = membername.strip()
                user.profile.birth = datetime.datetime.strptime(birth, "%Y%m%d")
                user.profile.phone = phone.strip()
                user.profile.company = company.strip()
                user.profile.email_verified = False
                user.save()

                current_site = get_current_site(request) 
                message = render_to_string('authentication/activation_email.html', {
                    'user': user,
                    'protocol' : request.scheme,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                mail_title = "[D'Nova] Activate your account"
                sendEmail = EmailMessage(mail_title, message, f"D'Nova <{settings.EMAIL_HOST_USER}>", to=[email])
                sendEmail.send()
        except Exception as e:
            print(e)
            return JsonResponse({"message": "Sign up error occurred."}, status=400)

        return JsonResponse({"url":reverse('website:activation_confirm') + f'?username={username}'},
            status=201)
    

class ActivationConfirmView(View):
    '''
        이메일 보냄 확인 페이지
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        username = request.GET.get('username', '')
        user = get_object_or_404(User, username=username)
        context['username'] = user.username
        context['email'] = user.email
         
        return render(request, 'authentication/activation_confirm.html', context)
    
    def post(self, request, *args, **kwargs):
        username = request.GET.get('username', '')
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({"message": "잘못된 아이디 입니다."},status=400)
        if not user.email:
            return JsonResponse({"message": "잘못된 이메일 입니다."},status=400)
        if not user.profile.email_verified:
            current_site = get_current_site(request) 
            message = render_to_string('authentication/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_title = "[D'Nova] Activate your account"
            sendEmail = EmailMessage(mail_title, message, f"D'Nova <{settings.EMAIL_HOST_USER}>", to=[user.email])
            sendEmail.send()
            return JsonResponse({"url":reverse('website:activation_confirm') + f'?username={user.username}', "message":"이메일이 재전송 되었습니다."}, status=200)
        else:
            return JsonResponse({"message": "이미 이메일 인증을 완료한 회원입니다."}, status=400)
        
def activate(request: HttpRequest, uidb64, token):
    '''
        토큰 인증을 통한 계정 활성화
    '''
    if request.method=='GET':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None            
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_verified = True
            user.save()
            return render(request, 'authentication/activation_complete.html', {'username' : user.username})
        else:
            return render(request, 'authentication/activation_error.html', {'error' : '만료 된 링크입니다.'})
        

class FindUsernameView(View):
    '''
        아이디 찾기
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            return redirect('website:home')
        return render(request, 'authentication/find_username.html', context)
    
    def post(self, request: HttpRequest, *args, **kwargs):
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except:
            return JsonResponse({'message':'가입된 이메일이 없습니다.'}, status = 400)
        return JsonResponse({'message':f'가입하신 아이디는 {user.username} 입니다.'}, status = 200)
    

@require_http_methods(["POST"])
def contact(request: HttpRequest):
    '''
        메일 전송
    '''
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    message = request.POST['message']
    company = request.POST['company']
    job = request.POST['job']

    to_email = 'dnova@d-nova.com'

    try:
        message = render_to_string('authentication/contact_email.html', {
            'name' : name,
            'email' : email,
            'phone' : phone,
            'company' : company,
            'job' : job,
            'message' : message
        })

        mail_title = f"Contact from {name}"
        sendEmail = EmailMessage(mail_title, message, f"Contact <{settings.EMAIL_HOST_USER}>", to=[to_email])
        sendEmail.send()
    except Exception as e:
        print(e)
        return JsonResponse({
            'message' : 'Send Error'
        }, status = 400)

    return JsonResponse({
        'message' : '이메일이 전송되었습니다.\n제공해주신 연락처를 통해 최대한 빠르게 답변드리겠습니다.'
    }, status = 200)


@require_http_methods(["POST"])
def subscribe(request: HttpRequest):
    '''
        구독
    '''
    email = request.POST['email']
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"message": "Invalid email format."},
            status=400)
    try:
        Subscriber.objects.get_or_create(email=email, is_activate=True)
    except:
        return JsonResponse({"message": "Subscribe Error."},
            status=400)
    return JsonResponse({
        'message' : 'Thank you for subscribing!'
    }, status = 200)