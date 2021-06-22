from django.db import models

# Create your models here.
class complaintregister(models.Model):
    
    name = models.CharField(max_length=100)
    rollno =  models.CharField(max_length=100)
    phoneno =  models.CharField(max_length=100)
    email =  models.CharField(max_length=100)
    verification_code = models.CharField(max_length=100)
    description =  models.CharField(max_length=100)
    d = "img/%Y/%m/%d/%H%M%S"
    image=models.ImageField(upload_to= d ,) 
     
    def __str__(self):
        return self.name

class complaintregister_verification(models.Model):
    name = models.CharField(max_length=100)
    verification_code = models.CharField(max_length=100)
    verification_status = models.CharField(max_length=10)
    token_code = models.CharField(max_length=20000)

class notesaddcse(models.Model):
    name = models.CharField(max_length=100)
    rollno = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    sem = models.CharField(max_length=10)
    email_id = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    notes_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    description =  models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    verificationstatus = models.CharField(max_length=10)
    d = "img_note/%Y/%m/%d/%H%M%S"
    image=models.ImageField(upload_to= d )
    image_url=models.CharField(max_length=20000)

class notesaddece(models.Model):
    name = models.CharField(max_length=100)
    rollno = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    sem = models.CharField(max_length=10)
    email_id = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    notes_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    description =  models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    verificationstatus = models.CharField(max_length=10)
    d = "img_note/%Y/%m/%d/%H%M%S"
    image=models.FileField(upload_to= d )
    image_url=models.CharField(max_length=20000)
    

class notesaddcivil(models.Model):
    name = models.CharField(max_length=100)
    rollno = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    sem = models.CharField(max_length=10)
    email_id = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    notes_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    description =  models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    verificationstatus = models.CharField(max_length=10)
    d = "img_note/%Y/%m/%d/%H%M%S"
    image=models.FileField(upload_to= d )
    image_url=models.CharField(max_length=20000)

class notesaddmechanical(models.Model):
    name = models.CharField(max_length=100)
    rollno = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    sem = models.CharField(max_length=10)
    email_id = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    notes_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    description =  models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    verificationstatus = models.CharField(max_length=10)
    d = "img_note/%Y/%m/%d/%H%M%S"
    image=models.FileField(upload_to= d )
    image_url=models.CharField(max_length=20000)
class notesaddauto(models.Model):
    name = models.CharField(max_length=100)
    rollno = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    sem = models.CharField(max_length=10)
    email_id = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    notes_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    description =  models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    verificationstatus = models.CharField(max_length=10)
    d = "img_note/%Y/%m/%d/%H%M%S"
    image=models.FileField(upload_to= d )
    image_url=models.CharField(max_length=20000)

class notesaddelectrical(models.Model):
    name = models.CharField(max_length=100)
    rollno = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    sem = models.CharField(max_length=10)
    email_id = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    notes_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    description =  models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    verificationstatus = models.CharField(max_length=10)
    d = "img_note/%Y/%m/%d/%H%M%S"
    image=models.FileField(upload_to= d )
    image_url=models.CharField(max_length=20000)

class loginC(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    subject = models.CharField(max_length=20)
    sem = models.CharField(max_length=20)
    database = models.CharField(max_length=20)
    def __str__(self):
        return self.name
class loginAdmin(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
class checking_tradesemsubject(models.Model):
    total = models.CharField(max_length=20)

class trades_and_data(models.Model):
    trade = models.CharField(max_length=20)
    sem = models.CharField(max_length=20)
    sub = models.CharField(max_length=20)


class teachers(models.Model):
    name = models.CharField(max_length=20)
    department_semsternumber = models.CharField(max_length=20)
    