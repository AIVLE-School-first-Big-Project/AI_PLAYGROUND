from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.utils import timezone
from argon2 import PasswordHasher, exceptions
import jwt
import aiplay.settings
from member.jwt import generate_access_token, generate_refresh_token
from .models import User


def signup(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        profile_text = request.POST.get('profile_text')

        user = User(user_id=user_id, password=PasswordHasher().hash(password), profile_text=profile_text)
        user.createdAt = timezone.now()
        user.save()

        return redirect('/base')
    else:
        return render(request, 'member/signup.html')


def login(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        try:
            user = User.objects.get(user_id=user_id)
            PasswordHasher().verify(user.password, password)

            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)

            template = loader.get_template('member/login.html')

            # (cookie) or variable or localStorage에 저장
            response = HttpResponse(template.render({'access_token': access_token}, request))  
            
            # XSS 방어를 위해 httponly=True 추가
            response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)  
            
            return response

        except User.DoesNotExist as e:
            return HttpResponse('Login fail')
        
        except exceptions.VerifyMismatchError as e:
            return HttpResponse('Password mismatched')

        except Exception as e:
            return HttpResponse('...')

    else:
        return render(request, 'member/login.html')


def refresh_jwt(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if refresh_token is None:
        return HttpResponse('Invalid access')

    try:
        payload = jwt.decode(refresh_token, aiplay.settings.SECRET_KEY, algorithms=['HS256'])

        user_id = payload['user_id']
        user = User.objects.get(user_id=user_id)

        access_token = generate_access_token(user)
        return JsonResponse({'access_token': access_token})
    
    except User.DoesNotExist as e:
        return HttpResponse('User not found')
    
    except Exception as e:
        return HttpResponse('...')
    

def logout(request):
    template = loader.get_template('/base')
    response = HttpResponse(template.render(), request)
    response.delete_cookie('refresh_token')

    return response
