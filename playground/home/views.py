from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .utils import send_email_to_client, send_email_with_attachment
from django.conf import settings

# Create your views here.

def send_email(request):

    # send_email_to_client()
    # return redirect("/")

    subject = "Django Test Mail"
    message = "This is a test mail sent you from django server email."
    recipient_list = ["karanpt168@gmail.com"]
    file_path = f"{settings.BASE_DIR}/test.txt"
    send_email_with_attachment(subject, message, recipient_list, file_path)
    return redirect("/")




def home(request):

    peoples = [
        {'name' : "Karn Patel", 'age' : 28},
        {'name' : "Sidharth Singh", 'age' : 29},
        {'name' : "Abhinav Singh Tomar", 'age': 27},
        {'name' : "Suchit Patel", 'age' : 30},
        {'name' : "Adarsh Srivastava", 'age' : 34},
        {'name' : "Shivam Verma", 'age': 30}
    ]

    return render(request, "index.html", context={'peoples':peoples, 'page' : 'Home'})

def about(request):

    context = {'page' : 'About'}

    return render(request, "about.html", context)

def contact(request):

    context = {'page' : 'Contact'}
    return render(request, "contact.html", context)