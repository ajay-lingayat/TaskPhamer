from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db import connection
from django.template import loader
import datetime

cursor = connection.cursor()

def index( request ):
       return render(request, 'TaskPhamer/index.html')

def contact( request ):
    if request.method == 'POST':
       
       fullname = request.POST['fullname']
       email = request.POST['email']
       message = request.POST['message']

       try:
          subject = f"TaskPhamer - A message for You!"
          From = "taskphamer@gmail.com"
          To = 'lingayatajay2810@gmail.com'
          text_content = f"Hey Ajay,\n{fullname} has sent you a message!\n\nFullname : {fullname}\nEmail Address : {email}\nMessage : {message}"
          html_content = f"""\
              <html>
                  <body>
                       <h1>
                           Hey Ajay,
                       </h1>
                       <h2>
                           {fullname} has sent you a message!
                       </h2>
                       <h4>
                           Fullname : {fullname}<br>
                           Email Address : {email}<br>
                           Message : {message}
                       </h4>
                  </body>
              </html>
              """
          msg = EmailMultiAlternatives(subject, text_content, From, [To])
          msg.attach_alternative(html_content, 'text/html')
          msg.send()
          messages.success(request, 'Mail Sent Successfully!')
          return redirect('contact')
       except:
          messages.warning(request, 'Please Check Your Internet Connection!')
          return redirect('contact')
    else:
       return render(request, 'TaskPhamer/contact.html')

def add_data( request ):
    if request.method == "POST":
       customer_name = request.POST['customer-name']
       amount = request.POST['amount']
       Type = request.POST['credit_or_debit']
       Type = Type.lower()

       username = False

       if request.user.is_authenticated:
          username = request.user.username
          username = username.upper()

       try:
          if username:
             raw_query = f"INSERT INTO {username}_DATA ( CUSTOMER_NAME, TYPE, AMOUNT ) VALUES ( \'{customer_name}\', \'{Type}\', \'{amount}\' );"
             cursor.execute(raw_query)
       except:
          print('Data not inserted!')

       return redirect('/')
    else:
       return redirect('/')

def delete_data( request, data_index ):
    if request.user.is_authenticated:
       username = request.user.username
       username = username.upper()

       raw_query = f"DELETE FROM {username}_DATA WHERE ID = {data_index};"
       cursor.execute(raw_query)
       return redirect('/')
    else:
       return redirect('/')

def edit_data( request ):
    if request.method == "POST":
       if request.user.is_authenticated:
          username = request.user.username
          username = username.upper()

          customer_name = request.POST['customer-name']
          amount = request.POST['amount']
          debit_or_credit = request.POST['credit_or_debit']
          debit_or_credit = debit_or_credit.lower()
          ID = request.POST['data-id']

          raw_query = f"UPDATE {username}_DATA SET CUSTOMER_NAME = \'{customer_name}\', TYPE = \'{debit_or_credit}\', AMOUNT = {amount}, ADD_DATE = DEFAULT WHERE ID = {ID};"
          cursor.execute(raw_query)
          return redirect('/')
       else:
          return redirect('/')
    else:
       return redirect('/')

def generate_pdf( request ):
    if request.user.is_authenticated:
       username = request.user.username
       username = username.upper()

       raw_query = f"SELECT * FROM {username}_DATA;"
       cursor.execute(raw_query)
       List = cursor.fetchall()

       current_time = datetime.datetime.now()
       Day = current_time.day
       Month = current_time.month
       Year = current_time.year
       Hour = current_time.hour
       Minute = current_time.minute

       current_time = f"{Day}/{Month}/{Year} 0{Hour}:{Minute}"

       total_debit = 0
       total_credit = 0
       for i in List:
           if i[2] == 'debit':
              total_debit += int(i[3])
           else:
              total_credit += int(i[3])

       generate_time = current_time
       transactions = len(List)

       deb = "debit"
       cred = "credit"

       context = {
          'generate_time': generate_time,
          'transactions': transactions,
          'total_debit': total_debit,
          'total_credit': total_credit,
          'List': List,
          'deb': deb,
          'cred': cred,
       }
       t = loader.get_template('generate_pdf.html')

       return HttpResponse(t.render(context, request))
    else:
       return redirect('/')

def about( request ):
    return render(request, 'TaskPhamer/about.html')