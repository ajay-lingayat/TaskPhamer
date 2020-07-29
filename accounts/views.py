from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
import random
from Designer.models import otp_verification
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.db import connection

cursor = connection.cursor()

def register( request ):
	cursor = connection.cursor()
    if request.method == "POST":

       username = request.POST["username"]
       email = request.POST["email"]
       password1 = request.POST["password1"]
       password2 = request.POST["password2"]

       if password1 == password2:
          if User.objects.filter(username=username).exists():
             messages.warning(request, 'Username Taken!')
             return redirect('register')
          elif User.objects.filter(email=email).exists():
             messages.warning(request, 'Email Taken!')
             return redirect('register')
          else:
             user = User.objects.create_user(username=username,password=password1,email=email)
             user.save()

             raw_query = f"CREATE TABLE {username.upper()}_DATA ( ID INT NOT NULL, CUSTOMER_NAME TEXT NOT NULL, TYPE TEXT NOT NULL, AMOUNT INT NOT NULL, ADD_DATE TEXT NOT NULL );"
             cursor.execute(raw_query)

             messages.success(request, "User Created Successfully!")
             return redirect('login')
       else:
          messages.warning(request, "Password does not match!")
          return redirect('register')
    else:
       return render(request, 'TaskPhamer/register.html')

def login( request ):
    if request.method == "POST":
       username = request.POST["username"]
       password = request.POST["password"]

       user = auth.authenticate(username=username,password=password)

       if user is not None:
          auth.login(request, user)
          return redirect('/')
       else:
          messages.warning(request, "Invalid Credentials!")
          return redirect('login')
    else:
       return render(request, 'TaskPhamer/login.html')

def logout( request ):
    auth.logout(request)
    return redirect('/')

def find_account( request ):
    if request.method == "POST":
       username_or_email = request.POST["username_or_email"]

       user = False
       email = False
       mail = False

       if User.objects.filter(username=username_or_email):
          user = username_or_email
       elif User.objects.filter(email=username_or_email):
          email = username_or_email
       else:
          messages.warning(request, "Account Not Found!")
          return redirect('password-reset')

       if user:
          mail = User.objects.get(username=user).email
       elif email:
          mail = email
          user = User.objects.get(email=email).username

       num = random.sample('123456789987654321',6)
       otp = ''
       for i in num:
           otp+=i
       otp = int(otp)
       print(otp)

       Found = False

       if otp_verification.objects.filter(email=mail).exists():
          obj = otp_verification.objects.get(email=mail)
          obj.otp = otp
          obj.save()
       else:
          obj = otp_verification(otp=otp,email=mail)
          obj.save()

       try:
          subject = f"TaskPhamer Password Reset OTP [{otp}]"
          From = "taskphamer@gmail.com"
          To = mail
          text_content = f"Hello {user},\nHere is your TaskPhamer pasword reset OTP - {otp}"
          html_content = """\
              <html lang="en-US">
                  <head>
                     <style>
                           html, body{
                              height: 100%;
                              margin: 0;
                              padding: 0;
                           }
                           .box{
                              margin-left: 10%;
                              margin-top: 20px;
                              background-color: #4da3ef;
                              color: #fff;
                              border: 0;
                              box-shadow: 2px 2px #999;
                              width: 80%;
                           }
                           button{
                              font-size: 20px;
                              border: 0;
                              background-color: #ff0066;
                              color: #fff;
                              padding: 15px 15px;
                              margin-bottom: 10px;
                              outline: none;
                              border-radius: 4px;
                           }
                     </style>
                  </head>
                  <body>
                     <div class="box">
                           <br>
                           <center>
                              <h1>
                                 Hello """+ user +"""\
                              </h1>
                              <h3>
                                 Here is your Taskphamer password reset OTP
                              </h3>
                              <button>
                                 <label>
                                       """+ f"{otp}" +"""\
                                 </label>
                              </button>
                           </center>
                     </div>
                  </body>
               </html>
              """
          msg = EmailMultiAlternatives(subject, text_content, From, [To])
          msg.attach_alternative(html_content, 'text/html')
          msg.send()
          messages.success(request, "Mail Sent Successfully!")
          return redirect('password-reset')
       except Exception as e:
          print(e)
          messages.warning(request, "Error occured while sending the mail!")
          return redirect('find-account')
    else:
       return render(request, 'TaskPhamer/find_account.html')

def password_reset( request ):
    if request.method == "POST":
       otp = request.POST["otp"]
       password1 = request.POST["password1"]
       password2 = request.POST["password2"]

       if otp_verification.objects.filter(otp=otp).exists():
          email = otp_verification.objects.get(otp=otp).email
          if password1 == password2:
             user = User.objects.get(email=email)

             hasher = PBKDF2PasswordHasher()
             newpassword = hasher.encode(password=password1, salt='salt',iterations=50000)

             user.password = newpassword
             user.save()
             messages.success(request, "Password Changed Successfully!")
             return redirect('login')
          else:
            messages.warning(request, "Password does not match!")
            return redirect('password-reset')
       else:
          messages.warning(request, 'Invalid OTP!')
          return redirect('password-reset')
    else:
       return render(request, 'TaskPhamer/password_reset.html')