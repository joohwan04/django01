from django.shortcuts import render, redirect
from .models import Topic, Choice
from django.utils import timezone
from django.core.paginator import Paginator

def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        cn = request.POST.getlist("cname")
        cp = request.FILES.getlist("cpic", ["", "", ""])
        cc = request.POST.getlist("ccom", "")

        print(s, c, cn, cp, cc)
        if len(cn) > 1 :
            t = Topic(subject=s, content=c, maker=request.user, pubdate=timezone.now())
            t.save()
            for name, pic, com in zip(cn, cp, cc):
                Choice(topic=t, chname=name, chpic=pic, chcom=com).save()
            return redirect("vote:index")
    return render(request, "vote/create.html")

def cancel(request, tpk):
    t = Topic.objects.get(id=tpk)
    t.voter.remove(request.user)
    # 나를 참조하고 있는 보기들 중에 유저있으면 빼네는 거~
    # cset = t.Choice_set.all()
    # for i in cset:
    #     if request.user in i.choicer.all():
    #      i.choicer.remove(request.user)
    #      break
    # 유저 입장에서 내가 고른 보기들 중 topic 이 t 인 친구를 고르는 것!!!
    print(request.user.choice_set.all())
    request.user.choice_set.get(topic=t).choicer.remove(request.user)
    return redirect("vote:detail", tpk)

def vote(request, tpk):
    t = Topic.objects.get(id=tpk)
    if not request.user in t.voter.all():
        t.voter.add(request.user)
        cpk = request.POST.get("ch")
        c = Choice.objects.get(id=cpk)
        c.choicer.add(request.user)
    return redirect('vote:detail', tpk)

def detail(request, tpk):
    t = Topic.objects.get(id=tpk)
    c = t.choice_set.all()
    context = {
        "t":t,
        "cset":c
    }
    return render(request, "vote/detail.html", context)

# Create your views here.
def index(request):
    page = request.GET.get("page", 1)
    t = Topic.objects.all()
    pag = Paginator(t, 6)
    obj = pag.get_page(page)
    t = t.order_by('-pubdate')
    context = {
        "tset" : obj
    }
    return render(request, "vote/index.html", context)