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
        return JsonResponse({"message": "Invalid email format."},status=400)
    try:
        User.objects.get(email=email)
        return JsonResponse({"message": "This email has already been signed up."},
        status=400)
    except:
        return JsonResponse({"message": "Available Email.", "email":email},status=200)
    
@require_http_methods(["POST"])
def check_username(request: HttpRequest):
    '''
        아이디 체크
    '''
    username = request.POST['username'].strip()
    if not validate_username(username):
        return JsonResponse({"message": "Invalid username."},status=400)
    try:
        User.objects.get(username=username)
        return JsonResponse({"message": "This username has already been signed up."},status=400)
    except:
        return JsonResponse({"message": "Available username", "username":username},status=200)
    
@require_http_methods(["POST"])
def check_birth(request: HttpRequest):
    '''
        생년월일체크
    '''
    birth = request.POST['birth']
    if not validate_birth(birth):
        return JsonResponse({"message": "Invalid birth."},status=400)
    return JsonResponse({"message": "Available birth", "birth":birth},status=200)


def validate_username(username):
    '''
        아이디 유효성 체크
    '''
    try:
        RegexValidator(regex=r'^[a-zA-z0-9]{6,20}$')(username)
    except:
        return False

    return True

def validate_password(password):
    '''
        비밀번호 유효성 체크
    '''
    try:
        # Minimum eight characters Maximum 16 characters, at least one letter and one number
        RegexValidator(regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d~#?!@$%^&*-+]{8,16}$')(password)

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