from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage



def activate_user(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except( ValueError):  
        user = None
    if user and generate_token.check_token(user,token):
        user.is_verified = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:
        return render(request, 'account/user/authentication/activate-failed.html',{'user':user})

def send_verification_mail(request,user): 
    try:       
        current_site    = get_current_site(request)
        email_subject   = 'Activate your account'
        email_body      = render_to_string('account/user/authentication/activate.html',{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':generate_token.make_token(user),
        })
        to_email = user.email 
        email = EmailMessage(  
                email_subject, email_body, to=[to_email]  
        )
        
        email.send()  
        
    except:
        print('verification mail failed!')

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
          
            user.is_verified = False
            user.set_password(user.password)
            user.save()
            
            send_verification_mail(request,user)
            return render(request, 'account/user/authentication/send-msg.html',{'user':user})     
        else:
            messages.error(request, 'Invalid credentials..')
    else:
        form = RegistrationForm()
    context = {
        'form' : form
    }
    return render(request, 'account/user/register.html',context)



def login_user(request):
    
    if request.user.is_authenticated:
        return redirect('store:user-home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email = email, password = password)
        print(user)
        # # emails = []
        
        # # for e in Account.objects.filter(is_admin=False):
        # #     emails.append(e.email)
        # if email in emails:
        #     print('email exist')
        #     user = Account.objects.get(email=email)
        #     if password == user.password:
        if user is not None:
            if user.is_verified:
                login(request,user)
                return redirect('store:user-home')
            else:
                messages.error(request, 'Email is not verified. Please check your inbox..')
           
        else:
            messages.error(request, 'user is blocked by admin please contact')        
    return render(request,'account/user/login.html')

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('user:login-user')