from django.shortcuts import get_object_or_404
from django .shortcuts import render,redirect
from django.contrib.auth.models import User
from todo import model
from todo.model import TODOO
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate,login,logout

def signup(request):
    if request.method=="POST":
       firstname=request.POST.get('first-name')
       surname=request.POST.get('surname')
       emailid=request.POST.get("email")
       password=request.POST.get("password")
       print(firstname,emailid,password)
       my_user = User.objects.create_user(firstname,emailid,password)
       my_user.save()
       return redirect('/login')


    return render(request,'signup.html')

def login(request):
    if request.method == "POST":
        firstname = request.POST.get('fnm')
        password = request.POST.get('pwd')
        user = authenticate(request, username=firstname, password=password)
        if user is not None:
            auth_login(request, user)   # ← must say auth_login, not login
            return redirect('/todopage/')
        else:
            return redirect('/login/')
    return render(request, 'login.html') 


@ login_required(login_url=("/login"))
def todo(request):
    if request.method == "POST":
        title = request.POST.get('title')
        model.TODOO(title=title, user=request.user).save() #save the object
        res = model.TODOO.objects.filter(user=request.user).order_by('-date')
        return redirect('/todopage',{'res':res})
    res = model.TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': res, 'user': request.user})



@ login_required(login_url=("/login"))
def edit_todo(request, srno):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj = model.TODOO.objects.get(srno=srno)
        obj.title = title
        obj.save()
        return redirect('/todopage')

    obj = model.TODOO.objects.get(srno=srno)
    return render(request, 'edit_todo.html', {'obj': obj})


@ login_required(login_url=("/login"))
def delete_todo(request,srno):
    obj=model.TODOO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')

def signout(request):
    logout(request)
    return redirect('/login/')

