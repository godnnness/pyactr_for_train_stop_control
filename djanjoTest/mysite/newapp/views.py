from django.shortcuts import render
from .models import *
# Create your views here.
def zhuce(request):
    if request.methon=="POST":
        zc=Zhuce()
        zc.user=request.POST.get('user')
        zc.pwd=request.POST.get('pwd')
        zc.save()
        return render(request,'newapp/show.html',{})
    else:
        return render(request,'newapp/add.html',{})