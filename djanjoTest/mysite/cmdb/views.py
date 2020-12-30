from django.shortcuts import render
from cmdb import models
from django.shortcuts import HttpResponse

# Create your views here.
# user_list=[
#     {"user":"sunyulong","pwd":"123456"},
#     {"user":"sunxingzhe","pwd":"2342423"},
# ]
def index(request):
    # return HttpResponse("herello world")
    if request.method=="POST":
            username=request.POST.get("username",None)
            password=request.POST.get("password",None)
            models.UserInfo.objects.create(user=username,pwd=password)
            # temp={"user":username,"pwd":password}
            # user_list.append(temp)
            # print(username,password)
    user_list=models.UserInfo.objects.all()
    return render(request,"index.html",{"data":user_list})
