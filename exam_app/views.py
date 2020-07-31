from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from datetime import datetime
from .models import User, Thought
from django.http import Http404
import bcrypt

def index(request):
    return render(request, "index.html") 



def login(request):
    userEmail = User.objects.filter(email=request.POST['email'])
    print(request.POST)
    pass1 = False
    emai1 = False

    if userEmail:
        emai1 = True
        logged_user = userEmail[0]
        password_check = bcrypt.checkpw(
            request.POST['password'].encode(), logged_user.password.encode())
        if password_check:
            pass1 = True
            request.session['userid'] = logged_user.id
            request.session['login'] = True
            return redirect('/thoughts')
    context = {
        'password': pass1,
        'email': emai1
    }
    errors = User.objects.login_validator(context)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
    return redirect('/')


def register(request):
    errors = User.objects.register_validator(request.POST)
    print(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        registered_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw_hash)
        request.session['userid'] = registered_user.id
        request.session['register'] = True
        return redirect('/thoughts')
    return redirect('/')


def logout(request):
    if request.session['userid']:
        request.session['userid'] = None
        request.session['register'] = False
        request.session['login'] = False
        return redirect('/')
    else:
        raise Http404("NOT ALLOWED")
    

############### THOUGHT AREA

######### PAGES ############
def thought_page(request):
    if request.session['userid']:
        user_id = request.session['userid']
        user = User.objects.get(id=user_id)
        thought = Thought.objects.all().order_by('-more_like')
        context = {
            "user": user,
            "thoughts": thought
        }
        return render(request, "main.html", context)
    else:
        raise Http404('Thats a No No')



def detail_page(request, id):
    if request.session['userid']:
        t_id = int(id)
        user_id = request.session['userid']
        user = User.objects.get(id=user_id)
        users = User.objects.all()
        t_id = int(id)
        thought = Thought.objects.get(id=t_id)
        thoughts = Thought.objects.all()
        like_thought = Thought.objects.first().likes.exclude(first_name=thought.thought_by.first_name)
        user_liked = Thought.objects.first().likes.filter(first_name=thought.thought_by.first_name)
        context = {
            "user": user,
            "users": users,
            "thought": thought,
            "userby_liked": user_liked,
            "users_liked": like_thought
        }
        return render(request, "detail.html", context)
    else:
        raise Http404('Thats a No No')


######### BUTTONS ############
def delete(request, id):
    if request.session['userid']:
        t_id = id
        Thought.objects.get(id=t_id).delete()
        return redirect('/thoughts')
    else:
        raise Http404('Thats a No No')



def like(request, id):
    if request.session['userid']:
        t_id = int(id)
        user_id = request.session['userid']
        this_user = User.objects.get(id=user_id)
        thought = Thought.objects.get(id=t_id)
        thought.likes.add(this_user)
        thought.more_like += 1
        thought.save()
        return redirect('/thoughts')
    else:
        raise Http404('Thats a No No')



def unlike(request, id):
    if request.session['userid']:
        t_id = int(id)
        user_id = request.session['userid']
        this_user = User.objects.get(id=user_id)
        thought = Thought.objects.get(id=t_id)
        thought.likes.remove(this_user)
        thought.more_like -= 1
        thought.save()
        return redirect('/thoughts')
    else:
        raise Http404('Thats a No No')


######### POST REQUEST ############
def add(request):
    if request.session['userid']:
        errors = User.objects.thought_validator(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
            return redirect('/thoughts')
        else:
            id = request.session['userid']
            user = User.objects.get(id=id)
            desc = request.POST['desc']
            thought = Thought.objects.create(
                desc=desc,
                thought_by=user,
                more_like=0)
            return redirect('/thoughts')
    else:
        raise Http404('Thats a No No')








