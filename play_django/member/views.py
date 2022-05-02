from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from argon2 import PasswordHasher, exceptions
from .models import User
from member.jwt import generate_access_token, generate_refresh_token, verify_token


def signup(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        profile_text = request.POST.get('profile_text')

        user = User(user_id=user_id, password=PasswordHasher().hash(password), profile_text=profile_text)
        user.save()

        return redirect('/')
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

            user.current_rftoken = refresh_token    # refresh_token 해시화 예정
            user.save()

            template = loader.get_template('member/login.html')
            # (cookie) or variable or localStorage에 저장
            response = HttpResponse(template.render({'access_token': access_token}, request))  
            # XSS 방어를 위해 httponly=True 추가
            response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)  
            return response

        except User.DoesNotExist as e:
            print(e)
            return HttpResponse('Login fail')
        except exceptions.VerifyMismatchError as e:
            print(e)
            return HttpResponse('Password mismatched')
        except Exception as e:
            print(e)
            return HttpResponse('...')
    else:
        return render(request, 'member/login.html')


def refresh_jwt(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if verify_token(refresh_token) == False:
        return JsonResponse({'access_token': 'Invalid_token'})

    try:
        user = User.objects.get(current_rftoken=refresh_token)
        access_token = generate_access_token(user)

        return JsonResponse({'access_token': access_token})

    except User.DoesNotExist as e:
        print(e)
        return JsonResponse({'access_token': 'Invalid_token'})


def logout(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if refresh_token == None:
        return HttpResponse('Invalid access')
    
    try:
        user = User.objects.get(current_rftoken=refresh_token)
        # refresh_token이 누출된 경우의 피해를 방지하기 위해 DB에 저장된 토큰값 삭제
        user.current_rftoken = ''
        user.save()
    
    except User.DoesNotExist as e:
        print(e)

    template = loader.get_template('member/login.html')
    response = HttpResponse(template.render({'access_token': 'logout'}, request))  
    response.delete_cookie(key='refresh_token')  

    return response
