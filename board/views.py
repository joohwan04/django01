from django.shortcuts import render, redirect
from .models import Board, Reply
# Create your views here.
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages


def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    action = request.GET.get("action", "")
    if action == 'add':
        b.likey.add(request.user)
    else:
        b.likey.remove(request.user)
    return redirect("board:detail", bpk)

def index(request):
    pg = request.GET.get("page", 1)
    cate = request.GET.get("cate", "")
    kw = request.GET.get("kw", "")

    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            try:
                from acc.models import User
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none()
        elif cate == "con":
            b = Board.objects.filter(content__contains=kw)
        else:
            messages.warning(request, "혼나!")
            b = Board.objects.all()
    else:
        b = Board.objects.all()
    
    b = b.order_by('-pubdate')

    pag = Paginator(b,5)
    obj = pag.get_page(pg)

    context = {
        "bset": obj,
        "cate": cate,
        "kw": kw
    }
    return render(request, "board/index.html", context)

def dreply(request, bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if request.user == r.replyer:
        r.delete()
    else:
        pass # 19일차
    return redirect("board:detail", bpk)

def creply(request, bpk):
    c = request.POST.get("com")
    b = Board.objects.get(id=bpk)
    Reply(b=b, replyer=request.user, comment=c, pubdate=timezone.now()).save()
    return redirect("board:detail", bpk)

def update(request, bpk):
    b = Board.objects.get(id=bpk)
    # 자신의 글이 아니면 board 의 index 로 이동!!!
    if b.writer != request.user:
        # 19 일차 메세지
        return redirect("board:index")

    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        b.subject = s
        b.content = c
        b.save()
        return redirect("board:detail", bpk)
    context = {
        "b":b
    }
    return render(request, "board/update.html", context)

def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        if s and c:
            Board(subject=s, content=c, writer=request.user, pubdate=timezone.now()).save()
            return redirect("board:index")

    return render(request, "board/create.html")

def delete(request, bpk):
    b = Board.objects.get(id=bpk)
    if request.user == b.writer:
        b.delete()
    else:
        messages.warning(request, "혼나!!")
    return redirect("board:index")

def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        "b": b,
        "rset" : r
    }
    return render(request, "board/detail.html", context)

