from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def take_to_main(request):
    return redirect('/main')

def main(request):
    return render(request, "main.html")

### LOG&REG
## CREATE

def register(request):
    ## Create a user!
    if request.method=='POST':
        ## validate our data
        errors=User.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        ## Creating the new user
        new_user=User.objects.create(
            first_name=request.POST['f_n'],
            last_name=request.POST['l_n'],
            email=request.POST['email'],
            password=request.POST['password'])
        ## storing new user data in session
        request.session['user_id']=new_user.id
        request.session['name']=f"{new_user.first_name} {new_user.last_name}"
        return redirect('/groups')

## FETCH

def login(request):
    if request.method=='POST':
        ## filter for a user using the submitted email
        logged_user=User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            if logged_user.password == request.POST['password']:
                request.session['user_id']=logged_user.id
                request.session['name']=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/groups')
            else:
                messages.error(request, "Incorrect Password.")
        else:
            messages.error(request, "Email does not exist.")
    return redirect('/')

## LOGOUT

def logout(request):
    request.session.clear()
    return redirect('/')

## GROUPS

def groups(request):
    context={
        'all_groups': Org.objects.all()
    }
    return render(request, "groups.html", context)

def groups_partial(request, group_id):
    context={
        'group':Org.objects.get(id=group_id) 
    }
    return render(request, "group_partial.html", context)

## CREATE

def create_org(request):
    if request.method=='POST':
        ## validate the data
        errors=Org.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/groups')
        new_group=Org.objects.create(name=request.POST['name'], description=request.POST['description'], location=request.POST['location'], creator=User.objects.get(id=request.session['user_id']))
        print(new_group)
        new_group.members.add(User.objects.get(id=request.session['user_id']))
        return redirect(f'/groups_partial/{new_group.id}')
    return redirect('/groups')

## ONE GROUP

def one_group(request, group_id):
    context={
        'group':Org.objects.get(id=group_id),
        'user':User.objects.get(id=request.session['user_id'])
    }
    return render(request, "one_group.html", context)

## MANY_TO_MANY

def add_member(request, group_id):
    new_member=User.objects.get(id=request.session['user_id'])
    group=Org.objects.get(id=group_id)
    group.members.add(new_member)
    return redirect(f'/groups/{group_id}')

def remove_member(request, group_id):
    new_member=User.objects.get(id=request.session['user_id'])
    group=Org.objects.get(id=group_id)
    group.members.remove(new_member)
    return redirect(f'/groups/{group_id}')
