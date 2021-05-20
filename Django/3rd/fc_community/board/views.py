from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.http import Http404
from .models import Board
from fcuser.models import Fcuser
from .forms import BoardForm
from django.contrib import messages

# Create your views here.


def board_delete(request, pk):
    res_data = {}
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404('찾을 수 없는 게시글입니다.')

    board = Board.objects.get(pk=pk)
    board.delete()
    messages.info(request, '게시글이 성공적으로 삭제되었습니다.')

    return redirect('/board/list/', res_data)


def board_detail(request, pk):
    res_data = {}
    if request.method == 'GET':
        try:
            board = Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise Http404('찾을 수 없는 게시글입니다.')
    else:
        board = BoardForm(request.POST)

        if board.is_valid():
            form = Board.objects.get(pk=pk)
            if board.cleaned_data['password'] != form.password:
                res_data['error'] = '비밀번호가 맞지 않습니다.'
                board = Board.objects.get(pk=pk)
            else:
                return redirect('/board/update/'+str(pk)+'/')
        else:
            board = Board.objects.get(pk=pk)
            res_data['error'] = '비밀번호를 입력해주세요.'

    return render(request, 'board_detail.html', {'board': board, 'res_data': res_data})


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
            board = Board.objects.get(pk=pk)
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.save()
            messages.info(request, '게시글이 성공적으로 수정되었습니다.')
            return redirect('/board/list/')
    return render(request, 'board_update.html', {'board': board, 'res_data': res_data})


def board_write(request):
    if not request.session.get('user', ''):
        return redirect('/fcuser/login')

    user_id = request.session.get('user')
    fcuser = Fcuser.objects.get(pk=user_id)

    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = Board()
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.password = form.cleaned_data['password']
            board.writer = fcuser
            board.save()
            messages.info(request, '등록완료되었습니다.')
            return redirect('/board/list/')
    else:
        form = BoardForm()
    return render(request, 'board_write.html', {'form': form, 'fcuser': fcuser})


def board_list(request):
    all_boards = Board.objects.all().order_by('-id')
    page_limit = 10
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_boards, page_limit)
    boards = paginator.get_page(page)

    index_value = paginator.count - ((page-1)*page_limit)
    print(index_value)

    return render(request, 'board_list.html', {'boards': boards, 'index_value': index_value})
