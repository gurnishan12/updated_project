from re import T
import re
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from pyrebase.pyrebase import Database
from .models import  complaintregister,notesaddcse,notesaddece,loginC,notesaddauto,notesaddcivil,notesaddelectrical,notesaddmechanical,teachers
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from .models import complaintregister,complaintregister_verification,City,Country,trades_and_data,checking_tradesemsubject
from PIL import Image
import os
import time
import math
import random
import uuid
import glob
import shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import mysql.connector
from django.contrib.auth import logout
from django.http import JsonResponse
import importlib
connection = mysql.connector.connect(host='localhost',
                                                                database='major',
                                                                user='root',
                                                                password='')
def index(request):
    return render(request, "index.html")

def homepage(request):
    return render(request, "index.html")

def homepage_admin(request):
    return render(request, "loginAdmin.html")

   

def complain_register(request):
            
    if request.method == 'POST':
        name = request.POST['name']
        rollno = request.POST['rollno']
        phoneno = request.POST['phoneno']
        description = request.POST['description'] 
        email = request.POST['email']
        
        values = {
            'name': name,
            'rollno': rollno,
            'phoneno': phoneno,
            'description': description,
            'email': email,
        }
        
        error_message = None
        
        if not name:
            error_message = 'Username Required'
            

        elif len(phoneno) != 10:
            error_message = 'Phone number is not'
            
        elif len(rollno) != 12:
            error_message = 'Registeration number is not valid valid'
            
        elif len(description) > 100:
            error_message = 'Description  must be less then 100 character '
            
        # elif complaintregister.objects.filter(email=email).exists():
        #     messages.info(request,'Email Taken')
        #     return redirect('complain_register')
       
        if not error_message:
            
            pic =request.FILES.getlist('image')
            
            
            for i in pic:
               
                digits = [x for x in range(0, 10)]
                random_str = ""
                for x in range(6):
                    index = math.floor(random.random() * 10)
                    random_str += str(digits[index])
                token_code = str(uuid.uuid4())
                user = complaintregister(name=name,rollno=rollno,phoneno=phoneno,verification_code=random_str,email=email,description=description,image=i)
                ## storing strings in a list
                
                
                user_complaintregister_verification = complaintregister_verification(name=name,verification_code=random_str,verification_status=0,token_code=token_code)
                
                request.session['random_str'] = random_str
                
               
                user_complaintregister_verification.save()
                
                user.save()
            
            email_user = 'helplinegndpcollege@gmail.com'
            email_password = 'helplinegndpcollege12345'
            email_send = 'gurnishansingh366@gmail.com'
            
            subject = 'subject'

            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_send
            msg['Subject'] = subject
            
            body = 'Description: '+ description +  ' Hi teacher, Please verify by clicking this link http://127.0.0.1:8000/verification_after_mail/' + token_code
            print(body)
            print(token_code)
            msg.attach(MIMEText(body,'plain'))
            try:
                connection = mysql.connector.connect(host='localhost',
                                                        database='major',
                                                        user='root',
                                                        password='')

                sql_select_Query = ("select * from calc_complaintregister where verification_code ='%s'" % random_str)
               
                cursor = connection.cursor()
                cursor.execute(sql_select_Query)
                # get all records
                records = cursor.fetchall()
                
                for row in records:
                    filename = "media/"+row[7]


                    attachment  =open(filename,'rb')

                    part = MIMEBase('application','octet-stream')
                    part.set_payload((attachment).read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition',"attachment; filename= "+filename)

                    msg.attach(part)
                    text = msg.as_string()
                    server = smtplib.SMTP('smtp.gmail.com',587)
                    server.starttls()
                server.login(email_user,email_password)
                
                

                server.sendmail(email_user,email_send,text)
                
                server.quit()
                shutil.rmtree('C:/Users/gurnishan/Downloads/Compressed/mj/mj/media/img/2021/')

            except mysql.connector.Error as e:
                print("Error reading data from MySQL table", e)
            finally:
                if connection.is_connected():
                    connection.close()
                    cursor.close()
                    print("MySQL connection is closed")
                context = {}
                context['random_str'] = random_str 
                context['msg'] = "Dear, user this is your number of complain use this to see your progress "   
                 
                return render(request,'complain.html',context)     
        else:
            data = {
                'error': error_message,
                'values': values
                            }   
            print(data['values'])
            return render(request,'complain.html', data)
            
    else:
        return render(request,'complain.html')

def verification_start(request):
    if request.method == 'POST':
        code = request.POST['code']

        connection = mysql.connector.connect(host='localhost',
                                                database='major',
                                                user='root',
                                                password='')

        sql_select_Query = ("select * from calc_complaintregister_verification where verification_code ='%s'" % code)
        
        cursor1 = connection.cursor()
        cursor1.execute(sql_select_Query)
        # get all records
        records = cursor1.fetchall()
        print(records)
        
        if records:
            context = {
                    }
            
            
            print("we have reocrd")
            for row in records:
                data  = row[3]
                print(data)
                if data == '1':
                    print("status is  ", data)
                    context = {
                    }
                    context['verified'] = 2

                    
                    return render(request,'tracknext.html',context) 
                else:
                    context = {
                        # "verified" : 2
                    }
                    context['verified'] = 1

                    
                    return render(request,'tracknext.html',context)
        else:
            context = {
                        # "verified" : 2
                    }
            context['verified'] = 4 
            context['error'] = "we have no record"
            return render(request,'tracknext.html',context)
              
               

    else:
        return render(request,'track.html')


    # verification_code =  request.session['verification_code'] 
    # print(verification_code) 



def about_us(request):
    return render(request, "aboutus.html")

def track(request):
    return render(request, "track.html")

def tracknext(request):
    return render(request, "tracknext.html")

def verification_after_mail(request, name):
    data = name
    print(data)
    connection = mysql.connector.connect(host='localhost',
                                                        database='major',
                                                        user='root',
                                                        password='')
    
    # '%s'" % data
    sql_select_Query = ("select * from calc_complaintregister_verification where token_code = '%s'" % data)
    
    cursor1 = connection.cursor()
    cursor1.execute(sql_select_Query)
    # get all records
    records = cursor1.fetchall()
   
    for row in records:
        data  = row[2]
        print(data)
        sql_select_Query_update = ("update calc_complaintregister_verification set verification_status =1 where verification_code ='%s'" % data)
        print(sql_select_Query_update)
        cursor2 = connection.cursor()
        execute = cursor2.execute(sql_select_Query_update)
        print(execute)   
        print(cursor2.rowcount, "record(s) affected")  
        connection.commit()  
        return render(request,'complain.html')

def notes(request):
    return render(request, "notes.html")
def loginCC(request):
    return render(request, "loginC.html")
    


def nxt_notes(request):
    return render(request, "nxtnote.html")

def notes_verify(request):
    
    query = request.GET.get('data')
    
    request.session['query'] = query

    
    mod_string = query[8:]
    print(mod_string)
    combine_data =query[:query.index("_")]
    request.session['database'] = combine_data
    trade = mod_string[:mod_string.index("_")]
    print("here",trade)
    request.session['trade'] = trade
    h = query[query.index("sem"):]
    sem_value = h[3]
    print(sem_value)
    request.session['sem'] = h[3]
        
    print(combine_data)
    connection = mysql.connector.connect(host='localhost',
                                                        database='major',
                                                        user='root',
                                                        password='')
    query = ("select * from calc_" + combine_data + " where verificationstatus = 1 and sem ='%s'" % sem_value)
    print(query)
    
    cursor4 = connection.cursor()
    d = cursor4.execute(query)
    print(d)
    # get all records
    records_query = cursor4.fetchall()
    rowcount = cursor4.rowcount
    print(rowcount)
    if rowcount >=1:

        thislist = []
        thislist2 = []
        for row in records_query:
    
            thislist.append(row)
            
            context = { "thislist" : thislist,
                        "message": "NOTES"
                             }        
        
        
        
        return render(request,'nxtnote.html',context)
    else:
        context = {
            "message":"No Data found "

        }
        return render(request,'nxtnote.html',context)
        
def notes_register(request):
    database = request.session['database']
    print(database)
    trades = request.session['trade'] 
    print(trades)
    sem = request.session['sem']
    total = trades + sem
    print(total)
    
    
    connection = mysql.connector.connect(host='localhost',
                                                        database='major',
                                                        user='root',
                                                        password='')
    query = ("select * from calc_country where name =  '%s'" % total)
    print(query)
    
    cursor4 = connection.cursor()
    d = cursor4.execute(query)
    
    # get all records
    records_query = cursor4.fetchall()
    rowcount = cursor4.rowcount
    
    list = []
    for r in records_query:
        subject = r[0]
        
        query_for_subject = ("select * from calc_city where country_id =  '%s'" % subject)
        
        cursor5 = connection.cursor()
        d2 = cursor5.execute(query_for_subject)
        
        # get all records
        records_query2 = cursor5.fetchall()
        rowcount2 = cursor5.rowcount
        print(rowcount2)
        if rowcount2 >= 1:
            for x in records_query2:
                print("hi")
                print(x[1])
                subject_notes = x[1] 
                request.session['subject_notes'] = subject_notes
            data = {
                'cc' : x[1],
                'sem' : sem,
                'trades': trades,
                
            }
            return render(request, "notes_register.html",data)

        else:
            data = {
                'error': 'Currently no subject is present'
            }
            return render(request, "nxtnote.html",data)
    


def notes_register_here(request):

    if request.method == 'POST':
        name = request.POST['name']
        rollno = request.POST['rollno']
        phoneno = request.POST['phoneno']
        
        description = request.POST['description'] 
        email = request.POST['email']
        section = request.POST['section']
        notes_name = request.POST['notesname']
        print("hh")
        sem = request.POST['sem']
        print(sem)
        subject = request.POST['subject']
        print(subject)
        semester = request.session['sem']
        trades = request.session['trade']
        subject_notes = request.session['subject_notes']
        pic =request.FILES.getlist('image')
        values = {
            'name': name,
            'rollno': rollno,
            'phoneno': phoneno,
            'description': description,
            'email': email,
            'sem': semester,
            'trades': trades,
            'subject_notes': subject_notes,
            'section': section,
            'notes_name': notes_name,
            'subject': subject,
            
        }
        
        
        query = request.session['query']
        print(query)
        status = '0'
        digits = [i for i in range(0, 10)]
        random_str = ""
        for i in range(6):
            index = math.floor(random.random() * 10)
            random_str += str(digits[index])
        
        combine_data = query[:query.index("_")]   
        print(combine_data)
        
    
        connection = mysql.connector.connect(host='localhost',
                                                                database='major',
                                                                user='root',
                                                                password='')
        error_message = None
        if not name:
            error_message = 'Username Required'
            print(error_message)

        elif len(phoneno) != 10:
            error_message = 'Phone number is not'
            print(error_message)
        elif len(rollno) != 12:
            error_message = 'Registeration number is not valid valid'
            print(error_message)
        elif len(notes_name) > 20:
            error_message = 'please write short name'
            print(error_message)            
        elif len(description) > 100:
            error_message = 'Description  must be less then 100 character '
            print(error_message)
        # elif complaintregister.objects.filter(email=email).exists():
        #     messages.info(request,'Email Taken')
        #     return redirect('complain_register')
       
        if not error_message:
            if combine_data == 'notesaddcse':
                print("working")
                for i in pic:
                    note_save = notesaddcse(name=name,rollno=rollno,section=section,sem=sem,email_id=email,phone_no=phoneno,notes_name=notes_name,subject=subject,description=description,code=random_str,verificationstatus=status,image=i)
                    note_save.save()  
                    
                
                    print(random_str)
                    
                    print("workin")
                    
                    query = ("select * from calc_notesaddcse where code = '%s'" % random_str)
                    print(query)
                    cursor4 = connection.cursor()
                    print(cursor4)
                    d = cursor4.execute(query)
                    print(d)
                    # get all records
                    records_query = cursor4.fetchall()
                    
                    for row in records_query:
                        print(row)
                        print("here working")
                        data  = row[12]
                        print(data)
                        
                        config ={
                            "apiKey": "AIzaSyCKWWPehnuKB6Cz0dh4H0INunG3Lu4MnHs",
                            "authDomain": "gndpc-44049.firebaseapp.com",
                            "projectId": "gndpc-44049",
                            "databaseURL":"https://gndpc-44049-default-rtdb.firebaseio.com/",
                            "storageBucket": "gndpc-44049.appspot.com",
                            "messagingSenderId": "92108007781",
                            "appId": "1:92108007781:web:0dc3ed150b264bc632198c",
                            "measurementI": "G-5E1G72WKR8"
                        }
                        
                        firebase = pyrebase.initialize_app(config)
                        storage = firebase.storage()


                        path_on_cloud = data
                        print("wokring")
                        print(path_on_cloud)
                        select0 = path_on_cloud[0]
                        select1 = path_on_cloud[1]
                        print(select1)
                        select2 = path_on_cloud[2]
                        select3 = path_on_cloud[3]
                        
                        select4 = path_on_cloud[4]
                        select5 = path_on_cloud[5]
                        select6 = path_on_cloud[6]
                        select7 = path_on_cloud[7]
                        select8 = path_on_cloud[8]
                        select9 = path_on_cloud[9]
                        select10 = path_on_cloud[10]
                        select11 = path_on_cloud[11]
                        select12 = path_on_cloud[12]
                        select13 = path_on_cloud[13]
                        select14 = path_on_cloud[14]
                        select15 = path_on_cloud[15]
                        select16 = path_on_cloud[16]
                        select17 = path_on_cloud[17]
                        select18 = path_on_cloud[18]
                        select19 = path_on_cloud[19]
                        select20 = path_on_cloud[20]
                        select21 = path_on_cloud[21]
                        select22 = path_on_cloud[22] 
                        select23 = path_on_cloud[23] 
                        select24 = path_on_cloud[24] 
                        select25 = path_on_cloud[25] 
                        select26 = path_on_cloud[26] 
                    
                        
                        # v = i.name
                        total_of_select =select0 + select1+ select2+select3+select4+select5+select6+select7+select8+  select9 + select10 + select11 + select12 + select13 +  select14+ select15+ select16+ select17+ select18+ select19+ select20+ select21 + select22+ select23+ select24+ select25+ select26 
                        print("this is total")
                        print(total_of_select)
                        
                        
                                        

                        path_local = "media/" + data
                        
                        storage.child(path_on_cloud).put(path_local)
                        # storage.child(data).download(total_of_select,"img_note/correct.png")
                        auth = firebase.auth()
                        email = "helplinegndpcollege12345@gmail.com"
                        password = "helplinegndpcollege12345"
                        user = auth.sign_in_with_email_and_password(email, password)
                        url = storage.child(path_on_cloud).get_url(user['idToken'])
                        print(url)
                        query_again = "update calc_notesaddcse set image_url ='%s'" % url + "where code ='%s'" % random_str
                        print(query_again)
                        cursor6 = connection.cursor()
                        print(cursor6)
                        w = cursor6.execute(query_again)
                        print(w)
                        
                        connection.commit()
                        context = {

                        }
                        context['url'] = url
                        context['msg'] = "Your notes has been register wait for techer to verufy them"
                        request.session['url_session'] = url
                        print("working")
                        shutil.rmtree('C:/Users/gurnishan/Downloads/Compressed/mj/mj/media/img_note/2021/') 
                        return render(request,'notes_register.html',context)
            elif combine_data == 'notesaddece':
                print("working")
                for i in pic:
                    note_save = notesaddece(name=name,rollno=rollno,section=section,sem=sem,email_id=email,phone_no=phoneno,notes_name=notes_name,subject=subject,description=description,code=random_str,verificationstatus=status,image=i)
                    note_save.save()  
                    
                
                    print(random_str)
                    
                    print("workin")
                    
                    query = ("select * from calc_notesaddece where code = '%s'" % random_str)
                    print(query)
                    cursor4 = connection.cursor()
                    print(cursor4)
                    d = cursor4.execute(query)
                    print(d)
                    # get all records
                    records_query = cursor4.fetchall()
                    
                    for row in records_query:
                        print(row)
                        print("here working")
                        data  = row[12]
                        print(data)
                        
                        config ={
                            "apiKey": "AIzaSyCKWWPehnuKB6Cz0dh4H0INunG3Lu4MnHs",
                            "authDomain": "gndpc-44049.firebaseapp.com",
                            "projectId": "gndpc-44049",
                            "databaseURL":"https://gndpc-44049-default-rtdb.firebaseio.com/",
                            "storageBucket": "gndpc-44049.appspot.com",
                            "messagingSenderId": "92108007781",
                            "appId": "1:92108007781:web:0dc3ed150b264bc632198c",
                            "measurementI": "G-5E1G72WKR8"
                        }
                        
                        firebase = pyrebase.initialize_app(config)
                        storage = firebase.storage()


                        path_on_cloud = data
                        print("wokring")
                        print(path_on_cloud)
                        select0 = path_on_cloud[0]
                        select1 = path_on_cloud[1]
                        print(select1)
                        select2 = path_on_cloud[2]
                        select3 = path_on_cloud[3]
                        
                        select4 = path_on_cloud[4]
                        select5 = path_on_cloud[5]
                        select6 = path_on_cloud[6]
                        select7 = path_on_cloud[7]
                        select8 = path_on_cloud[8]
                        select9 = path_on_cloud[9]
                        select10 = path_on_cloud[10]
                        select11 = path_on_cloud[11]
                        select12 = path_on_cloud[12]
                        select13 = path_on_cloud[13]
                        select14 = path_on_cloud[14]
                        select15 = path_on_cloud[15]
                        select16 = path_on_cloud[16]
                        select17 = path_on_cloud[17]
                        select18 = path_on_cloud[18]
                        select19 = path_on_cloud[19]
                        select20 = path_on_cloud[20]
                        select21 = path_on_cloud[21]
                        select22 = path_on_cloud[22] 
                        select23 = path_on_cloud[23] 
                        select24 = path_on_cloud[24] 
                        select25 = path_on_cloud[25] 
                        select26 = path_on_cloud[26] 
                    
                        
                        # v = i.name
                        total_of_select =select0 + select1+ select2+select3+select4+select5+select6+select7+select8+  select9 + select10 + select11 + select12 + select13 +  select14+ select15+ select16+ select17+ select18+ select19+ select20+ select21 + select22+ select23+ select24+ select25+ select26 
                        print("this is total")
                        print(total_of_select)
                        
                        
                                        

                        path_local = "media/" + data
                        
                        storage.child(path_on_cloud).put(path_local)
                        # storage.child(data).download(total_of_select,"img_note/correct.png")
                        auth = firebase.auth()
                        email = "helplinegndpcollege12345@gmail.com"
                        password = "helplinegndpcollege12345"
                        user = auth.sign_in_with_email_and_password(email, password)
                        url = storage.child(path_on_cloud).get_url(user['idToken'])
                        print(url)
                        query_again = "update calc_notesaddcse set image_url ='%s'" % url + "where code ='%s'" % random_str
                        print(query_again)
                        cursor6 = connection.cursor()
        
                        w = cursor6.execute(query_again)
                        
                        
                        connection.commit()
                        context = {

                        }
                        context['url'] = url
                        request.session['url_session'] = url
                        print("working")
                        shutil.rmtree('C:/Users/gurnishan/Downloads/Compressed/mj/mj/media/img_note/2021/') 
                        return render(request,'notes_register.html',context)
            elif combine_data == 'notesaddcivil':
                print("working")
                for i in pic:
                    note_save = notesaddcivil(name=name,rollno=rollno,section=section,sem=sem,email_id=email,phone_no=phoneno,notes_name=notes_name,subject=subject,description=description,code=random_str,verificationstatus=status,image=i)
                    note_save.save()  
                    
                
                    print(random_str)
                    
                    print("workin")
                    
                    query = ("select * from calc_notesaddcivil where code = '%s'" % random_str)
                    print(query)
                    cursor4 = connection.cursor()
                    print(cursor4)
                    d = cursor4.execute(query)
                    print(d)
                    # get all records
                    records_query = cursor4.fetchall()
                    
                    for row in records_query:
                        print(row)
                        print("here working")
                        data  = row[12]
                        print(data)
                        
                        config ={
                            "apiKey": "AIzaSyCKWWPehnuKB6Cz0dh4H0INunG3Lu4MnHs",
                            "authDomain": "gndpc-44049.firebaseapp.com",
                            "projectId": "gndpc-44049",
                            "databaseURL":"https://gndpc-44049-default-rtdb.firebaseio.com/",
                            "storageBucket": "gndpc-44049.appspot.com",
                            "messagingSenderId": "92108007781",
                            "appId": "1:92108007781:web:0dc3ed150b264bc632198c",
                            "measurementI": "G-5E1G72WKR8"
                        }
                        
                        firebase = pyrebase.initialize_app(config)
                        storage = firebase.storage()


                        path_on_cloud = data
                        print("wokring")
                        print(path_on_cloud)
                        select0 = path_on_cloud[0]
                        select1 = path_on_cloud[1]
                        print(select1)
                        select2 = path_on_cloud[2]
                        select3 = path_on_cloud[3]
                        
                        select4 = path_on_cloud[4]
                        select5 = path_on_cloud[5]
                        select6 = path_on_cloud[6]
                        select7 = path_on_cloud[7]
                        select8 = path_on_cloud[8]
                        select9 = path_on_cloud[9]
                        select10 = path_on_cloud[10]
                        select11 = path_on_cloud[11]
                        select12 = path_on_cloud[12]
                        select13 = path_on_cloud[13]
                        select14 = path_on_cloud[14]
                        select15 = path_on_cloud[15]
                        select16 = path_on_cloud[16]
                        select17 = path_on_cloud[17]
                        select18 = path_on_cloud[18]
                        select19 = path_on_cloud[19]
                        select20 = path_on_cloud[20]
                        select21 = path_on_cloud[21]
                        select22 = path_on_cloud[22] 
                        select23 = path_on_cloud[23] 
                        select24 = path_on_cloud[24] 
                        select25 = path_on_cloud[25] 
                        select26 = path_on_cloud[26] 
                    
                        
                        # v = i.name
                        total_of_select =select0 + select1+ select2+select3+select4+select5+select6+select7+select8+  select9 + select10 + select11 + select12 + select13 +  select14+ select15+ select16+ select17+ select18+ select19+ select20+ select21 + select22+ select23+ select24+ select25+ select26 
                        print("this is total")
                        print(total_of_select)
                        
                        
                                        

                        path_local = "media/" + data
                        
                        storage.child(path_on_cloud).put(path_local)
                        # storage.child(data).download(total_of_select,"img_note/correct.png")
                        auth = firebase.auth()
                        email = "helplinegndpcollege12345@gmail.com"
                        password = "helplinegndpcollege12345"
                        user = auth.sign_in_with_email_and_password(email, password)
                        url = storage.child(path_on_cloud).get_url(user['idToken'])
                        print(url)
                        query_again = "update calc_notesaddcivil set image_url ='%s'" % url + "where code ='%s'" % random_str
                        print(query_again)
                        cursor6 = connection.cursor()
        
                        w = cursor6.execute(query_again)
                        
                        
                        connection.commit()
                        context = {

                        }
                        context['url'] = url
                        request.session['url_session'] = url
                        print("working")
                        shutil.rmtree('C:/Users/gurnishan/Downloads/Compressed/mj/mj/media/img_note/2021/') 
                        return render(request,'notes_register.html',context)
            elif combine_data == 'notesaddelectrical':
                print("working")
                for i in pic:
                    note_save = notesaddelectrical(name=name,rollno=rollno,section=section,sem=sem,email_id=email,phone_no=phoneno,notes_name=notes_name,subject=subject,description=description,code=random_str,verificationstatus=status,image=i)
                    note_save.save()  
                    
                
                    print(random_str)
                    
                    print("workin")
                    
                    query = ("select * from calc_notesaddelectrical where code = '%s'" % random_str)
                    print(query)
                    cursor4 = connection.cursor()
                    print(cursor4)
                    d = cursor4.execute(query)
                    print(d)
                    # get all records
                    records_query = cursor4.fetchall()
                    
                    for row in records_query:
                        print(row)
                        print("here working")
                        data  = row[12]
                        print(data)
                        
                        config ={
                            "apiKey": "AIzaSyCKWWPehnuKB6Cz0dh4H0INunG3Lu4MnHs",
                            "authDomain": "gndpc-44049.firebaseapp.com",
                            "projectId": "gndpc-44049",
                            "databaseURL":"https://gndpc-44049-default-rtdb.firebaseio.com/",
                            "storageBucket": "gndpc-44049.appspot.com",
                            "messagingSenderId": "92108007781",
                            "appId": "1:92108007781:web:0dc3ed150b264bc632198c",
                            "measurementI": "G-5E1G72WKR8"
                        }
                        
                        firebase = pyrebase.initialize_app(config)
                        storage = firebase.storage()


                        path_on_cloud = data
                        print("wokring")
                        print(path_on_cloud)
                        select0 = path_on_cloud[0]
                        select1 = path_on_cloud[1]
                        print(select1)
                        select2 = path_on_cloud[2]
                        select3 = path_on_cloud[3]
                        
                        select4 = path_on_cloud[4]
                        select5 = path_on_cloud[5]
                        select6 = path_on_cloud[6]
                        select7 = path_on_cloud[7]
                        select8 = path_on_cloud[8]
                        select9 = path_on_cloud[9]
                        select10 = path_on_cloud[10]
                        select11 = path_on_cloud[11]
                        select12 = path_on_cloud[12]
                        select13 = path_on_cloud[13]
                        select14 = path_on_cloud[14]
                        select15 = path_on_cloud[15]
                        select16 = path_on_cloud[16]
                        select17 = path_on_cloud[17]
                        select18 = path_on_cloud[18]
                        select19 = path_on_cloud[19]
                        select20 = path_on_cloud[20]
                        select21 = path_on_cloud[21]
                        select22 = path_on_cloud[22] 
                        select23 = path_on_cloud[23] 
                        select24 = path_on_cloud[24] 
                        select25 = path_on_cloud[25] 
                        select26 = path_on_cloud[26] 
                    
                        
                        # v = i.name
                        total_of_select =select0 + select1+ select2+select3+select4+select5+select6+select7+select8+  select9 + select10 + select11 + select12 + select13 +  select14+ select15+ select16+ select17+ select18+ select19+ select20+ select21 + select22+ select23+ select24+ select25+ select26 
                        print("this is total")
                        print(total_of_select)
                        
                        
                                        

                        path_local = "media/" + data
                        
                        storage.child(path_on_cloud).put(path_local)
                        # storage.child(data).download(total_of_select,"img_note/correct.png")
                        auth = firebase.auth()
                        email = "helplinegndpcollege12345@gmail.com"
                        password = "helplinegndpcollege12345"
                        user = auth.sign_in_with_email_and_password(email, password)
                        url = storage.child(path_on_cloud).get_url(user['idToken'])
                        print(url)
                        query_again = "update calc_notesaddelectrical set image_url ='%s'" % url + "where code ='%s'" % random_str
                        print(query_again)
                        cursor6 = connection.cursor()
        
                        w = cursor6.execute(query_again)
                        
                        
                        connection.commit()
                        context = {

                        }
                        context['url'] = url
                        request.session['url_session'] = url
                        print("working")
                        shutil.rmtree('C:/Users/gurnishan/Downloads/Compressed/mj/mj/media/img_note/2021/') 
                        return render(request,'notes_register.html',context)
            elif combine_data == 'notesaddmechanical':
                print("working")
                for i in pic:
                    note_save = notesaddmechanical(name=name,rollno=rollno,section=section,sem=sem,email_id=email,phone_no=phoneno,notes_name=notes_name,subject=subject,description=description,code=random_str,verificationstatus=status,image=i)
                    note_save.save()  
                    
                
                    print(random_str)
                    
                    print("workin")
                    
                    query = ("select * from calc_notesaddmechanical where code = '%s'" % random_str)
                    print(query)
                    cursor4 = connection.cursor()
                    print(cursor4)
                    d = cursor4.execute(query)
                    print(d)
                    # get all records
                    records_query = cursor4.fetchall()
                    
                    for row in records_query:
                        print(row)
                        print("here working")
                        data  = row[12]
                        print(data)
                        
                        config ={
                            "apiKey": "AIzaSyCKWWPehnuKB6Cz0dh4H0INunG3Lu4MnHs",
                            "authDomain": "gndpc-44049.firebaseapp.com",
                            "projectId": "gndpc-44049",
                            "databaseURL":"https://gndpc-44049-default-rtdb.firebaseio.com/",
                            "storageBucket": "gndpc-44049.appspot.com",
                            "messagingSenderId": "92108007781",
                            "appId": "1:92108007781:web:0dc3ed150b264bc632198c",
                            "measurementI": "G-5E1G72WKR8"
                        }
                        
                        firebase = pyrebase.initialize_app(config)
                        storage = firebase.storage()


                        path_on_cloud = data
                        print("wokring")
                        print(path_on_cloud)
                        select0 = path_on_cloud[0]
                        select1 = path_on_cloud[1]
                        print(select1)
                        select2 = path_on_cloud[2]
                        select3 = path_on_cloud[3]
                        
                        select4 = path_on_cloud[4]
                        select5 = path_on_cloud[5]
                        select6 = path_on_cloud[6]
                        select7 = path_on_cloud[7]
                        select8 = path_on_cloud[8]
                        select9 = path_on_cloud[9]
                        select10 = path_on_cloud[10]
                        select11 = path_on_cloud[11]
                        select12 = path_on_cloud[12]
                        select13 = path_on_cloud[13]
                        select14 = path_on_cloud[14]
                        select15 = path_on_cloud[15]
                        select16 = path_on_cloud[16]
                        select17 = path_on_cloud[17]
                        select18 = path_on_cloud[18]
                        select19 = path_on_cloud[19]
                        select20 = path_on_cloud[20]
                        select21 = path_on_cloud[21]
                        select22 = path_on_cloud[22] 
                        select23 = path_on_cloud[23] 
                        select24 = path_on_cloud[24] 
                        select25 = path_on_cloud[25] 
                        select26 = path_on_cloud[26] 
                    
                        
                        # v = i.name
                        total_of_select =select0 + select1+ select2+select3+select4+select5+select6+select7+select8+  select9 + select10 + select11 + select12 + select13 +  select14+ select15+ select16+ select17+ select18+ select19+ select20+ select21 + select22+ select23+ select24+ select25+ select26 
                        print("this is total")
                        print(total_of_select)
                        
                        
                                        

                        path_local = "media/" + data
                        
                        storage.child(path_on_cloud).put(path_local)
                        # storage.child(data).download(total_of_select,"img_note/correct.png")
                        auth = firebase.auth()
                        email = "helplinegndpcollege12345@gmail.com"
                        password = "helplinegndpcollege12345"
                        user = auth.sign_in_with_email_and_password(email, password)
                        url = storage.child(path_on_cloud).get_url(user['idToken'])
                        print(url)
                        query_again = "update calc_notesaddmechanical set image_url ='%s'" % url + "where code ='%s'" % random_str
                        print(query_again)
                        cursor6 = connection.cursor()
        
                        w = cursor6.execute(query_again)
                        
                        
                        connection.commit()
                        context = {

                        }
                        context['url'] = url
                        request.session['url_session'] = url
                        print("working")
                        shutil.rmtree('C:/Users/gurnishan/Downloads/Compressed/mj/mj/media/img_note/2021/') 
                        return render(request,'notes_register.html',context)
            elif combine_data == 'notesaddauto':
                print("working")
                for i in pic:
                    note_save = notesaddauto(name=name,rollno=rollno,section=section,sem=sem,email_id=email,phone_no=phoneno,notes_name=notes_name,subject=subject,description=description,code=random_str,verificationstatus=status,image=i)
                    note_save.save()  
                    
                
                    print(random_str)
                    
                    print("workin")
                    
                    query = ("select * from calc_notesaddauto where code = '%s'" % random_str)
                    print(query)
                    cursor4 = connection.cursor()
                    print(cursor4)
                    d = cursor4.execute(query)
                    print(d)
                    # get all records
                    records_query = cursor4.fetchall()
                    
                    for row in records_query:
                        print(row)
                        print("here working")
                        data  = row[12]
                        print(data)
                        
                        config ={
                            "apiKey": "AIzaSyCKWWPehnuKB6Cz0dh4H0INunG3Lu4MnHs",
                            "authDomain": "gndpc-44049.firebaseapp.com",
                            "projectId": "gndpc-44049",
                            "databaseURL":"https://gndpc-44049-default-rtdb.firebaseio.com/",
                            "storageBucket": "gndpc-44049.appspot.com",
                            "messagingSenderId": "92108007781",
                            "appId": "1:92108007781:web:0dc3ed150b264bc632198c",
                            "measurementI": "G-5E1G72WKR8"
                        }
                        
                        firebase = pyrebase.initialize_app(config)
                        storage = firebase.storage()


                        path_on_cloud = data
                        print("wokring")
                        print(path_on_cloud)
                        select0 = path_on_cloud[0]
                        select1 = path_on_cloud[1]
                        print(select1)
                        select2 = path_on_cloud[2]
                        select3 = path_on_cloud[3]
                        
                        select4 = path_on_cloud[4]
                        select5 = path_on_cloud[5]
                        select6 = path_on_cloud[6]
                        select7 = path_on_cloud[7]
                        select8 = path_on_cloud[8]
                        select9 = path_on_cloud[9]
                        select10 = path_on_cloud[10]
                        select11 = path_on_cloud[11]
                        select12 = path_on_cloud[12]
                        select13 = path_on_cloud[13]
                        select14 = path_on_cloud[14]
                        select15 = path_on_cloud[15]
                        select16 = path_on_cloud[16]
                        select17 = path_on_cloud[17]
                        select18 = path_on_cloud[18]
                        select19 = path_on_cloud[19]
                        select20 = path_on_cloud[20]
                        select21 = path_on_cloud[21]
                        select22 = path_on_cloud[22] 
                        select23 = path_on_cloud[23] 
                        select24 = path_on_cloud[24] 
                        select25 = path_on_cloud[25] 
                        select26 = path_on_cloud[26] 
                    
                        
                        # v = i.name
                        total_of_select =select0 + select1+ select2+select3+select4+select5+select6+select7+select8+  select9 + select10 + select11 + select12 + select13 +  select14+ select15+ select16+ select17+ select18+ select19+ select20+ select21 + select22+ select23+ select24+ select25+ select26 
                        print("this is total")
                        print(total_of_select)
                        
                        
                                        

                        path_local = "media/" + data
                        
                        storage.child(path_on_cloud).put(path_local)
                        # storage.child(data).download(total_of_select,"img_note/correct.png")
                        auth = firebase.auth()
                        email = "helplinegndpcollege12345@gmail.com"
                        password = "helplinegndpcollege12345"
                        user = auth.sign_in_with_email_and_password(email, password)
                        url = storage.child(path_on_cloud).get_url(user['idToken'])
                        print(url)
                        query_again = "update calc_notesaddauto set image_url ='%s'" % url + "where code ='%s'" % random_str
                        print(query_again)
                        cursor6 = connection.cursor()
        
                        w = cursor6.execute(query_again)
                        
                        
                        connection.commit()
                        context = {

                        }
                        context['url'] = url
                        request.session['url_session'] = url
                        print("working")
                        shutil.rmtree('C:/Users/gurnishan/Downloads/Compressed/mj/mj/media/img_note/2021/') 
                        return render(request,'notes_register.html',context)
            

                    # user = complaintregister(name=name,rollno=rollno,phoneno=phoneno,email=email,description=description,image=i)
            else:
                return render(request,'notes_register.html')
        else:
            data2 = {
                'error' : error_message,
                'values':values
            }
            return render(request,'notes_register.html', data2)
    else:
        return render(request,'notes_register.html')
def loginc_verify(request):
    print("hii  ")
    if request.method == 'POST':
        print("hi")
        name = request.POST['_id']
        request.session['id'] = name
        password = request.POST['password']
        request.session['password'] = password
        context = {
            'name' : name,
            
        } 
        if name != '' and password !='':
            connection = mysql.connector.connect(host='localhost',
                                                                    database='major',
                                                                    user='root',
                                                                    password='')
            query = ("select * from calc_loginc where name = '%s'" % name + " and " + "password = '%s'" % password)
            
            
            
            cursor6 = connection.cursor()
        
            w = cursor6.execute(query)
            
            records_query = cursor6.fetchall()
            print(cursor6.rowcount, "record(s) affected")  
            connection.commit()
            for i in records_query:
                row = i[5]  
                print("this is row",row)
                row_subject = i[3]
            
            context = {
                'name' : name,
                'error' : "No account found"
            } 
            
            if cursor6.rowcount == 1:
                query2 =("select * from calc_" + row + " where verificationstatus = 0 and subject = '%s'" % row_subject)    
                print(query2)
                cursor7 = connection.cursor()
                w = cursor7.execute(query2) 
                records_query2 = cursor7.fetchall()
                print(records_query2)
                if records_query2 != []:
                    thislist1 = []
                    for r in records_query2:
                        
                        context = {

                        }
                        thislist1.append(r)
                        
                        context['name'] = r[1]
                        context['rollno'] = r[2]
                        context['section'] = r[3]
                        context['sem'] = r[4]
                        context['email_id'] = r[5]
                        context['phone_no'] = r[6]
                        context['notes_name'] = r[7]
                        context['subject'] = r[8]
                        context['database'] = row
                        context['code'] = r[10]
                        context['url'] = r[13]
                        
                        
                        context['thislist1'] = thislist1
                    
                    print("hearere")
                    return render(request,'controlp.html',context)
                else:
                    print("this2")
                    context = {}
                    context['noentry'] = "no request found"
                    return render(request,'controlp.html',context)
            else:
                
                return render(request,'loginC.html',context)
        else:
            context = {
                    
                    'error' : "please fill details "
                }
            return render(request,'loginC.html',context)
    else:
        return render(request,'loginC.html')
        
        

def verify_notes_by_teacher(request):
    database = request.GET.get('database')

    mod_string2 = database[database.index("_"):]
    total_code = mod_string2[1:]
    print("totalcode,",total_code)

    total_database = database[:database.index("_")]
    print(total_database)
    
    print(total_code)
    
    
    connection = mysql.connector.connect(host='localhost',
                                        database='major',
                                        user='root',
                                        password='')
    print("hii")
    query_update = "update calc_" + total_database + " set verificationstatus ='1' where code ='%s'" % total_code 
    print(query_update)  
    cursor11 = connection.cursor()
       
    w1 = cursor11.execute(query_update) 
    print(w1)
    # query_update11 = cursor11.fetchall()

    
    print(cursor11.rowcount, "record(s) affected")  
    connection.commit()
    cursor11.close()
    connection.close()
    print("MySQL connection is closed")
    return fff(request)
def fff(request):
    _id = request.session['id']
    password = request.session['password']
    connection = mysql.connector.connect(host='localhost',
                                                                database='major',
                                                                user='root',
                                                                password='')
    query = ("select * from calc_loginc where name = '%s'" % _id + " and " + "password = '%s'" % password)
    
    
    
    cursor6 = connection.cursor()
    
    w = cursor6.execute(query)
    
    records_query = cursor6.fetchall()
    for i in records_query:
        row = i[5]
        row_subject_fff = i[3]

    print(row)
    print(cursor6.rowcount, "record(s) affected")  
    connection.commit()
    if cursor6.rowcount == 1:
        query2 =("select * from calc_" + row + " where verificationstatus = 0 and subject = '%s'" % row_subject_fff)    
        print(query2)
        cursor7 = connection.cursor()
        w = cursor7.execute(query2) 
        records_query2 = cursor7.fetchall()
        print(records_query2)
        if records_query2 != []:
            thislist1 = []
            for r in records_query2:
                
                context = {

                }
                thislist1.append(r[0])
                
                context['name'] = r[1]
                context['rollno'] = r[2]
                context['section'] = r[3]
                context['sem'] = r[4]
                context['email_id'] = r[5]
                context['phone_no'] = r[6]
                context['notes_name'] = r[7]
                context['subject'] = r[8]
                context['database'] = row
                context['code'] = r[10]
                
                
                context['thislist1'] = thislist1
            
            
            return render(request,'controlp.html',context)
        else:
            context = {}
            context['noentry'] = "no request found"
            return render(request,'controlp.html',context)

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("homepage")

def get_topics_ajax(request):
    
    if request.method == "GET":
        
        subject_id = request.GET['subject_id']
        print(subject_id)
        try:
            subject = Country.objects.filter(id = subject_id).first()
            print("subject ",subject)
            topics = City.objects.filter(country_id = subject)
            print(topics)
        except Exception:
            data = 'error'
            return JsonResponse(data)
        return JsonResponse(list(topics.values('id', 'name')), safe = False)  
    
def admin(request):
    return render(request, "admin.html")

def show_subject_in_addsubject(request):
    if request.method == "GET":
        trade_ = request.GET['trade']
        trade_total_ = trade_ + "1"
        print("this is 1",trade_total_)
        
        query2_ =("select * from calc_country where name ='%s'" % trade_total_)    
        print(query2_)
        cursor7_ = connection.cursor()
        w_ = cursor7_.execute(query2_) 
        records_query2_ = cursor7_.fetchall()
       
        print(records_query2_)
        
        for r_ in records_query2_:
            print("this is sem 1")
            value = r_[0]
            print(value)
            try:
                print("wrokin")
                all = Country.objects.filter(id = value).first()
                print(all)
                all1 = City.objects.filter(country_id = all)
                print(all1)
            except Exception:
                data = 'error'
                return JsonResponse(data)
            return JsonResponse(list(all1.values('id', 'name')), safe = False)  
    # return render(request,'admin.html',context)
def show_subject_in_addsubject2(request):
    if request.method == "GET":
       
        trade2 = request.GET['trade2']
        trade_total2 = trade2 + "2"
        print(trade_total2)
        
        query2 =("select * from calc_country where name ='%s'" % trade_total2)    
        print(query2)
        cursor2 = connection.cursor()
        w2 = cursor2.execute(query2) 
        records_query2 = cursor2.fetchall()
        print(records_query2)
        
        for r2 in records_query2:
            print("this is sem 2")
            value2= r2[0]
           
            try:
                record = Country.objects.filter(id = value2).first()
                print(record)
                record2 = City.objects.filter(country_id = record)
                print(record2)
            except Exception:
                data = 'error'
                return JsonResponse(data)
            return JsonResponse(list(record2.values('id', 'name')), safe = False) 
def show_subject_in_addsubject3(request):
    if request.method == "GET":
       
        trade___ = request.GET['trade3']
        trade_total___ = trade___ + "3"
        print(trade_total___)
        
        query2___ =("select * from calc_country where name ='%s'" % trade_total___)    
        print(query2___)
        cursor7___ = connection.cursor()
        w = cursor7___.execute(query2___) 
        records_query2___ = cursor7___.fetchall()
        print(records_query2___)
        
        for r___ in records_query2___:
          
            value___ = r___[0]
           
            try:
                f = Country.objects.filter(id = value___).first()
                print(f)
                f2 = City.objects.filter(country_id = f)
                print(f2)
            except Exception:
                data = 'error'
                return JsonResponse(data)
            return JsonResponse(list(f2.values('id', 'name')), safe = False) 
def show_subject_in_addsubject4(request):
    if request.method == "GET":
       
        trade____ = request.GET['trade4']
        trade_total____ = trade____ + "4"
        print(trade_total____)
        
        query2____ =("select * from calc_country where name ='%s'" % trade_total____)    
        print(query2____)
        cursor7____ = connection.cursor()
        w____ = cursor7____.execute(query2____) 
        records_query2____ = cursor7____.fetchall()
        print(records_query2____)
        
        for r____ in records_query2____:
          
            value____ = r____[0] 
           
            try:
                all1 = Country.objects.filter(id = value____).first()
                print(all1)
                all2 = City.objects.filter(country_id = all1)
                print(all2)
            except Exception:
                data = 'error'
                return JsonResponse(data)
            return JsonResponse(list(all2.values('id', 'name')), safe = False) 

def show_subject_in_addsubject5(request):
    if request.method == "GET":
        
        trade_____ = request.GET['trade5']
        print(trade_____)
        trade_total_____ = trade_____ + "5"
        print(trade_total_____)
        
        query2_____ =("select * from calc_country where name ='%s'" % trade_total_____)    
        print(query2_____)
        cursor7_____ = connection.cursor()
        w_____ = cursor7_____.execute(query2_____) 
        records_query2_____ = cursor7_____.fetchall()
        print(records_query2_____)
        
        for r_____ in records_query2_____:
          
            value_____ = r_____[0]
           
            try:
                all1 = Country.objects.filter(id = value_____).first()
                print(all1)
                all2 = City.objects.filter(country_id = all1)
                print(all2)
            except Exception:
                data = 'error'
                return JsonResponse(data)
            return JsonResponse(list(all2.values('id', 'name')), safe = False) 

def show_subject_in_addsubject6(request):
    if request.method == "GET":
        
        trade______ = request.GET['trade6']
        trade_total______ = trade______ + "6"
        print(trade_total______)
        
        query2______ =("select * from calc_country where name ='%s'" % trade_total______)    
        print(query2______)
        cursor7______ = connection.cursor()
        w = cursor7______.execute(query2______) 
        records_query2______ = cursor7______.fetchall()
        print(records_query2______)
        
        for r______ in records_query2______:
          
            value______ = r______[0]
            print(value______)
            try:
                all1 = Country.objects.filter(id = value______).first()
                print("sem",all1)
                all2 = City.objects.filter(country_id = all1)
                print(all2)
            except Exception:
                data = 'error'
                return JsonResponse(data)
            return JsonResponse(list(all2.values('id', 'name')), safe = False) 

def admin_add_subject(request):
    if request.method == 'POST':  
        trade = request.POST['trade']
        sem = request.POST['sem']
        sub = request.POST['sub']
        total = trade + sem
        total_all = trade + sem + sub
        record = checking_tradesemsubject.objects.filter(total = total_all).exists()
        
        print(record)
        if record == True :
            print("already subject present")
            context = {
                'error' : "Already present ",
                
            }
            return render(request,"admin.html",context)
        else:
            print("this is working")
            # data = Country(name=total)
            # data.save()
            connection = mysql.connector.connect(host='localhost',
                                                                database='major',
                                                                user='root',
                                                                password='')
            query = ("select * from calc_country where name = '%s'" % total)
            print(query)
            
            
            cursor6 = connection.cursor()
            
            w = cursor6.execute(query)
            
            records_query = cursor6.fetchall()
            for i in records_query:
                print(i[0])
                d = i[0]
                print(d)
            add_q = City(name = sub,country_id = d)
            add_q.save()
            add_total = checking_tradesemsubject(total = total_all)
            add_total.save()
            # print(id_)
            # data2 = City(name = sub,)
              
            return render(request,"admin.html")
    else:
        return render(request,"admin.html")
def store_data(request):
    if request.method == "GET":
        
        trade = request.GET['trade']
        print(trade)
        print("hiii")
        print("hiii")
        print("hiii")
        print("hiii")
        request.session['trade'] = trade
        return HttpResponse('')
def store_data_full(request):
    
    if request.method == "GET":
        print("hi")
        trade = request.session['trade']
        print(trade)
        print("trdae via session",trade)
        subjectid = request.GET['subject_id']
        subject_id = trade + subjectid
        print(subject_id) 
        print(subject_id)
        try:
            subject = Country.objects.filter(name = subject_id).first()
            print("subject ",subject)
            topics = City.objects.filter(country_id = subject)
            
            print(topics)
            
           
        except Exception:
            data = 'error'
            return JsonResponse(data)
        return JsonResponse(list(topics.values('id', 'name')), safe = False)  
    else:
        return render(request,"admin.html") 

def delete_subject_query(request):
    if request.method == 'POST':
        trade = request.POST['trade']
        sem = request.POST['sem']
        total = trade + sem
        sub = request.POST['sub']
        
        query = ("select * from calc_country where name = '%s'" % total)
        cursor = connection.cursor()

        w = cursor.execute(query)
   
        records_query = cursor.fetchall()
        print(records_query)
        for i in records_query:
            id_ = i[0]
            print(id_)
            query2 = ("select * from calc_city where id = '%s'" % sub )
            
            print(query2)
            cursor2 = connection.cursor()

            w2 = cursor2.execute(query2)
    
            records_query2 = cursor2.fetchall()
            print(records_query2)
            for x in records_query2:
                subject = x[1]
                total_all = total + subject
                print(total_all)
                query3 = "DELETE FROM calc_city WHERE name = '%s'" % subject + " and country_id = '%s'" % id_
                query4 =  "DELETE FROM calc_checking_tradesemsubject WHERE total = '%s'" % total_all
                print(query3)
                print(query4)
                cursor3 = connection.cursor()
                cursor4 = connection.cursor()

                w = cursor3.execute(query3)
                w4 = cursor3.execute(query4)
                
                    
                connection.commit()

            
        return render(request,"admin.html")
    else:
        return render(request,"admin.html") 

def delete_subject(request):
    return render(request,"admin.html")

def update_subject_query(request):
    if request.method == 'POST':
        trade = request.POST['trade']
        sem = request.POST['sem']
        
        total = trade + sem
        sub = request.POST['sub']
        new_sub = request.POST['new_sub']
        
        query = ("select * from calc_country where name = '%s'" % total)
        cursor = connection.cursor()

        w = cursor.execute(query)
        print(w)
        records_query = cursor.fetchall()
        print(records_query)
        for i in records_query:
            id_ = i[0]
            print(id_)
            query2 = ("select * from calc_city where id = '%s'" % sub )
            
            print(query2)
            cursor2 = connection.cursor()

            w2 = cursor2.execute(query2)

            records_query2 = cursor2.fetchall()
            print(records_query2)
            for x in records_query2:
                subject = x[1]
                print(subject)
                total_all = total + subject
                total_all_ = trade + sem +  new_sub 
                print(total_all)
                query3 = "update calc_city set name = '%s'" % new_sub  + " WHERE name = '%s'" % subject + " and country_id = '%s'" % id_
                query4 =  "update calc_checking_tradesemsubject set total = '%s'" % total_all_ + " WHERE total = '%s'" % total_all
                print(query3)
                print(query4)
                cursor3 = connection.cursor()
                cursor4 = connection.cursor()

                w = cursor3.execute(query3)
                w4 = cursor3.execute(query4)
                
                    
                connection.commit()
            return render(request,"admin.html") 
    else:
        return render(request,"admin.html") 

def id_add_session_function(request):
    if request.method == "GET":
        
        trade_for_id = request.GET['trade_for_id']
        print(trade_for_id)
 
        request.session['trade_for_id'] = trade_for_id
        return HttpResponse('')
def id_add_after_session_function_for_semestervalue(request):
    
    if request.method == "GET":
        semester = request.GET['semester']
        trade_from_idsection =  request.session['trade_for_id']
        total_for_id =  trade_from_idsection +semester 
        request.session['trade_for_id_total'] = total_for_id 
        print(total_for_id)
        
        try:
            subject_id = Country.objects.filter(name = total_for_id).first()
            print("subject ",subject_id)
            topics_id = City.objects.filter(country_id = subject_id)
            
            print(topics_id)
            
           
        except Exception:
            data = 'error'
            return JsonResponse(data)
        return JsonResponse(list(topics_id.values('id', 'name')), safe = False)  
    else:
        return render(request,"admin.html") 

def id_add_after_session_function_for_namevalue(request):
    
    if request.method == "GET":
        semester = request.GET['name']
        trade_from_idsection =  request.session['trade_for_id']
        total_for_id =  trade_from_idsection +semester 
        request.session['trade_for_id_total'] = total_for_id 
        print("checking",total_for_id)
        
        try:
            
            topics_id = teachers.objects.filter(department_semsternumber = total_for_id)
            
            print(topics_id)
            for i in topics_id:
                print(i.name)
                request.session['name_value'] = i.name
           
        except Exception:
            data = 'error'
            return JsonResponse(data)
        return JsonResponse(list(topics_id.values('name')), safe = False)  
    else:
        return render(request,"admin.html") 

def id_add(request):
    if request.method == 'POST':
        trade_for_id_total = request.session['trade_for_id_total']
        
        trade_for_id = request.POST['trade_for_id']
        semester_for_id = request.POST['semester_for_id']
        id_choose_subject = request.POST['id_choose_subject']
        print(id_choose_subject)
        name = request.session['name_value']
        
        
        print("hiiii",name)
        password = request.POST['password']
       
        print(trade_for_id_total)
        trade_for_id_total_total = "notesadd" + trade_for_id
        print(trade_for_id_total_total)
        query1112 = ("select * from calc_city where id = '%s'" % id_choose_subject)
        cursor = connection.cursor()

        w = cursor.execute(query1112)

        records_query22 = cursor.fetchall()
        print("why ntow kring",records_query22)
        for i in records_query22:
            value = i[1]
            ii = loginC.objects.filter(subject = value).exists()
            print(ii)

            if ii == False:
                print("jo")
                addme = loginC(name=name,password=password,sem=semester_for_id,database=trade_for_id_total_total,subject=value)
                addme.save()
            else:
                print("hhh")
                context = {
                'error' : "id already present",
                
                } 
                return render(request,"admin.html",context)          
    return render(request,"admin.html") 

def id_delete(request):
    # delete_id_trade = request.POST['delete_id_trade']
    # semester_delete_id = request.POST['semester_delete_id']
    # subject_delete_id = request.POST['subject_delete_id']
    semvalue_id_a = request.GET['semvalue_id_a']
    print("this",semvalue_id_a)
    try:
        delete_topics_id = loginC.objects.filter(subject = semvalue_id_a)
        
        print(delete_topics_id)
        
        
    except Exception:
        data = 'error'
        return JsonResponse(data)
    return JsonResponse(list(delete_topics_id.values('name', 'password')), safe = False)  

def delete_id_aftereveyrhting(request):
    if request.method == 'POST':
        subject11 = request.POST['id_choose_subject']
        
     
        
        query = ("delete  from calc_loginc where subject = '%s'" % subject11)
        print(query)  
        cursor1111 = connection.cursor()
        
        w1 = cursor1111.execute(query) 
        print(w1)
        # query_update11 = cursor11.fetchall()

        
        
        connection.commit()
     
    return render(request,"admin.html") 

def id_update(request):
    # delete_id_trade = request.POST['delete_id_trade']
    # semester_delete_id = request.POST['semester_delete_id']
    # subject_delete_id = request.POST['subject_delete_id']
    semvalue_id_a = request.GET['semvalue_id_a']
    print("this",semvalue_id_a)
    try:
        delete_topics_id = loginC.objects.filter(subject = semvalue_id_a)
        
        print(delete_topics_id)
        
        
    except Exception:
        data = 'error'
        return JsonResponse(data)
    return JsonResponse(list(delete_topics_id.values('name', 'password')), safe = False)

def update_id(request):
    if request.method == 'POST':
        update_subject_id = request.POST['update_subject_id']
       
        
        name_update_id = request.POST['update_id_name']
        update_id_password = request.POST['update_id_password']
       
        
        query3 = "update calc_loginc set name = '%s'" % name_update_id  +" WHERE subject = '%s'" % update_subject_id 
        query4 = "update calc_loginc set password = '%s'" % update_id_password  +" WHERE subject = '%s'" % update_subject_id 
       
        print(query3)

        cursor3 = connection.cursor()
        cursor4 = connection.cursor()

        w23 = cursor3.execute(query3)
        w22 = cursor3.execute(query4)

        
            
        connection.commit()
    return render(request,"admin.html") 
    
def login_admin(request):
    return render(request, "loginAdmin.html")

def loginAdmin_verify(request):
    print("hii  ")
    if request.method == 'POST':
        print("hi")
        name = request.POST['_id']
        request.session['id'] = name
        password = request.POST['password']
        request.session['password'] = password
        if name != '' and password != '':
            context = {
                'name' : name,
                
            } 
            connection = mysql.connector.connect(host='localhost',
                                                                    database='major',
                                                                    user='root',
                                                                    password='')
            query = ("select * from calc_loginadmin where name = '%s'" % name + " and " + "password = '%s'" % password)
            
            
            
            cursor6 = connection.cursor()
        
            w = cursor6.execute(query)
            
            records_query = cursor6.fetchall()

            print(cursor6.rowcount, "record(s) affected")  
            connection.commit()
            if cursor6.rowcount == 1:
                return render(request,'admin.html')
            else:
                context = {
                    'name' : name,
                    'error' : "No account found "
                }
                return render(request,'loginAdmin.html',context)
        else:
            context = {
                    
                    'error' : "please fill details "
                }
            return render(request,'loginAdmin.html',context)
    else:
       
        return render(request,'loginAdmin.html')
    
def logout_request_admin(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("homepage_admin")

def shownotes_to_admin(request):
    if request.method == "GET":
        
        trade_choose_selecttrade = request.GET['trade_choose_selecttrade']
        print(trade_choose_selecttrade)
 
        request.session['trade_choose_selecttrade'] = trade_choose_selecttrade
        return HttpResponse('')
        
def shownotes_to_admin_after_session(request):
    semster_choose_selectsem = request.GET['semster_choose_selectsem']
    print("thissds",semster_choose_selectsem)
    trade_choose_selecttrade =  request.session['trade_choose_selecttrade']
    my_model = trade_choose_selecttrade
    print(trade_choose_selecttrade)
    if trade_choose_selecttrade == "notesaddcivil":
        try:
            delete_topics_id = notesaddcivil.objects.filter(sem = semster_choose_selectsem)
            print("deleteropicid",delete_topics_id)
        
            
            
        except Exception:
            data = 'error'
            return JsonResponse(data)
        return JsonResponse(list(delete_topics_id.values('name','subject','code','image_url')), safe = False)
    elif(trade_choose_selecttrade == "notesaddcse"):
        try:
            delete_topics_id = notesaddcse.objects.filter(sem = semster_choose_selectsem)
            print("deleteropicid",delete_topics_id)
        
            
            
        except Exception:
            data = 'error'
            return JsonResponse(data)
        return JsonResponse(list(delete_topics_id.values('name','subject','code','image_url')), safe = False)
    elif(trade_choose_selecttrade == "notesaddmechanical"):
        try:
            delete_topics_id = notesaddmechanical.objects.filter(sem = semster_choose_selectsem)
            print("deleteropicid",delete_topics_id)
        
            
            
        except Exception:
            data = 'error'
            return JsonResponse(data)
        return JsonResponse(list(delete_topics_id.values('name','subject','code','image_url')), safe = False)
    elif(trade_choose_selecttrade == "notesaddauto"):
        try:
            delete_topics_id = notesaddauto.objects.filter(sem = semster_choose_selectsem)
            print("deleteropicid",delete_topics_id)
        
            
            
        except Exception:
            data = 'error'
            return JsonResponse(data)
        return JsonResponse(list(delete_topics_id.values('name','subject','code','image_url')), safe = False)
    elif(trade_choose_selecttrade == "notesaddelectrical"):
        try:
            delete_topics_id = notesaddelectrical.objects.filter(sem = semster_choose_selectsem)
            print("deleteropicid",delete_topics_id)
        
            
            
        except Exception:
            data = 'error'
            return JsonResponse(data)
        return JsonResponse(list(delete_topics_id.values('name','subject','code','image_url')), safe = False)
    elif(trade_choose_selecttrade == "notesaddece"):
        try:
            delete_topics_id = notesaddece.objects.filter(sem = semster_choose_selectsem)
            print("deleteropicid",delete_topics_id)
        
            
            
        except Exception:
            data = 'error'
            return JsonResponse(data)
        return JsonResponse(list(delete_topics_id.values('name','subject','code','image_url')), safe = False)
def viewnotes_in_admin(request):
    if request.method == "POST":
        submit_value = request.POST.get('submit')
        print(submit_value)
        return HttpResponse('')
def delet_notesinadmin(request):
    submit_value = request.GET.get('data')
    print(submit_value)
    trade_choose_selecttrade =  request.session['trade_choose_selecttrade']

    query2 = ("select * from calc_" + trade_choose_selecttrade + " where code = '%s'" % submit_value )
        
    print(query2)
    cursor2 = connection.cursor()

    w2 = cursor2.execute(query2)

    records_query2 = cursor2.fetchall()
    
    for x in records_query2:
        subject = x[12]
        print(subject)

        config ={
                    "apiKey": "AIzaSyCKWWPehnuKB6Cz0dh4H0INunG3Lu4MnHs",
                    "authDomain": "gndpc-44049.firebaseapp.com",
                    "projectId": "gndpc-44049",
                    "databaseURL":"https://gndpc-44049-default-rtdb.firebaseio.com/",
                    "storageBucket": "gndpc-44049.appspot.com",
                    "serviceAccount": "gndpc-44049-firebase-adminsdk-bcioz-9f21adb34d.json",
                    "messagingSenderId": "92108007781",
                    "appId": "1:92108007781:web:0dc3ed150b264bc632198c",
                    "measurementI": "G-5E1G72WKR8"
                }

        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()

        h = storage.delete(subject)
        print(h)
        query3 = "DELETE FROM calc_" + trade_choose_selecttrade + " WHERE code = '%s'" % submit_value
        
        print(query3)
        
        cursor3 = connection.cursor()
        # cursor4 = connection.cursor()

        w = cursor3.execute(query3)
        # w4 = cursor3.execute(query4)

            
        connection.commit()

    return render(request,'admin.html')