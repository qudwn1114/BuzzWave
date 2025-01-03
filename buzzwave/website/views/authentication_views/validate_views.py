from django.core.validators import RegexValidator
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.validators import validate_email
from django.core.exceptions  import ValidationError
from django.contrib.auth.models import User

import datetime

@require_http_methods(["POST"])
def check_email(request: HttpRequest):
    '''
        이메일 체크
    '''
    email = request.POST['email'].strip()
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"message": "잘못된 이메일 형식입니다."},status=400)
    try:
        User.objects.get(email=email)
        return JsonResponse({"message": "이미 가입된 이메일 입니다."},
        status=400)
    except:
        return JsonResponse({"message": "사용가능한 이메일 입니다.", "email":email},status=200)
    
@require_http_methods(["POST"])
def check_username(request: HttpRequest):
    '''
        아이디 체크
    '''
    username = request.POST['username'].strip()
    if not validate_username(username):
        return JsonResponse({"message": "유효하지 않은 아이디 형식입니다."},status=400)
    try:
        User.objects.get(username=username)
        return JsonResponse({"message": "이미 가입된 아이디 입니다."},status=400)
    except:
        return JsonResponse({"message": "사용가능한 아이디 입니다.", "username":username},status=200)
    
@require_http_methods(["POST"])
def check_birth(request: HttpRequest):
    '''
        생년월일체크
    '''
    birth = request.POST['birth']
    if not validate_birth(birth):
        return JsonResponse({"message": "잘못된 날짜 형식 입니다. ex) 19900101"},status=400)
    return JsonResponse({"message": "사용가능한 날짜 입니다.", "birth":birth},status=200)


def validate_username(username):
    '''
        아이디 유효성 체크
    '''
    try:
        RegexValidator(regex=r'^[a-z0-9]{6,20}$')(username)
    except:
        return False

    return True

def validate_password(password):
    '''
        비밀번호 유효성 체크
    '''
    try:
        # Minimum eight characters Maximum 16 characters, at least one letter and one number
        RegexValidator(regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()_\-+={}\[\]:;"\'<>,.?/~`|\\]{8,16}$')(password)

        # Minimum eight characters  Maximum 16 characters, at least one uppercase letter, one lowercase letter, one number and one special character
        # RegexValidator(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~#?!@$%^&*-+])[A-Za-z\d~#?!@$%^&*-+]{8,16}$')(password)
    except:
        return False

    return True

def validate_birth(birth):
    '''
    생년월일 유효성체크
    '''
    try:
        birth = datetime.datetime.strptime(birth, "%Y%m%d")
    except ValueError:
        return False
    
    return True