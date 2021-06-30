from django.contrib.messages.api import error
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from .models import Board, Comment, BoardFile
from user.models import User
from .forms import BoardForm, CommentForm
from django.contrib import messages
from user.decorators import login_required
from datetime import date, datetime, timedelta
from django.db.models import Max, F
from django.views.decorators.csrf import csrf_exempt
from array import *
import json
import os
import zipfile
from io import BytesIO

def board_test(request):
    print(request.POST.get)
    pk=42
    checked_files = request.POST.getlist('checkFileChange[]', False)
    updated_board = Board.objects.get(pk=pk)
    
    for file_id in checked_files:
        updated_board.files.remove(BoardFile.objects.get(id=file_id))
        BoardFile.objects.get(id=file_id).delete()
        
    
    return redirect('/board/update/42')

def download_zip_file(request, pk):
    files = Board.objects.get(id=pk).files.all()
    filenames = []
    for file in files:
        filenames.append('./media/'+str(file.file))

    zip_subdir = str(pk)
    zip_filename = "%s.zip" % zip_subdir

    s = BytesIO()

    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(fpath, zip_path)

    zf.close()

    resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp

def include_comments(user_id, boards):
    comments_list = []
    for index in range(len(boards)):
        if not Board.objects.filter(id=boards[index].id).exists():
            return {'messages': 'POSTING_DOES_NOT_EXIST'}

        comments_list.append([{
            "contents": comment.content
        } for comment in Comment.objects.filter(board_id=boards[index].id).filter(user_id=user_id).order_by('-created_at')
        ])
    return boards, comments_list

def get_file_list(boards):
    file_list = {}
    for board in boards:
        files = board.files.all()
        file_list[board.id] = []
        for file in files:
            file_list[board.id].append(file)
                    
    return file_list
        
def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    board_id = comment.board_id
    comment_user = User.objects.get(id=comment.user_id)
    user = User.objects.get(user_id=request.session.get('user'))

    if comment_user.id == user.id:
        comment.delete()
    else:
        raise Http404('해당 댓글의 소유 권한이 없습니다.')

    return redirect('/board/detail/' + str(board_id))


@csrf_exempt
@login_required
def write_comment(request):
    if request.method == 'POST':
        comment = Comment()
        user = User.objects.get(user_id=request.session.get('user'))
        board = Board.objects.get(pk=request.POST.get('board_id'))
        comment.content = request.POST.get('comment')
        comment.user = user
        comment.board = board
        comment.save()

    return HttpResponse(json.dumps({}), content_type="application/json")


def search_comment(board_id):
    if not Board.objects.filter(id=board_id).exists():
        return {'messages': 'POSTING_DOES_NOT_EXIST'}

    comment_list = [{
        "id": comment.id,
        "username": User.objects.get(id=comment.user_id).user_id,
        "contents": comment.content,
        "created_at": comment.created_at
    } for comment in Comment.objects.filter(board_id=board_id).order_by('-created_at')
    ]
    return comment_list


@login_required
def like_board(request, pk):
    board = get_object_or_404(Board, id=pk)
    user = request.session.get('user')
    user_id = User.objects.get(user_id=user)
    if user_id in board.like_users.all():
        board.like_users.remove(user_id)
    else:
        board.like_users.add(user_id)
    return redirect('/board/detail/'+str(pk))


@csrf_exempt
def board_delete_multi(request):
    if request.method == 'POST':
        list = request.POST
        for key, value in list.items():
            try:
                board = Board.objects.get(pk=value)
            except Board.DoesNotExist:
                raise Http404('찾을 수 없는 게시글입니다.')
            board.delete()
    print('hi')
    return redirect('/board/list')


def board_delete(request, pk):
    res_data = {}
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404('찾을 수 없는 게시글입니다.')
    print(type(request.session.get('user')), type(board.writer))
    if str(board.writer) == request.session.get('user'):
        board = Board.objects.get(pk=pk)
        board.delete()
        messages.info(request, '게시글이 성공적으로 삭제되었습니다.')
    else:
        messages.info(request, '본인 게시글이 아니면 삭제할 수 없습니다.')

    return redirect('/board/list/', res_data)


@login_required
def board_detail(request, pk):
    res_data = {}
    if request.method == 'GET':
        try:
            board = Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise Http404('찾을 수 없는 게시글입니다.')
    else:
        form = BoardForm(request.POST)
        board = Board.objects.get(pk=pk)
        if form.is_valid():
            if str(board.writer) != request.session.get('user'):
                res_data['error'] = '해당 게시글의 작성자가 아닙니다.'
            else:
                return redirect('/board/update/'+str(pk)+'/')
        else:
            res_data['error'] = '비밀번호를 입력해주세요.'

    if str(board.writer) == request.session.get('user', ''):
        myboard = True
    else:
        myboard = False

    comment_list = search_comment(pk)
    response = render(request, 'board_detail.html', {
                      'board': board,
                      'myboard': myboard,
                      'res_data': res_data,
                      'comment_list': comment_list
                      })

    # 조회수 기능
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    if request.COOKIES.get('hitboard') is None:
        cookie_value = '_'
    else:
        cookie_value = request.COOKIES.get('hitboard')
    print(cookie_value)

    if f'_{pk}_' not in cookie_value:
        cookie_value += f'{pk}_'
        response.set_cookie('hitboard', value=cookie_value, max_age=max_age, httponly=True)
        board.hit += 1
        board.save()

    return response


@login_required
def board_update(request, pk):
    res_data = {}
    if request.method == 'GET':
        try:
            board = Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise Http404('찾을 수 없는 게시글입니다.')
    else:
        form = BoardForm(request.POST)
        
        if form.is_valid():
            checked_files = request.POST.getlist('checkFileChange[]', False)
            board = Board.objects.get(pk=pk)
            if checked_files:
                for file_id in checked_files:
                    board.files.remove(BoardFile.objects.get(id=file_id))
                    BoardFile.objects.get(id=file_id).delete()
                
            try:
                for f in request.FILES.getlist('files'):
                    board.files.create(file=f)
            except:
                print('수정 실패')
                pass
                        
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.save()
            messages.info(request, '게시글이 성공적으로 수정되었습니다.')
            return redirect('/board/list/')
    return render(request, 'board_update.html', {'board': board, 'res_data': res_data})


@login_required
def board_write(request):
    if not request.session.get('user', ''):
        return redirect('/login')

    user_id = request.session.get('user')
    user = User.objects.get(user_id=user_id)
    reply = []
    
    if request.method == 'POST':
        form = BoardForm(request.POST, request.FILES)
        if form.is_valid():
            board = Board()
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.writer = user

            if not request.GET.get('reply', ''):
                value = Board.objects.aggregate(max_groupno=Max('groupno'))
                board.groupno = value["max_groupno"]+1
            else:
                parent_board = Board.objects.get(id=request.GET.get('reply'))
                Board.objects.filter(orderno__gte=parent_board.orderno+1).update(orderno=F('orderno')+1)
                board.groupno = parent_board.groupno
                board.orderno = parent_board.orderno+1
                board.depth = parent_board.depth+1
            
            board.save()
            print(request.FILES.getlist('files'))
            
            try:
                for f in request.FILES.getlist('files'):
                    #TODO : 용량, 이름 등 제한 걸기 감사합니다.
                    board.files.create(file=f)
            except:
                print('실패')
                pass
            
            messages.info(request, '등록완료되었습니다.')
            return redirect('/board/list/')
    else:
        if request.GET.get('reply', ''):
            form = BoardForm()
            reply.append(request.GET.get('reply'))
            reply.append(Board.objects.get(pk=reply[0]))
        else:
            form = BoardForm()
        
    return render(request, 'board_write.html', {'form': form, 'fcuser': user, 'reply': reply})


def board_list(request):
    if request.method == 'GET':
        all_boards = search(request)

        if all_boards == 'login':
            return redirect('/login/')

        search_keyword = request.GET.get('word', '')
        search_type = request.GET.get('type', '')
        filter = request.GET.get('filter', '')

        page_limit = 3
        page = int(request.GET.get('p', 1))
        paginator = Paginator(all_boards, page_limit)
        boards = paginator.get_page(page)
        index_value = paginator.count - ((page-1)*page_limit)
        
        comments_list = []
        if filter == 'myWritingcomment':
            boards, comments_list = include_comments(User.objects.get(
                user_id=request.session.get('user')).id, boards)
            
        
        comment_count_list = []
        for board in boards:
            comment_count_list.append(Comment.objects.filter(
                board_id=board.id).count())

        file_list = []
        file_list = get_file_list(boards)
        
        
        fullList = []
            
        for index, board in enumerate(boards):
            try:
                comment_count = comment_count_list[index]
            except:
                comment_count = []
            try:
                comment_list = comments_list[index]
            except:
                comment_list = []
            try:
                file = file_list[board.id]
            except:
                file = []
    
            fullList.append((board, comment_count, comment_list, file))
            
        return render(request, 'board_list.html', {'boards': boards,
                                                   'index_value': index_value,
                                                   'search_type': search_type,
                                                   'filter': filter,
                                                   'search_keyword': search_keyword,
                                                   'comments_list': comments_list,
                                                   'comment_count_list': comment_count_list,
                                                   'fullList': fullList
                                                   })


def search(request):
    search_keyword = request.GET.get('word', '')
    search_type = request.GET.get('type', '')
    filtering = request.GET.get('filter', '')
    try:
        user = User.objects.get(user_id=request.session.get('user'))
    except User.DoesNotExist:
        user = ''
        
    if search_type == 'title':
        all_boards = Board.objects.filter(title__icontains=str(search_keyword)).order_by('-groupno', 'orderno')
    elif search_type == 'content':
        all_boards = Board.objects.filter(
            contents__icontains=str(search_keyword)).order_by('-groupno', 'orderno')
    else:
        all_boards = Board.objects.all().order_by('-groupno', 'orderno')

    if filtering and user:
        if filtering == 'myWritingboard':
            all_boards = all_boards.filter(writer_id=user.id)
        elif filtering == 'myLikeBoard':
            all_boards = all_boards.filter(like_users=user.id)
    elif filtering and not user:
        return 'login'

    return all_boards
