from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from board.forms import BoardForm
from django.core.paginator import Paginator
from board.models import Board
from member.models import User
from django.db.models import Q

def write(request):
    
    context = {}

    if request.method == 'POST':
        if if_logined(request) is None:
            return render(request, 'board/write_fail.html', context)

        form = BoardForm(request.POST, request.FILES)
        user_id = if_logined(request)
        if form.is_valid():
            board = form.save(commit=False)
            user_id = User.objects.get(user_id=user_id)
            board.user_id = user_id
            board.date = timezone.now()
            
            board.save()
            return render(request, 'board/write_success.html', context)
    
    else:
        form = BoardForm()
    context['form'] = form
    return render(request, 'board/write.html', context)


def delete(request, id):
    ''
#     context = {}
#     if if_session(request):
#         context['user_session_id'], context['user_session_veg_type'] = if_session(request)
#     try:
#         review = Review.objects.get(id=id)
#         review.delete()

#         return render(request, 'reviews/delete_success.html', context)
    
#     except:
#         return render(request, 'reviews/delete_fail.html', context)

# # 세션 추가
def update(request, id):
    context={}
    board = Board.objects.get(id=id)
    
    context = {}

    if request.method == 'POST':
        if if_logined(request) is None:
            return render(request, 'board/update_fail.html')

        form = BoardForm(request.POST, request.FILES)
        user_id = if_logined(request)

        if form.is_valid():
            board.user_id = User.objects.get(user_id = user_id)
            board.date = timezone.now()
            board.title = form.cleaned_data['title']
            # board.model_name = form.cleaned_data['model_name']
            board.body = form.cleaned_data['body']
            board.file = form.cleaned_data['file']

            board.save()
            return render(request, 'board/update_success.html', context)
    
    else:
        form = BoardForm()
    
    
    context['form'] = form
    context['board'] = board
    
    return render(request, 'board/update.html', context)



def list(request):

    board_list = Board.objects.order_by('-id')


    user_id = request.GET.get('user_id', '')
    if user_id:
        board_list = board_list.filter(
            Q(user_id__user_id__icontains=user_id)
        )
    title = request.GET.get('title', '')
    if title:
        board_list = board_list.filter(
            Q(title__icontains=title)
        )
    model_name = request.GET.get('model_name', '')
    if model_name:
        board_list = board_list.filter(
            Q(model_name__icontains=model_name)
        )

    try:
        now_page = int(request.GET.get('page'))
    except TypeError:
        now_page = 1


    p = Paginator(board_list, 10)
    info = p.page(now_page)

    now_page = int(now_page)
    start_page = (now_page - 1) // 10 * 10 + 1
    end_page = start_page + 9
    if end_page > p.num_pages:
        end_page = p.num_pages  

    context = {
    'info' : info,
    'now_page' : now_page,
    'start_page' : start_page,
    'end_page' : end_page,
    'page_range' : range(start_page, end_page+1),
    'has_previous' : p.page(start_page).has_previous(),
    'has_next' : p.page(end_page).has_next(),
    'user_id' : user_id,
    'title' : title,
    'model_name' : model_name,
    }
    

    return render(
        request, 'board/list.html', context)




def details(request):
    id = int(request.GET.get('id'))
    board = Board.objects.get(id=id)

    is_logined = False

    if if_logined(request) is not None and board.user_id:
        if if_logined(request) == board.user_id.user_id:
            is_logined = True

    context = {
        'id' : id,
        'board' : board,
        'is_logined' : is_logined
    }

    return render(request, 'board/details.html', context)


from aiplay import settings
import os


def download(request, id):
    board = Board.objects.get(id=id)
    
    filepath = str(settings.BASE_DIR) + ('/media/%s' % board.file.name)
    filename = os.path.basename(filepath)

    with open(filepath, 'rb') as f:
        response = HttpResponse(f, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        
        return response

def if_logined(request):
    refresh_token = request.COOKIES.get('refresh_token')
    try:
        user = User.objects.get(current_rftoken=refresh_token)
        user_id = user.user_id
        return user_id
    except:
        return None

def boardcreate(request):
    # 게시글 200개 만들기
    for i in range(200):
        userid = User.objects.get(id==0)
        Board.objects.create(user_id=userid, date='2020-12-12', model_name='pcolor',
        title='title_'+i, body='body_'+i)
    return HttpResponse('데이터 입력 완료')
    return HttpResponse(if_logined(request))