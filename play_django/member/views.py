import profile
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
        email = request.POST.get('email')

        user = User(user_id=user_id, password=PasswordHasher().hash(password), email=email)
        user.save()

        return redirect('/')
    else:
        return render(request, 'member/signup.html')


def find_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as e:
            print(e)
            return HttpResponse('<h1>No matching information found</h1>')

        return HttpResponse(f'<h1 style="text-align: center; margin-top: 3%">Your UserID is {user.user_id}.</h1>') 

    else:
        return render(request, 'member/find_user.html')


def update_user(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if refresh_token == None:
        return redirect('/')

    if request.method == 'POST':
        password = request.POST.get('password')

        try:
            user = User.objects.get(current_rftoken=refresh_token)
            user.password = PasswordHasher().hash(password)
            user.save()

        except User.DoesNotExist as e:
            print(e)
            HttpResponse('<h1>Invalid access</h1>')

        return redirect('/')   
    else:
        return render(request, 'member/update_user.html')


def delete_user(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if refresh_token == None:
        return HttpResponse('<h1>Invalid access</h1>')
    
    try:
        user = User.objects.get(current_rftoken=refresh_token)
        user.delete()

    except User.DoesNotExist as e:
        print(e)

    template = loader.get_template('member/login.html')
    response = HttpResponse(template.render({'access_token': 'logout'}, request))  
    response.delete_cookie(key='refresh_token')  

    return response


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
            return HttpResponse('<h1>Login fail</h1>')
        except exceptions.VerifyMismatchError as e:
            print(e)
            return HttpResponse('<h1>Password mismatched</h1>')
        except Exception as e:
            print(e)
            return HttpResponse('<h1>...</h1>')
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
        return HttpResponse('<h1>Invalid access</h1>')
    
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