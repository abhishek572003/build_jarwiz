from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, get_user_model, login, logout 
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, FileResponse
from .models import *
import os
from pathlib import Path
from django.conf import settings
from subplatform.settings import MEDIA_ROOT, BASE_DIR
from django.core.files.storage import FileSystemStorage
import datetime
import shutil
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import CustomUser
from .forms import FilesForm
from django.contrib.auth.decorators import login_required
from .uploadfile import *
from .getAdditionalTags import *
from .fetchDocuments import *





@csrf_protect
def signup_view(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_str = request.POST.get('email', 'default user')  # use a new variable for email string
        phonenum = request.POST.get('phoneInput')
        phonecode = request.POST.get('countrySelect')
        phonenumber = (str(phonecode.replace('+', '')) + phonenum)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = email_str.replace('@', '')

        # Check if a user with the given email or phone already exists
        if User.objects.filter(email=email_str).exists() or User.objects.filter(phone=phonenumber).exists():
            messages.error(request, "A user with this email or phone number already exists.")
            return render(request, 'account/signup.html', {'form': form})
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'account/signup.html', {'form': form})

        user = User.objects.create_user(
            username=username,
            email=email_str,
            phone=phonenumber,
            first_name=first_name,
            last_name=last_name,
            password=password1
        )
        user_email = EmailAddress.objects.create(user=user, email=email_str)  # renamed the variable for clarity
        user_email.save()
        phone = PhoneNumber.objects.create(
            user = user, phone_number = phonenumber,phoneis_verified = True,
        )
        phone.save()
        current_site = get_current_site(request)
        subject = "Verify Email"
        message = render_to_string('account/verify_email_message.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        email_msg = EmailMessage(subject, message, to=[user_email.email])  # corrected to use the email field of the EmailAddress object
        email_msg.send()
        endpoint_url = 'https://build.myjarwiz.com/send_whatsappnotify/'
        whatsapp_message = "Thank you registering on our website !!!"
        
        # Data to be sent in the POST request
        data = {
            'phone_number': phonenumber,
            'message_content': whatsapp_message
        }
        
        # Make the POST request
        response = requests.post(endpoint_url, data=data)
        
        # Check the response
        if response.status_code == 200:
            print("POST request successful")
        else:
            print("POST request failed")
        login(request, user)
        return redirect('landing')  # Assume there is a URL named 'landing' to redirect to after signup

    else:
        form = CreateUserForm()
        return render(request, 'account/signup.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        print("user: ", user)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return render(request, 'account/index.html')
        else:
            messages.error(request, 'Log in Fail')
    return render(request, 'account/my-login.html')
# so we can reference the user model as User instead of CustomUser

@csrf_exempt
def send_whatsapp_message(request):
    if request.method == "POST":
        # Extract phone number and message text from the request
        phone_number = request.POST.get('phone_number')
        message_content = request.POST.get('message_content')
        print("hello world")
        print(phone_number)
        print(message_content)
        print("bijbidjbjakd")


        # Check if phone number and message content are provided
        if not phone_number or not message_content:
            return JsonResponse({"error": "Phone number and message content are required."}, status=400)

        # Construct the message body
        message_body = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message_content
            }
        }

        # Your Facebook Access Token
        access_token = 'EAAF35c3SkigBO3iNUPxlxEYpk0zSwriv5iLi79giNqDOyz7u5t86AWfmVEEZArGLfg25uDS2SJ6AD7VOIkXeIOXyxaBHIjQn9poGZArKG4tZAZBJjmmQMQZCnz9pdNprQo4pYWEdqwyOATOiKwPmVpxHGMmtntRBQO4H2Ez1zT5qqPbquUPuhY0TehAPt02FC'

        # Make the POST request to send the message
        url='https://graph.facebook.com/v18.0/244045088793951/messages'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer EAAF35c3SkigBO3iNUPxlxEYpk0zSwriv5iLi79giNqDOyz7u5t86AWfmVEEZArGLfg25uDS2SJ6AD7VOIkXeIOXyxaBHIjQn9poGZArKG4tZAZBJjmmQMQZCnz9pdNprQo4pYWEdqwyOATOiKwPmVpxHGMmtntRBQO4H2Ez1zT5qqPbquUPuhY0TehAPt02FC'  # Use GITHUB_ACCESS_TOKEN here
        }
        response = requests.post(url, headers=headers, data=json.dumps(message_body))
        for attr in dir(response.text):
            print(attr)
        # print(response.__attri__)
        # Check if the message was sent successfully
        if response.status_code == 200:
            return JsonResponse({"message": "Message sent successfully."}, status=200)
        else:
            return JsonResponse({"error": f"Failed to send message: {response.text}"}, status=response.status_code)

    else:
        print("nahi huaaa")
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)


User = get_user_model()
# send email with verification link
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_verfified = True
        user.save()
        return render(request, 'account/index.html') 
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'account/index.html')

def home(request):
    return render(request, 'account/index.html')

def faq(request):
    return render(request, 'account/faq.html')

def about(request):
    return render(request, 'account/about.html')

def user_logout(request):
    logout(request)
    return render(request, 'account/index.html')

def landing(request):
    return render(request,'account/landing.html')



def terms(request):
    return render(request, 'account/terms_and_conditions.html')

@login_required
def profile(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        emailform = UserEmailForm(request.POST)
        if form.is_valid():
            phonenum = form.cleaned_data['phone_number']
            phonecode=request.POST.get('countrySelect')
            phone_number=(str(phonecode.replace('+', ''))+phonenum)
            if not phonenum.isdigit():
                messages.error(request,"Please Enter Numerical Number")
            elif len(phonenum) < 10:
                messages.error(request, "Phone number must be at least 10 digits long.")
            elif PhoneNumber.objects.filter(phone_number=phone_number).exists():
                messages.error(request,"This phone number is already taken by another user.")
            else:
                phone = PhoneNumber.objects.create(
                    user = request.user, phone_number = phone_number,
                )
                phone.save()
                endpoint_url = 'https://build.myjarwiz.com/send_whatsappnotify/'
                whatsapp_message = "Thank you registering on our website !!!"
                
                # Data to be sent in the POST request
                data = {
                    'phone_number': phone_number,
                    'message_content': whatsapp_message
                }
                
                # Make the POST request
                response = requests.post(endpoint_url, data=data)
                return redirect('profile') 
        if emailform.is_valid():
            email = emailform.cleaned_data['email']
            if EmailAddress.objects.filter(email=email).exists():
                messages.error(request,"This email is already taken by another user.")
            else:
                email_instance = emailform.save(commit=False)
                email_instance.user = request.user
                email_instance.save()
                messages.success(request,"Email ID added Sucessfully")
                return redirect('profile')  
    print("get request ha")
    user = request.user
    phone_numbers = user.phone_numbers.all()
    user_emails = user.email_addresses.all()
    form = PhoneNumberForm()
    emailform = UserEmailForm()
    context = {'user': user, 'phone_numbers': phone_numbers,'form':form,'emailform':emailform,'user_emails':user_emails}
    return render(request, 'account/profile.html', context)

def fileupload(request):
    form = FilesForm(request.FILES)
    if request.method == 'POST':
        inpfile = request.FILES.get('file')
        fname = inpfile.name
        username = request.user.get_username()
        path = os.path.join(MEDIA_ROOT, username)
        information = uploadfiles(fname, username, inpfile, path)
        request.session['tags'] = information[0]  # Store tags in session
        request.session['filename'] = information[1]  # Store filename in session
        DocumentRecord = UploadedDocuments()
        DocumentRecord.username = request.user
        DocumentRecord.newfilename = information[1]
        DocumentRecord.filename = fname
        DocumentRecord.path = information[2]
        DocumentRecord.extension = information[3]
        DocumentRecord.tags = information[0]
        DocumentRecord.save()
        return redirect('gettags')
    context = {'form': form}
    return render(request, "account/upload.html", context)


def gettags(request):
    # Initialize default values if the session keys do not exist
    tags = request.session.get('tags', 'No tags available')
    filename = request.session.get('filename', 'No filename available')

    form = AddTags(request.POST)
    if request.method == 'POST':
        addtags = request.POST.get('tags')
        
        getadditionaltag(addtags, filename)
        # Optionally update the tags in the session if changed
        request.session['tags'] = addtags  # Only if addtags modifies the tags meaningfully
        return redirect('home')
    return render(request, "account/fileindex.html", {'tags': tags})




@csrf_exempt
def check_user_existence(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        phone_number = data.get('phone_number', None)

        if phone_number:
            user_exists = PhoneNumber.objects.filter(phone_number=phone_number).exists()

            response_data = {'exists': user_exists}
            return JsonResponse(response_data)
        else:
            # If phone number is not provided in the request data
            response_data = {'error': 'Phone number is missing'}
            return JsonResponse(response_data, status=400)
    else:
        # If request method is not POST
        response_data = {'error': 'Only POST method is allowed'}
        return JsonResponse(response_data, status=405)


def delete_phone_number(request, pk):
    phone_number = PhoneNumber.objects.get(pk=pk)
    if phone_number.user == request.user:
        phone_number.delete()
        messages.success(request,"Number Deleted Sucessfully")

    return redirect('profile')  

def delete_email(request, pk):
    email = EmailAddress.objects.get(pk=pk)
    if email.user == request.user:
        email.delete()
        messages.success(request,"Email ID Deleted Sucessfully")

    return redirect('profile') 

@csrf_protect
def fetch(request):
    if request.method == "POST":
        tag = request.POST.get('tag')
        username = request.user.get_username()
        # Establish a connection to the database
        fetchinformation=fetchdocument(tag, username)
        newpaths=fetchinformation[1]
        foundext = fetchinformation[0]
        return render(request, "account/searchresults.html", {'newpaths': newpaths, 'foundext': foundext})
    return render(request, "account/fetch.html")