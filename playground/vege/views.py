from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages                 #this is used to send messages to the html page
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator         #this used to use page functionality
from django.db.models import Q, Sum             #this 'Q' is used in place or condition in django
from django.contrib.auth import  get_user_model     

User = get_user_model()

# Create your views here.
@login_required(login_url = "/login/")
def receipes(request):

    if request.method == "POST":
        data = request.POST
        rn = data.get('receipe_name')
        rd = data.get('recipe_discription')
        ri = request.FILES.get("receipe_image")

        Receipe.objects.create(
            receipe_name = rn,
            receipe_discription = rd,
            receipe_image = ri
        )

        return redirect("/receipes/")

    queryset = Receipe.objects.all()


    # Search Block
    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))



    context = {'receipes' : queryset}
    return render(request, "receipes.html", context)


@login_required(login_url = "/login/")
def update_receipe(request, id):

    queryset = Receipe.objects.get(id = id)

    if request.method == "POST":
        data = request.POST
        rn = data.get('receipe_name')
        rd = data.get('recipe_discription')
        ri = request.FILES.get("receipe_image")

        queryset.receipe_name = rn
        queryset.receipe_discription = rd

        if ri:
            queryset.receipe_image = ri

        queryset.save()

        return redirect("/receipes/")


    context = {'receipe': queryset}
    return render(request, "update_receipe.html", context)


@login_required(login_url = "/login/")
def delete_receipe(request, id):

    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    return redirect('/receipes/')


def login_page(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')   

        if not User.objects.filter(username = username).exists():
            messages.error(request, "Invalid username")
            return redirect('/login/')
        
        user = authenticate(username = username, password = password)
        
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        
        else:
            login(request, user)
            return redirect('/receipes/')

    return render(request, 'login.html')


def logout_page(request):

    logout(request)
    return redirect('/login/')


def register(request):

    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.error(request, "Username already exist")
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email
        )

        user.set_password(password)
        user.save()

        messages.info(request, "Account created successfully")

        return redirect('/login/')

    return render(request, 'register.html')


def get_students(request):
    queryset = Student.objects.all()


    if request.GET.get('search'):
        search = request.GET.get('search')
        queryset = queryset.filter(                                         #applying 'or' condition using Q
            Q(student_name__icontains = search) |
            Q(department__department__icontains = search) |
            Q(student_id__student_id__icontains = search) |
            Q(student_email__icontains = search) 
        )

        paginator = Paginator(queryset,len(queryset))
    else:

        paginator = Paginator(queryset,25)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'report/students.html', {'page_obj' : page_obj})
    
def see_marks(request, student_id):
    queryset = SubjectMarks.objects.filter(student__student_id__student_id__icontains = student_id)
    total_marks = queryset.aggregate(total_marks = Sum('marks'))
    
    return render(request, "report/marks.html", {'queryset' : queryset, 'total_marks' : total_marks})